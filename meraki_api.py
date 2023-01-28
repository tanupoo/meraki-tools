import requests
import json

base_url = "https://api.meraki.com"
base_api = "{base_url}/api/v1".format(base_url=base_url)

def do_request(method: str,
               api_epr: str,
               data: str=None,
               debug: bool=False
               ) -> dict:
    # api_key
    api_key = environ.get("MERAKI_API_KEY")
    if api_key is None:
        raise ValueError("api_key must be specified.")
    # method
    if method == "GET":
        func = requests.get
    elif method == "PUT":
        func = requests.put
    else:
        raise ValueError(f"unknown method: {method}")
    # url and headers
    url = f"{base_api}/{api_epr}"
    headers = { "X-Cisco-Meraki-API-Key": f"{api_key}" }
    # payload
    payload = None
    if data:
        headers.update({"Content-Type": "application/json"})
        payload = json.dumps(data)
    if debug:
        print(method, url)
        print("--- header ---")
        print(headers)
        print("--- payload ---")
        print(payload)
    # request
    try:
        ret = func(url, headers=headers, data=payload)
        if not ret.ok:
            raise ValueError(f"{ret.status_code} {ret.reason}")
        ctype = ret.headers.get("content-type")
        if not ctype.startswith("application/json"):
            raise ValueError(f"the response is not JSON, but {ctype}")
        if debug:
            print("--- response ---")
            print(f"{ret.json()}")
            print("--- done ---")
        return ret.json()
    except Exception as e:
        if debug:
            print(f"ERROR: {e}")
            print(f"{ret.text}")
            print("--- done ---")
        return []

def meraki_put_ssid(network_id, ssid_number, data):
    api_epr = f"/networks/{network_id}/wireless/ssids/{ssid_number}"
    return do_request("PUT", api_epr, data)

def meraki_get_ssid(network_id, ssid_number):
    api_epr = f"/networks/{network_id}/wireless/ssids/{ssid_number}"
    return do_request("GET", api_epr)

