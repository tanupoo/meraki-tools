#!/usr/bin/env python

from util import do_request
import json
import argparse
from os import environ

"""
ssid_switch.py -c config.json -k file:meraki-apikey.txt
"""

def put_ssid(network_id, ssid_number, data):
    api_epr = f"/networks/{network_id}/wireless/ssids/{ssid_number}"
    return do_request("PUT", api_epr, data)

def get_ssid(network_id, ssid_number):
    api_epr = f"/networks/{network_id}/wireless/ssids/{ssid_number}"
    return do_request("GET", api_epr)

def print_ssid_status(result):
    if result:
        state = "up" if result.get("enabled") == True else "down"
        print(f"{result.get('name')}: {state}")
    else:
        print(result)

def get_ssid_status(ssid_name, target):
    ret = get_ssid(target["network_id"], target["ssid_number"])
    print_ssid_status(ret)

def update_ssid_status(ssid_name, target, status):
    if status == "up":
        data = { "enabled": True }
    elif status == "down":
        data = { "enabled": False }
    else:
        raise RuntimeError
    ret = put_ssid(target["network_id"], target["ssid_number"], data)
    print_ssid_status(ret)

def set_required_values():
    # get the API key
    if opt.config is None:
        raise ValueError("config must be specified.")
    ssid_info = json.loads(open(opt.config).read())

    # get the API key
    if opt.api_key is None:
        raise ValueError("API key must be specified.")
    elif opt.api_key.startswith("key:"):
        api_key = opt.api_key[len("key:"):]
    elif opt.api_key.startswith("file:"):
        api_key = open(opt.api_key[len("file:"):]).read().strip()
    elif opt.api_key:
        api_key = open(opt.api_key).read().strip()
    environ["MERAKI_API_KEY"] = api_key

    return ssid_info

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
ap.add_argument("-c", "--config", action="store", dest="config",
                help=f"specify the config filename.")
opt = ap.parse_args()

if opt.show_all_status:
    ssid_info = set_required_values()
    for ssid,v in ssid_info.items():
        get_ssid_status(ssid, v)
elif opt.ssid:
    ssid_info = set_required_values()
    if opt.status:
        update_ssid_status(opt.ssid, ssid_info[opt.ssid], opt.status)
    else:
        get_ssid_status(ssid, ssid_info[opt.ssid])
else:
    ap.print_help()
