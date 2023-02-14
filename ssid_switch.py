from meraki_api import meraki_put_ssid, meraki_get_ssid
import json
from os import environ

def get_ssid_status(ssid_name, target):
    return meraki_get_ssid(target["network_id"], target["ssid_number"])

def update_ssid_status(ssid_name, target, status):
    if status == "up":
        data = { "enabled": True }
    elif status == "down":
        data = { "enabled": False }
    else:
        raise RuntimeError
    return meraki_put_ssid(target["network_id"], target["ssid_number"], data)

def set_conf_apikey(config: str, api_key_spec: str) -> dict:
    # read the config.
    ssid_info = json.loads(open(config).read())

    # get the API key.
    if api_key_spec.startswith("key:"):
        api_key = api_key_spec[len("key:"):]
    elif api_key_spec.startswith("file:"):
        api_key = open(api_key_spec[len("file:"):]).read().strip()
    elif api_key_spec:
        api_key = open(api_key_spec).read().strip()
    environ["MERAKI_API_KEY"] = api_key

    return ssid_info

