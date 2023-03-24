import asyncio
import aiohttp
import json
from os import environ
from typing import Optional, List

base_url = "https://api.meraki.com"
base_api = "{base_url}/api/v1".format(base_url=base_url)

class meraki_asyncio_api:

    def __init__(self, loop=None):
        self.loop = loop
        self.api_key = None

    async def do_get(self, url, headers=None, data=None):
        async with aiohttp.ClientSession(loop=self.loop) as ses:
            async with ses.get(url,
                               headers=headers,
                               data=data,
                               ) as res:
                payload = await res.json()
                return res.ok, res.status, res.reason, res.headers, payload

    async def do_put(self, url, headers=None, data=None):
        async with aiohttp.ClientSession(loop=self.loop) as ses:
            async with ses.put(url,
                               header=headers,
                               data=data,
                               ) as res:
                payload = await res.json()
                return res.ok, res.status, res.reason, res.headers, payload

    async def _async_do(self,
                   method: str,
                   url: str,
                   headers: dict=None,
                   payload: str=None,
                   debug: bool=False
                   ) -> dict:
        # request
        if debug:
            print(method, url)
            print("--- header ---")
            print(headers)
            print("--- payload ---")
            print(payload)
        try:
            if method == "GET":
                ok, code, reason, headers, payload = await self.do_get(url, headers=headers)
            elif method == "PUT":
                ok, code, reason, headers, payload = await self.do_post(url, headers=headers, data=payload)
            else:
                raise ValueError(f"unknown method: {method}")
            if not ok:
                raise ValueError(f"{code} {reason}")
            ctype = headers.get("content-type")
            if not ctype.startswith("application/json"):
                raise ValueError(f"the response is not JSON, but {ctype}")
            if debug:
                print("--- response ---")
                print(f"{payload}")
                print("--- done ---")
            return payload
        except Exception as e:
            if debug:
                print(f"ERROR: {e}")
                print(f"{payload}")
                print("--- done ---")
            return []

    def do_request(self,
                   method: str,
                   api_epr: str,
                   data: dict=None,
                   debug: bool=False
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
        #
        if self.loop:
            pass
        else:
            self.loop = asyncio.new_event_loop()
            task = self.loop.create_task(self._async_do(method, url, headers, payload, debug))
            result = self.loop.run_until_complete(task)
            return result

    def get_all_orgs(self, debug=False) -> List:
        api_epr = f"/organizations"
        return self.do_request("GET", api_epr, debug=debug)

    def get_all_networks(self, org_id, debug=False):
        api_epr = f"/organizations/{org_id}/networks"
        return self.do_request("GET", api_epr, debug=debug)

    def get_all_ssids(self, network_id, debug=False):
        api_epr = f"/networks/{network_id}/wireless/ssids"
        return self.do_request("GET", api_epr, debug=debug)

    def put_ssid(self, network_id, ssid_number, data, debug=False):
        api_epr = f"/networks/{network_id}/wireless/ssids/{ssid_number}"
        return self.do_request("PUT", api_epr, data, debug=debug)

    def get_ssid(self, network_id, ssid_number, debug=False):
        api_epr = f"/networks/{network_id}/wireless/ssids/{ssid_number}"
        return self.do_request("GET", api_epr, debug=debug)

    def sensors_get_metric(self, network_id, debug=False):
        api_epr = f"/networks/{network_id}/sensor/alerts/current/overview/byMetric"
        return self.do_request("GET", api_epr, debug=debug)

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

