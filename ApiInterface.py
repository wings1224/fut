import json
import requests
import config

class ApiInterface:


    def __init__(self, base_url, sid = config.G_SID):
        self.base_url = base_url
        self.sid = sid

    def send_request(self, endpoint, method="GET", data=None, params=None, headers=config.G_HEADERS):
        try:
            url = self.base_url + endpoint
            payload = json.dumps(data)
            headers["X-UT-SID"] = self.sid
            response = requests.request(
                method, url, data=payload, params=params, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)

            # HTTP status code 200 (OK)
            if response.status_code == requests.codes.ok:
                return response.text
            else:
                print(f"Request succeeded with status code {response.status_code}, but response content might be unexpected.")
                return None
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            return None
    
    def usermassinfo(self):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/usermassinfo"
        return self.send_request(endpoint)
    
    def credits(self):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/user/credits"
        return self.send_request(endpoint)
        
    def tradepile(self):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/tradepile"
        return self.send_request(endpoint)

    def club(self, count=90, sort="asc", sortby="value", start=0, type="player"):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/club"
        payload = {"count":count,"sort":sort,"sortBy":sortby,"start":start,"type":type}
        return self.send_request(endpoint, "POST", payload)

    # buy or check item
    # if pack_id is not null, post with payload like {"currency":"COINS", packId} to buy the pack item
    # else to get check the pack item you bought
    # return json {"itemData":[], "duplicateItemIdList":[]}
    def purchased_items(self, pack_id=None, currency="COINS"):
        self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/purchased/items"
        payload = {
            "currency": currency,
            "packId": pack_id
        }
        if pack_id is not None:
            return self.send_request(endpoint, "POST", payload)
        else:
            return self.send_request(endpoint, "GET")

    def put_items(self, arr_items=None, misc_item_id=None):
        self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/item"
        
        if misc_item_id is not None:
            payload = {"apply":[]}
            return self.send_request(endpoint+'/'+str(misc_item_id), "POST")
        else:
            payload = {
                "itemData": arr_items
            }
            return self.send_request(endpoint, "PUT", payload)

    def delete_items(self, arr_items):
        self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "delete/game/fifa23/item"
        payload = {
            "itemId": arr_items
        }
        return self.send_request(endpoint, "POST", payload)


if __name__ == "__main__":
    # 创建 API 接口实例
    api = ApiInterface(base_url="https://api.example.com")
