import os
import yara
import py7zr
import zipfile
import requests

import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np
import io

import matplotlib.pyplot as plt
from copy import deepcopy


class MalConv(nn.Module):
    # trained to minimize cross-entropy loss: criterion = nn.CrossEntropyLoss()
    def __init__(
            self,
            embd_size=8, # dimensionality of the byte embeddings
            padding_idx=0, # padding index for the embedding layer
            total_nr_of_bytes=256, # number of possible byte values
            channels=256, # number of independent channels in the convolutional layer
            window_size=512, # size of the convolutional window
            stride=512, # stride (jump length) of the convolutional window
            out_size=2 # size of the output layer, corresponds to the number of classes we want to detect
    ):
        super(MalConv, self).__init__()
        self.padding_idx = padding_idx
        bytes_with_padding = total_nr_of_bytes + 1
        self.embd = nn.Embedding(bytes_with_padding, embd_size, padding_idx=padding_idx)
        
        self.window_size = window_size
    
        self.conv_1 = nn.Conv1d(embd_size, channels, window_size, stride=stride, bias=True)
        self.conv_2 = nn.Conv1d(embd_size, channels, window_size, stride=stride, bias=True)
        
        self.pooling = nn.AdaptiveMaxPool1d(1)
        
        self.fc_1 = nn.Linear(channels, channels)
        self.fc_2 = nn.Linear(channels, out_size)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # if padding_idx=0, bytes are shifted by 1 in forward pass
        x = x + 1 if self.padding_idx == 0 else x
        x = self.embd(x.long())
        x = torch.transpose(x, -1, -2)
        
        cnn_value = self.conv_1(x)
        gating_weight = torch.sigmoid(self.conv_2(x))
        
        x = cnn_value * gating_weight
        
        x = self.pooling(x)
        
        # flatten
        x = x.view(x.size(0), -1)
        
        x = F.relu(self.fc_1(x))
        x = self.fc_2(x)
        
        return x


class MalConvModel(object):
    def __init__(self, padding_idx: int = 0) -> None:
        self.model = MalConv(padding_idx=padding_idx)
        
    def load_state(self, model_weights):
        if isinstance(model_weights, str): # on disk
            weights = torch.load(model_weights, map_location='cpu', weights_only=True)
        elif isinstance(model_weights, bytes): # memory
            weights = torch.load(io.BytesIO(model_weights), map_location='cpu', weights_only=True)
        elif isinstance(model_weights, dict): # dict
            weights = model_weights
        else:
            raise ValueError("model_weights must be a file path, bytes, or dict")
        self.model.load_state_dict(weights['model_state_dict'])

    def get_score_from_bytez(self, bytez):
        bytez = bytez[:2000000]
        try:
            _inp = torch.from_numpy( np.frombuffer(bytez, dtype=np.uint8)[np.newaxis,:].copy() )
            with torch.no_grad():
                outputs = F.softmax( self.model(_inp), dim=-1)
            return outputs.detach().numpy()[0,1]
        except Exception as e:
            print(e)
        return 0.0

    def get_score_from_path(self, file_path):
        try:
            with open(file_path, 'rb') as fp:
                bytez = fp.read(2000000) # read the first 2000000 bytes
            return self.get_score_from_bytez(bytez)
        except Exception as e:
            print(e)
        return 0.0
    
    def get_score(self, input_data):
        if isinstance(input_data, str):
            return self.get_score_from_path(input_data)
        elif isinstance(input_data, bytes):
            return self.get_score_from_bytez(input_data)
        else:
            raise ValueError("input_data must be a file path or bytes")

    def is_evasive(self, input_data, threshold = 0.5):
        score = self.get_score(input_data)
        return score < threshold
    
    def predict_sample(self, input_data):
        return self.get_score(input_data)


