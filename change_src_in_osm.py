from settings import DSS_ADDRESSES
from utils import get_contract, approve_transaction


osm = get_contract('OSM')


def change_src_in_osm(osm_address, median_address):
    tx = osm.call_payable_method(contract_address=osm_address,
                                 method_name="change",
                                 gas=300000,
                                 params={
                                     "kwargs": {
                                         "src_": median_address
                                     }
                                 })
    approve_transaction(tx)
    print(f"tx change src on  {median_address} ({osm_address}): " + tx)


def change_srces_in_osm():
    change_src_in_osm(DSS_ADDRESSES['PIP_ETH'], DSS_ADDRESSES['MCD_MEDIAN_ETHRUB'])
    change_src_in_osm(DSS_ADDRESSES['PIP_WBTC'], DSS_ADDRESSES['MCD_MEDIAN_BTCRUB'])


if __name__ == '__main__':
    change_srces_in_osm()
