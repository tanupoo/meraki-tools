#!/usr/bin/env python

import argparse
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
ap.add_argument("--no-async", action="store_true", dest="non_async",
                help=f"specify not to use asyncio")
ap.add_argument("-d", action="store_true", dest="debug",
                help=f"enable debug mode")
ap.add_argument("config",
                help=f"specify the config filename.")
opt = ap.parse_args()

config = get_conf(opt.config)

if opt.non_async:
    from meraki_api import meraki_api
else:
    from meraki_asyncio_api import meraki_asyncio_api as meraki_api

meraki = meraki_api(debug=opt.debug)
meraki.set_apikey(api_key_spec=opt.api_key,
                  config_api_key_spec=config["api_key_spec"])

if opt.get_orgs:
    ret = meraki.get_all_orgs(debug=opt.debug)
    for a in ret:
        print(f"## name:{a['name']} id:{a['id']}")
        print(a)
        print()
elif opt.get_networks:
    if opt.org_id:
        ret = meraki.get_all_networks(opt.org_id, debug=opt.debug)
        for a in ret:
            print(f"## name:{a['name']} id:{a['id']}")
            print(a)
            print()
    else:
        print("ERROR: specify the network id")
        exit(1)
elif opt.get_ssids:
    if opt.network_id:
        ret = meraki.get_all_ssids(opt.network_id, debug=opt.debug)
        for a in ret:
            print(f"## name:{a['name']} enabled:{a['enabled']}")
            print(a)
            print()
    else:
        print("ERROR: specify the network id")
        exit(1)
elif opt.get_sensors:
    if opt.network_id:
        ret = meraki.sensors_get_metric(opt.network_id, debug=opt.debug)
        print(ret)
    else:
        print("ERROR: specify the network id")
        exit(1)