def get_encrypted_archive(
        link: str = None,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        password: str = 'infected',
        remove_archive: bool = None
) -> bytes:
    if link.startswith("http://") or link.startswith("https://"):
        archive_name = link.split("/")[-1]
        with requests.get(link, headers={"User-Agent": user_agent}) as response:
            response.raise_for_status()
            archive = response.content
        
        with open(archive_name, "wb") as f:
            f.write(archive)
        if remove_archive is None:
            remove_archive = True
    else:
        archive_name = link
        if remove_archive is None:
            remove_archive = False
    
    if archive_name.endswith(".7z"):
        with py7zr.SevenZipFile(archive_name, "r", password=password) as archive:
            try:
                # vx-underground has single file <hash>.7z with <hash> inside
                file_hash = os.path.basename(archive_name).replace(".7z", "")
                content = archive.read(targets=[file_hash])[file_hash].read()
            except KeyError:
                print(f"[-] File {file_hash} not found in archive {archive_name}, providing all files")
                io_dict = archive.read(archive.getnames())
                content = {file: io_dict[file].read() for file in io_dict}

    elif archive_name.endswith(".zip"):
        # other sources, multiple files
        with zipfile.ZipFile(archive_name, "r") as archive:
            archive.setpassword(password.encode())
            content = {file: archive.read(file) for file in archive.namelist()}
    else:
        raise ValueError(f"[-] archive must be .7z or .zip, got: {archive_name}")

    if remove_archive:
        os.remove(archive_name)

    return content


class YaraWrapper(object):
    def __init__(self) -> None:
        pass
        
    def check_sample(self, sample_bytes, rules) -> yara.Match:
        rules = yara.compile(source=rules)
        self.matches = rules.match(data=sample_bytes)
        if self.matches:
            print(f"[+] Match found: {self.matches}")
        else:
            print("[-] No matches found.")
        return self.matches

    def pretty_print(self, print_limit=10):
        for match in self.matches:
            print(f"[!] Rule: {match.rule}")
            for i, string in enumerate(match.strings):
                for j, instance in enumerate(string.instances):
                    if j >= print_limit:
                        print(f"    [*] ... {len(string.instances) - print_limit} more\n")
                        break

                    print(f"    [+] Matched data: {instance.matched_data} | Offset: 0x{instance.offset:x}")
                    if string.is_xor():
                        print(f"\t[!] XOR key: {instance.xor_key}")
                        print(f"\t[!] Decoded: {instance.plaintext()}")
                
                if i >= print_limit:
                    print(f"\n  [*] ... {len(match.strings) - print_limit} more")
                    break
        

def plot_shap_values(
        shap_values: np.ndarray,
        name: str,
        range_start: int = 0,
        range_width: int = 512,
        ax: plt.Axes = None
):
    shap_values = shap_values.mean(axis=2).squeeze()
    
    pos_idx = shap_values >= 0
    neg_index = shap_values < 0
    
    pos_shap = deepcopy(shap_values)
    pos_shap[neg_index] = 0
    
    neg_shap = deepcopy(shap_values)
    neg_shap[pos_idx] = 0

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    
    # shap values is of input size, we will plot only the those in the range
    range_end = range_start + range_width
    x = np.arange(range_start, range_end)
    ax.bar(x, pos_shap[range_start:range_end])
    ax.bar(x, neg_shap[range_start:range_end])
    ax.set_title(name)
    ax.set_xlabel("Byte position")
    ax.set_ylabel("SHAP value")
    
    return ax

def find_most_influential_bytes(shap_values: np.ndarray, top_n: int = 10, positive: bool = True) -> np.ndarray:
    shap_values = shap_values.mean(axis=2).squeeze()
    print(shap_values.shape)
    if positive:
        return np.argsort(shap_values)[::-1][:top_n]
    else:
        return np.argsort(shap_values)[:top_n]

def find_hex_offset(byte_idx: int) -> str:
    # returnx 0x0000 format
    return f"0x{byte_idx:04x}"

def bytes_to_hex(bytes_: bytes) -> str:
    return " ".join([f"{byte:02x}" for byte in bytes_])
