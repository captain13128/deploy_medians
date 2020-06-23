import os
import json

NETWORK = "kovan"
# NETWORK = "mainnet"


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "addresses", f"{NETWORK.lower()}_addresses.json")
ABI_DIR = os.path.join(BASE_DIR, "abi")
BIN_DIR = os.path.join(BASE_DIR, "bin")

with open(CONFIG_DIR, 'r') as dss_addresses:
    DSS_ADDRESSES = json.loads(dss_addresses.read())

if NETWORK.upper() == "MAINNET":
    # MAIN

    ACCOUNT = "0x69B18942F19B7c3aF37647e6b05CF861BD14f2Ec"
    ACCOUNT_PRIVATE_KEY = ""
    RPC_URL = "https://mainnet.infura.io/v3/****"

    MEDIAN_ETHRUB_TX_SIGNER = "0xf077aeD04CA0ffD31a67dbc6bE9a21D844924f0C"
    MEDIAN_BTCRUB_TX_SIGNER = "0xf077aeD04CA0ffD31a67dbc6bE9a21D844924f0C"

    PHRASE = "Please enter the address of the contract that was deployed " \
             "in this transaction https://etherscan.io/tx/{transaction} \n"

elif NETWORK.upper() == "KOVAN":
    # KOVAN

    ACCOUNT = "0xC0CCab7430aEc0C30E76e1dA596263C3bdD82932"
    ACCOUNT_PRIVATE_KEY = ""
    RPC_URL = "https://kovan.infura.io/v3/****"

    MEDIAN_ETHRUB_TX_SIGNER = ACCOUNT
    MEDIAN_BTCRUB_TX_SIGNER = ACCOUNT

    PHRASE = "Please enter the address of the contract that was deployed " \
             "in this transaction https://kovan.etherscan.io/tx/{transaction} \n"

else:
    raise Exception('NOT SUPPORTED NETWORK')
