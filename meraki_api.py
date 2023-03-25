import requests
import json
from os import environ
from typing import Optional, List

base_url = "https://api.meraki.com"
base_api = "{base_url}/api/v1".format(base_url=base_url)

class meraki_api:

    def __init__(self, debug=False):
        self.api_key = None
        self.debug = debug

    def do_request(self,
                   method: str,
                   api_epr: str,
                   data: str=None
                   ) -> dict:
        if self.api_key is None:
            raise ValueError("api_key must be specified.")
        # url and headers
        url = f"{base_api}/{api_epr}"
        headers = { "X-Cisco-Meraki-API-Key": f"{self.api_key}" }
        # payload
        payload = None
        if data:
            headers.update({"Content-Type": "application/json"})
            payload = json.dumps(data)
        if self.debug:
            print(method, url)
            print("--- header ---")
            print(headers)
            print("--- payload ---")
            print(payload)
        # request
        try:
            if method == "GET":
                ret = requests.get(url, headers=headers)
            elif method == "PUT":
                ret = requests.put(url, headers=headers, data=payload)
            else:
                raise ValueError(f"unknown method: {method}")
            if not ret.ok:
                raise ValueError(f"{ret.status_code} {ret.reason}")
            ctype = ret.headers.get("content-type")
            if not ctype.startswith("application/json"):
                raise ValueError(f"the response is not JSON, but {ctype}")
            if self.debug:
                print("--- response ---")
                print(f"{ret.json()}")
                print("--- done ---")
            return ret.json()
        except Exception as e:
            if self.debug:
                print(f"ERROR: {e}")
                print(f"{ret.text}")
                print("--- done ---")
            return []

    def get_all_orgs(self) -> List:
        api_epr = f"/organizations"
        return self.do_request("GET", api_epr)

    def get_all_networks(self, org_id):
        api_epr = f"/organizations/{org_id}/networks"
        return self.do_request("GET", api_epr)

    def get_all_ssids(self, network_id):
        api_epr = f"/networks/{network_id}/wireless/ssids"
        return self.do_request("GET", api_epr)

    def put_ssid(self, network_id, ssid_number, data):
        api_epr = f"/networks/{network_id}/wireless/ssids/{ssid_number}"
        return self.do_request("PUT", api_epr, data)

    def get_ssid(self, network_id, ssid_number):
        api_epr = f"/networks/{network_id}/wireless/ssids/{ssid_number}"
        return self.do_request("GET", api_epr)

    def sensors_get_metric(self, network_id):
        api_epr = f"/networks/{network_id}/sensor/alerts/current/overview/byMetric"
        return self.do_request("GET", api_epr)

    def set_apikey(self,
            api_key_spec: str=None,
            config_api_key_spec: str=None
            ) -> None:
        """
        Priority:
            1. api_key_spec
            2. environmental variable
            3. config_api_key_spec
        """
        def set_apikey(spec):
            if spec.startswith("key:"):
                self.api_key = spec[len("key:"):]
            elif spec.startswith("file:"):
                self.api_key = open(spec[len("file:"):]).read().strip()
            else:
                self.api_key = spec
        # get the API key.
        if api_key_spec:
            set_apikey(api_key_spec)
        else:
            if environ.get("MERAKI_API_KEY"):
                set_apikey(environ.get("MERAKI_API_KEY"))
            else: 
                if config_api_key_spec:
                    set_apikey(config_api_key_spec)
                else:
                    raise ValueError("ERROR: APIKEY must be set.")
