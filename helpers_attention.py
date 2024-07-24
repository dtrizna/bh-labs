
import os

import numpy as np
from collections import Counter
from bertviz import head_view

import nebula
from nebula import PEDynamicFeatureExtractor, JSONTokenizerBPE, TransformerEncoderChunks

from torch import Tensor, sigmoid, manual_seed

def get_attn(x: Tensor, model: TransformerEncoderChunks):
    attentions = []
    x = model.pos_encoder(model.encoder(x))
    for layer in model.transformer_encoder.layers:
        this_layer_attn = layer.self_attn(x,x,x, average_attn_weights=False)[1]
        attentions.append(this_layer_attn.cpu().detach())
        x = layer(x)
    return attentions

def get_attention_report(report: dict, model: TransformerEncoderChunks, maxLen=512, seed=0):
    
    extractor = PEDynamicFeatureExtractor()
    exampleProcessed = extractor.filter_and_normalize_report(report)
    
    bpe_model_path = os.path.join(os.path.dirname(nebula.__file__), "objects", "bpe_50000_sentencepiece.model")
    vocab_path = os.path.join(os.path.dirname(nebula.__file__), "objects", "bpe_50000_vocab.json")
    tokenizer = JSONTokenizerBPE(
        vocab_size=50001,
        seq_len=maxLen,
        model_path=bpe_model_path,
        vocab=vocab_path
    )

    exampleTokenized = tokenizer.tokenize(exampleProcessed)[0]
    exampleEncoded = tokenizer.encode(exampleProcessed)[0]
    x = Tensor(exampleEncoded).long().reshape(1,-1)

    manual_seed(seed)
    logit = model.forward(x[:, :maxLen])
    prob = sigmoid(logit)
    logit_bad, prob_bad = logit[0].detach().item(), prob[0].detach().item()
    print(f"[!] Model scores on this sample -- logit: {logit_bad:.2f} and probability: {prob_bad*100:.2f}%")

    attentions = get_attn(x, model)
    return attentions, exampleTokenized

def attention_viz(start, end, attentions, exampleTokenized, threshold=0.005, layer=1, heads=[]):
    m = 1/threshold
    tokens = exampleTokenized[start:end]
    att_crop = [x[:, :, start:end, start:end]*m for x in attentions]
    head_view(att_crop, tokens, prettify_tokens=False, heads=heads, layer=layer)


def report_where_attends(seq_1, seq_2, token_location, tokenized_input):
    # TODO: somewhat broken?
    msg = ""
    token = tokenized_input[token_location]
    where_attends_seq_2 = np.where(seq_1 == token_location)[0]
    if len(where_attends_seq_2) > 0:
        counterpart_tokens = list(set([tokenized_input[x] for x in seq_2[where_attends_seq_2].tolist()]))
        if token in counterpart_tokens:
            counterpart_tokens.remove(token)
        if counterpart_tokens: # TODO: this part reports wrong results???
            msg = f"\t  It has connections with tokens at following locations and values:\n"
            msg += f"\t\tLocated: {where_attends_seq_2}\n"
            msg += f"\t\tValues: {counterpart_tokens}\n"
    return msg

def analyze_attentions(
        attentions,
        tokenized_input,
        threshold=0.005,
        diff=20,
        most_common=5,
        types=["proximity", "frequency"],
        limit=20,
        verbose=True,
        token_whitelist=[],
        visualize=True
):
    counter = 0
    print(f"\n[!] Analyzing attentions based on {types}... ")
    if token_whitelist:
        print(f"\n[!] Whitelisted tokens: {token_whitelist}... Everything else will be ignored!")
    for layer_nr, layer in enumerate(attentions):
        idxs = np.where(layer > threshold)
        print(f"\n[!] Total {len(idxs[0])} tokens has strong activations at layer {layer_nr} with threshold: {threshold}!")
        if len(idxs[0]) > 0:
            heads = idxs[1].tolist()
            attn_seq_1 = idxs[2]
            attn_seq_2 = idxs[3]

            if "proximity" in types:
                # PROXIMITY CHECK
                print(f"[*] Performing a token attention proximity check with token difference: {diff}... ")
                for j, (a1, a2) in enumerate(zip(attn_seq_1, attn_seq_2)):
                    # check if difference between a1 and a2 is below threshold
                    token_at_a1 = tokenized_input[a1]
                    token_at_a2 = tokenized_input[a2]
                    if token_at_a1 == token_at_a2:
                        continue
                    if token_whitelist and \
                        (token_at_a1.strip("▁") not in token_whitelist \
                         and token_at_a2.strip("▁") not in token_whitelist):
                            continue
                    if abs(a1 - a2) > diff:
                        if verbose:
                            print(f"\tThese two tokens has strong activations but are far (diff: {abs(a1 - a2)}):\n\t\t{token_at_a1}\n\t\t{token_at_a2}")
                    elif abs(a1 - a2) <= diff:
                        counter += 1
                        if counter > limit:
                            return
                        which_heads = heads[j]
                        
                        print("\t[+] These two close sequence tokens has strong activations:", a1, a2, f"at layer {layer_nr} head", which_heads)
                        print(f"\t\tToken at location {a1} -> {token_at_a1}")
                        print(f"\t\tToken at location {a2} -> {token_at_a2}")
                        
                        aa = sorted([a1, a2])
                        a1, a2 = aa[0]-5, aa[1]+5
                        a1 = 0 if a1 < 0 else a1
                        a2 = len(tokenized_input) if a2 > len(tokenized_input) else a2

                        vizString = f"attention_viz({a1}, {a2}, attentions, tokenized_input, layer={layer_nr}, heads=[{which_heads}])"
                        if visualize:
                            print(f"\t[!] Calling: {vizString}\n")
                            attention_viz(a1, a2, attentions, tokenized_input, layer=layer_nr, heads=[which_heads])
                        else:
                            print(f"\t[!] Visualization is disabled, but you can call it manually with: {vizString}\n")
            
            if "count" in types or "frequency" in types:
                # COUNTER CHECK
                print("[*] Performing a token frequency check ... ")
                c = attn_seq_2.tolist()
                c.extend((attn_seq_1.tolist()))
                c = Counter(c).most_common(most_common)        
                for token_location, token_frequency in c:
                    appear_in_heads = [heads[i] for i in np.where(attn_seq_1 == token_location)[0].tolist()]
                    appear_in_heads.extend([heads[i] for i in np.where(attn_seq_2 == token_location)[0].tolist()])
                    appear_in_heads = list(set(appear_in_heads))

                    token_value = tokenized_input[token_location]
                    msg1 = report_where_attends(attn_seq_1, attn_seq_2, token_location, tokenized_input)
                    msg2 = report_where_attends(attn_seq_2, attn_seq_2, token_location, tokenized_input)
                    if msg1 or msg2:
                        msg = f"\n\t> Token '{token_value}' location in sequence: {token_location}\n"
                        msg += f"\t  It appears {token_frequency} times, in layer {layer_nr}, heads: {appear_in_heads}\n"
                        msg += msg1 + msg2
                        print(msg)
                        
                        counter += 1
                        if counter > limit:
                            return
