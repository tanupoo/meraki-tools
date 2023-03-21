#!/usr/bin/env python

import argparse
from meraki_api import meraki_put_ssid, meraki_get_ssid, meraki_set_apikey
import json

"""
ssid_man.py config.json -k file:meraki-apikey.txt
"""

def get_conf(config: str) -> dict:
    return json.loads(open(config).read())

def get_ssid_spec(ssid_list, ssid_name):
    for x in ssid_list:
        if x["ssid_name"] == ssid_name:
            return x
    else:
        print(f"ERROR: unknown SSID: {ssid_name}")
        exit(1)

def print_ssid_status(result):
    if result:
        state = "up" if result.get("enabled") == True else "down"
        print(f"{result.get('name')}: {state}")
    else:
        print(result)

#
# main
#
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--ssid", action="store", dest="ssid",
                help="specify a SSID.")
ap.add_argument("-u", "--update-status", action="store", dest="status",
                choices=["up", "down"],
                help="disable SSID specified.")
ap.add_argument("-a", "--show-all-status", action="store_true", dest="show_all_status",
                help=f"show current status of all APs")
ap.add_argument("-k", "--apikey", action="store", dest="api_key",
                help=f"specify the API key with the prefix of either 'file:' or 'key:'.")
ap.add_argument("config",
                help=f"specify the config filename.")
opt = ap.parse_args()

config = get_conf(opt.config)
ssid_list = config.get("ssid_list")
if ssid_list is None:
    print("ERROR: ssid_list must be defined.")
    exit(1)

if opt.show_all_status:
    meraki_set_apikey(api_key_spec=opt.api_key,
                      config_api_key_spec=config.get("api_key_spec"))
    for x in ssid_list:
        ret = meraki_get_ssid(x["network_id"], x["ssid_number"])
        print_ssid_status(ret)
elif opt.ssid:
    meraki_set_apikey(api_key_spec=opt.api_key,
                      config_api_key_spec=config.get("api_key_spec"))
    ssid_spec = get_ssid_spec(ssid_list, opt.ssid)
    if opt.status:
        if opt.status == "up":
            data = { "enabled": True }
        elif opt.status == "down":
            data = { "enabled": False }
        else:
            raise RuntimeError
        ret = meraki_put_ssid(ssid_spec["network_id"], ssid_spec["ssid_number"], data)
        print(f"enabled: {ret.get('enabled')}")
    else:
        ret = meraki_get_ssid(ssid_spec["network_id"], ssid_spec["ssid_number"])
        print_ssid_status(ret)
else:
    ap.print_help()

