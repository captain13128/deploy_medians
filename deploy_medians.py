from utils import get_contract, approve_transaction, get_user_input_address


MEDIAN_ETHRUB_NAME = 'MedianETHRUB'
MEDIAN_BTCRUB_NAME = 'MedianBTCRUB'

median_eth_rub = get_contract(MEDIAN_ETHRUB_NAME)
median_btc_rub = get_contract(MEDIAN_BTCRUB_NAME)


def deploy_medians():
    tx = median_eth_rub.deploy(params={})
    approve_transaction(tx_hash=tx)
    print(f"tx deployed {MEDIAN_ETHRUB_NAME}: " + tx)
    get_user_input_address(tx, "MCD_MEDIAN_ETHRUB")

    tx = median_btc_rub.deploy(params={})
    approve_transaction(tx_hash=tx)
    print(f"tx deployed {MEDIAN_BTCRUB_NAME}: " + tx)
    get_user_input_address(tx, "MCD_MEDIAN_BTCRUB")


if __name__ == '__main__':
    deploy_medians()
