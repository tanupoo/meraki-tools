#!/usr/bin/env python

import argparse
from ssid_switch import get_ssid_status, update_ssid_status, set_conf_apikey

"""
ssid_man.py config.json -k file:meraki-apikey.txt
"""

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

if opt.api_key is None:
    raise ValueError("api key must be specified.")
if opt.show_all_status:
    ssid_info = set_conf_apikey(opt.config, opt.api_key)
    for ssid,v in ssid_info.items():
        ret = get_ssid_status(ssid, v)
        print_ssid_status(ret)
elif opt.ssid:
    ssid_info = set_conf_apikey(opt.config, opt.api_key)
    if opt.status:
        ret = update_ssid_status(opt.ssid, ssid_info[opt.ssid], opt.status)
    else:
        ret = get_ssid_status(ssid, ssid_info[opt.ssid])
        print_ssid_status(ret)
else:
    ap.print_help()
