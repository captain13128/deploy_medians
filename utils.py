import json
import os
import logging

import web3

from contract import Contract
from settings import ACCOUNT, ACCOUNT_PRIVATE_KEY, RPC_URL, ABI_DIR, BIN_DIR, DSS_ADDRESSES, CONFIG_DIR, PHRASE

logger = logging.getLogger("approve_transaction")


def get_contract(contract_name: str) -> Contract:
    return Contract(
        account=ACCOUNT,
        private_key=ACCOUNT_PRIVATE_KEY,
        contract_name=contract_name,
        abi_file=os.path.join(ABI_DIR, f"{contract_name}.json"),
        bytecode_file=os.path.join(BIN_DIR, f"{contract_name}.bin"),
        rpc_url=RPC_URL
    )


def str_to_bytes32(string):
    hex_data = web3.Web3.toHex(text=string)
    res = hex_data.lstrip("0x")
    zero_count = 64 - len(res)

    if zero_count >= 0:
        return "0x" + res + "0" * zero_count
    else:
        raise


def convert_int_to_bytes32(value: int):
    res = hex(value)
    res = res.lstrip("0x")
    zero_count = 64 - len(res)

    if zero_count >= 0:
        return "0x" + "0" * zero_count + res
    else:
        raise


def confirm_transaction(tx_hash: str or hex):
    def approve():
        try:
            return web3.Web3(web3.HTTPProvider(RPC_URL)).eth.getTransactionReceipt(tx_hash)
        except Exception as e:
            return None

    finish = False
    while not finish:
        transaction = approve()
        if transaction is None:
            continue
        elif transaction['status'] != 1:
            logger.info(f"transaction ({tx_hash}) failed")
            print(f"transaction ({tx_hash}) failed")
            raise
        else:
            finish = True

    logger.info(f"transaction ({tx_hash}) is confirmed")
    print(f"transaction ({tx_hash}) is confirmed")
    return transaction


def approve_transaction(tx_hash: str or hex, description: str = "transaction sending ...", transaction_details=None):
    try:
        logger.info(f"{description} {tx_hash}")
        print(f"{description} {tx_hash}")
        confirm_transaction(tx_hash)
    except Exception as e:
        logger.error(e)
        print(e)
        if transaction_details:
            logger.debug(transaction_details)
            print(transaction_details)
        raise


def write_config(name: str, value: str):
    DSS_ADDRESSES.update({name: value})

    with open(CONFIG_DIR, 'w') as dss_addresses:
        dss_addresses.write(json.dumps(DSS_ADDRESSES))
    return True


def get_user_input_address(tx: str, address_name: str):
    is_valid_address = False
    while not is_valid_address:
        try:
            address = web3.Web3.toChecksumAddress(input(PHRASE.format(transaction=tx)))
            is_valid_address = True
        except ValueError:
            print("Address is not valid")
    write_config(name=address_name, value=address)
    return address
