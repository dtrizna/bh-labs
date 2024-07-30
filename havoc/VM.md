# VM Configuration

Now: B2ms (2 CPU / 8 GB RAM)

NSG:

```json
{
    "name": "dmz-nsg",
    "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg",
    "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
    "type": "Microsoft.Network/networkSecurityGroups",
    "location": "eastus",
    "tags": {
        "zone": "dmz"
    },
    "properties": {
        "provisioningState": "Succeeded",
        "resourceGuid": "eb5e3943-3791-44e1-bff6-470804b8c12f",
        "securityRules": [
            {
                "name": "SSH",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/securityRules/SSH",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/securityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "protocol": "TCP",
                    "sourcePortRange": "*",
                    "destinationPortRange": "22",
                    "sourceAddressPrefix": "*",
                    "destinationAddressPrefix": "*",
                    "access": "Allow",
                    "priority": 300,
                    "direction": "Inbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            },
            {
                "name": "HTTPS",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/securityRules/HTTPS",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/securityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "protocol": "TCP",
                    "sourcePortRange": "*",
                    "destinationPortRange": "443",
                    "sourceAddressPrefix": "*",
                    "destinationAddressPrefix": "*",
                    "access": "Allow",
                    "priority": 320,
                    "direction": "Inbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            },
            {
                "name": "HTTP",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/securityRules/HTTP",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/securityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "protocol": "TCP",
                    "sourcePortRange": "*",
                    "destinationPortRange": "80",
                    "sourceAddressPrefix": "*",
                    "destinationAddressPrefix": "*",
                    "access": "Allow",
                    "priority": 340,
                    "direction": "Inbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            },
            {
                "name": "VNC-range",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/securityRules/VNC-range",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/securityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "5902-5912",
                    "sourceAddressPrefix": "*",
                    "destinationAddressPrefix": "*",
                    "access": "Allow",
                    "priority": 370,
                    "direction": "Inbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            },
            {
                "name": "HTTP-alt",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/securityRules/HTTP-alt",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/securityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "8080",
                    "sourceAddressPrefix": "*",
                    "destinationAddressPrefix": "*",
                    "access": "Allow",
                    "priority": 350,
                    "direction": "Inbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            }
        ],
        "defaultSecurityRules": [
            {
                "name": "AllowVnetInBound",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/defaultSecurityRules/AllowVnetInBound",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "description": "Allow inbound traffic from all VMs in VNET",
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "*",
                    "sourceAddressPrefix": "VirtualNetwork",
                    "destinationAddressPrefix": "VirtualNetwork",
                    "access": "Allow",
                    "priority": 65000,
                    "direction": "Inbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            },
            {
                "name": "AllowAzureLoadBalancerInBound",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/defaultSecurityRules/AllowAzureLoadBalancerInBound",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "description": "Allow inbound traffic from azure load balancer",
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "*",
                    "sourceAddressPrefix": "AzureLoadBalancer",
                    "destinationAddressPrefix": "*",
                    "access": "Allow",
                    "priority": 65001,
                    "direction": "Inbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            },
            {
                "name": "DenyAllInBound",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/defaultSecurityRules/DenyAllInBound",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "description": "Deny all inbound traffic",
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "*",
                    "sourceAddressPrefix": "*",
                    "destinationAddressPrefix": "*",
                    "access": "Deny",
                    "priority": 65500,
                    "direction": "Inbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            },
            {
                "name": "AllowVnetOutBound",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/defaultSecurityRules/AllowVnetOutBound",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "description": "Allow outbound traffic from all VMs to all VMs in VNET",
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "*",
                    "sourceAddressPrefix": "VirtualNetwork",
                    "destinationAddressPrefix": "VirtualNetwork",
                    "access": "Allow",
                    "priority": 65000,
                    "direction": "Outbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            },
            {
                "name": "AllowInternetOutBound",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/defaultSecurityRules/AllowInternetOutBound",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "description": "Allow outbound traffic from all VMs to Internet",
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "*",
                    "sourceAddressPrefix": "*",
                    "destinationAddressPrefix": "Internet",
                    "access": "Allow",
                    "priority": 65001,
                    "direction": "Outbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            },
            {
                "name": "DenyAllOutBound",
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkSecurityGroups/dmz-nsg/defaultSecurityRules/DenyAllOutBound",
                "etag": "W/\"f06e2de7-b122-4026-9db5-2b5b4f586a0a\"",
                "type": "Microsoft.Network/networkSecurityGroups/defaultSecurityRules",
                "properties": {
                    "provisioningState": "Succeeded",
                    "description": "Deny all outbound traffic",
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "*",
                    "sourceAddressPrefix": "*",
                    "destinationAddressPrefix": "*",
                    "access": "Deny",
                    "priority": 65500,
                    "direction": "Outbound",
                    "sourcePortRanges": [],
                    "destinationPortRanges": [],
                    "sourceAddressPrefixes": [],
                    "destinationAddressPrefixes": []
                }
            }
        ],
        "networkInterfaces": [
            {
                "id": "/subscriptions/1e359c34-9a91-49f9-b1b2-3263ed21c585/resourceGroups/PrivateLab/providers/Microsoft.Network/networkInterfaces/dmz130"
            }
        ]
    }
}
```
