from settings import  MEDIAN_ETHRUB_TX_SIGNER, MEDIAN_BTCRUB_TX_SIGNER, DSS_ADDRESSES
from utils import get_contract, approve_transaction


def add_relayer_to_median_ethrub(contract_name: str, median_address: str, pip_address: str, signer_address: str):
    median = get_contract(contract_name)

    tx = median.call_payable_method(contract_address=median_address, method_name="lift",
                                    params={"kwargs": {"a": [signer_address]}}, gas=3000000)

    approve_transaction(tx)
    print(f"Add relayer ({signer_address}) to median ({median_address}): " + tx)

    tx = median.call_payable_method(contract_address=median_address, method_name="kiss",
                                    params={"kwargs": {"a": pip_address}}, gas=3000000)

    approve_transaction(tx)
    print(f"Add OSM ({pip_address}) to median ({median_address}): " + tx)


def add_relayer_to_medians():
    add_relayer_to_median_ethrub('MedianETHRUB', DSS_ADDRESSES["MCD_MEDIAN_ETHRUB"],
                                 DSS_ADDRESSES["PIP_ETH"], MEDIAN_ETHRUB_TX_SIGNER)

    add_relayer_to_median_ethrub('MedianBTCRUB', DSS_ADDRESSES["MCD_MEDIAN_BTCRUB"],
                                 DSS_ADDRESSES["PIP_WBTC"], MEDIAN_BTCRUB_TX_SIGNER)


if __name__ == '__main__':
    add_relayer_to_medians()
