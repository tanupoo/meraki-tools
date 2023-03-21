#!/usr/bin/env python

import argparse
from meraki_api import *
import json

def get_conf(config: str) -> dict:
    return json.loads(open(config).read())

#
# main
#
ap = argparse.ArgumentParser()
ap.add_argument("--get-orgs", action="store_true", dest="get_orgs",
                help="specify to get a list of organizations.")
ap.add_argument("--get-networks", action="store_true", dest="get_networks",
                help="specify to get a list of networks.")
ap.add_argument("--get-ssids", action="store_true", dest="get_ssids",
                help="specify to get a list of SSIDs.")
ap.add_argument("--get-sensors", action="store_true", dest="get_sensors",
                help="specify to get a list of sensors.")
ap.add_argument("--org-id", "-O", action="store", dest="org_id",
                help="specify the network ID.")
ap.add_argument("--network-id", "-N", action="store", dest="network_id",
                help="specify the network ID.")
ap.add_argument("-k", "--apikey", action="store", dest="api_key",
                help=f"specify the API key with the prefix of either 'file:' or 'key:'.")
ap.add_argument("config",
                help=f"specify the config filename.")
opt = ap.parse_args()

config = get_conf(opt.config)
if opt.get_orgs:
    meraki_set_apikey(api_key_spec=opt.api_key, config=config)
    ret = meraki_get_all_orgs()
    for a in ret:
        print(f"## name:{a['name']} id:{a['id']}")
        print(a)
        print()
elif opt.get_networks:
    if opt.org_id:
        meraki_set_apikey(api_key_spec=opt.api_key, config=config)
        ret = meraki_get_all_networks(opt.org_id)
        for a in ret:
            print(f"## name:{a['name']} id:{a['id']}")
            print(a)
            print()
    else:
        print("ERROR: specify the network id")
        exit(1)
elif opt.get_ssids:
    if opt.network_id:
        meraki_set_apikey(api_key_spec=opt.api_key, config=config)
        ret = meraki_get_all_ssids(opt.network_id)
        for a in ret:
            print(f"## name:{a['name']} enabled:{a['enabled']}")
            print(a)
            print()
    else:
        print("ERROR: specify the network id")
        exit(1)
elif opt.get_ssids:
    if opt.network_id:
        meraki_set_apikey(api_key_spec=opt.api_key, config=config)
        ret = meraki_sensors_get_metric(opt.network_id)
        print(ret)
    else:
        print("ERROR: specify the network id")
        exit(1)
