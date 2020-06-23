from settings import DSS_ADDRESSES
from utils import get_contract, approve_transaction, get_user_input_address

CONTRACT_NAME = 'MegaPoker'
mega_poker = get_contract(CONTRACT_NAME)


def deploy_mega_poke():
    tx = mega_poker.deploy(
        params={
            "kwargs": {
                "eth_osm_address": DSS_ADDRESSES['PIP_ETH'],
                "wbtc_osm_address": DSS_ADDRESSES['PIP_WBTC'],
                "pot_address": DSS_ADDRESSES['MCD_POT'],
                "jug_address": DSS_ADDRESSES['MCD_JUG'],
                "spot_address": DSS_ADDRESSES['MCD_SPOT']
            }
        }
    )
    approve_transaction(tx)
    get_user_input_address(tx, "MCD_MEGA_POKER")


if __name__ == '__main__':
    deploy_mega_poke()
