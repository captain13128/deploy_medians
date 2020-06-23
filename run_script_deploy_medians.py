from deploy_medians import deploy_medians
from deploy_mega_poke import deploy_mega_poke

from add_relayer_to_median import add_relayer_to_medians
from change_src_in_osm import change_srces_in_osm


if __name__ == '__main__':
    deploy_medians()
    add_relayer_to_medians()
    change_srces_in_osm()

    deploy_mega_poke()
    print("Medians were successfully deployed")
