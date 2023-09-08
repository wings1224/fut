import json
import time
import requests
import config

class ApiInterface:


    def __init__(self, base_url, sid = config.G_SID):
        self.base_url = base_url
        self.sid = sid

    def send_request(self, endpoint, method="GET", data=None, params=None, headers=config.G_HEADERS):
        # time.sleep(1)
        retries = 0
        while retries < 3:
            try:
                url = self.base_url + endpoint
                payload = json.dumps(data)
                headers["X-UT-SID"] = self.sid
                response = requests.request(
                    method, url, data=payload, params=params, headers=headers)
                # time.sleep(1)
                response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)

                # HTTP status code 200 (OK)
                if response.status_code == requests.codes.ok:
                    return response.text
                else:
                    print(f"Request succeeded with status code {response.status_code}, but response content might be unexpected.")
                    return config.E_CLIENT_ERROR
            except requests.exceptions.HTTPError as e:
                print("HTTPError Request failed:", e)
                code = e.response.status_code
                if code in [401, 403, 410]:
                    return config.E_CLIENT_ERROR
                if code in [471]:
                    return config.E_CLIENT_ERROR_471

                print(f"HTTPError Retrying in 3 seconds...")
                time.sleep(2)
                retries += 1
            except requests.exceptions.RequestException as e:
                print("Request failed:", e)
                print(f"Retrying in 3 seconds...")
                time.sleep(2)
                retries += 1
        
        print(f"Failed to fetch data from {url} after 3 retries.")
        return config.E_NETWORK_ERROR
    
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

    def sold(self):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/trade/sold"
        
        return self.send_request(endpoint,method="DELETE")

    def re_list(self):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/auctionhouse/relist"
        
        return self.send_request(endpoint,method="PUT")

    def auctionhouse(self, startingBid=None, buyNowPrice=None, duration=3600, id=None):
        if startingBid is None or buyNowPrice is None or id is None:
            return False
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/auctionhouse"
        payload = {"buyNowPrice":buyNowPrice,"duration":duration,"itemData":{"id":id},"startingBid":startingBid}
        return self.send_request(endpoint, "POST", payload)
    
    def transfermarket(self, minb):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/transfermarket"
        params = 'num=21&start=0&type=player&definitionId=50545748&minb={}'.format(minb)
        return self.send_request(endpoint, "GET", params=params)


    def club(self, count=150, sort="asc", sortby="value", start=0, type="player"):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/club"
        payload = {"count":count,"sort":sort,"sortBy":sortby,"start":start,"type":type}
        return self.send_request(endpoint, "POST", payload)
    
    def squad_init_get(self, sbc_id=None):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/sbs/challenge/{}/squad".format(sbc_id)
        return self.send_request(endpoint, "GET")

    def squad_init_post(self, sbc_id=None):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/sbs/challenge/{}".format(sbc_id)
        return self.send_request(endpoint, "POST")

    def squad(self, sbc_id, arr_items):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/sbs/challenge/{}/squad".format(sbc_id)
        payload = {"players":[]}
        for index, value in enumerate(arr_items):
            # print("Index:", index, "Value:", value)
            if 3340 == sbc_id and 9 == index:
                payload["players"].append({"index":index,"itemData":{"id":0,"dream":"false"}})
                continue
            if sbc_id in [3503, 3500] and index not in [0,2,3] :
                payload["players"].append({"index":index,"itemData":{"id":0,"dream":"false"}})
                continue
            payload["players"].append({"index":index,"itemData":{"id":value,"dream":"false"}})

        return self.send_request(endpoint, "PUT", payload)

    def commit_suqad(self, sbc_id, arr_items):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/sbs/challenge/{}?skipUserSquadValidation=false".format(sbc_id)
        payload = {"players":[]}
        for index, value in enumerate(arr_items):
            # print("Index:", index, "Value:", value)
            if 3340 == sbc_id and 9 == index:
                payload["players"].append({"index":index,"itemData":{"id":0,"dream":"false"}})
                continue
            if sbc_id in [3503, 3500] and index not in [0,2,3] :
                payload["players"].append({"index":index,"itemData":{"id":0,"dream":"false"}})
                continue
            payload["players"].append({"index":index,"itemData":{"id":value,"dream":"false"}})

        return self.send_request(endpoint, "PUT", payload)


    # buy or check item
    # if pack_id is not null, post with payload like {"currency":"COINS", packId} to buy the pack item
    # else to get check the pack item you bought
    # return json {"itemData":[], "duplicateItemIdList":[]}
    def purchased_items(self, purchased_type=None, pack_id=None, currency="COINS"):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/purchased/items"        
        if "buy" == purchased_type:
            payload = {
                "currency": currency,
                "packId": pack_id
            }
            return self.send_request(endpoint, "POST", payload)
        elif "open" == purchased_type:
            payload = {"packId":pack_id,"untradeable":"true","usePreOrder":"true"}
            return self.send_request(endpoint, "POST", payload)
        else:
            return self.send_request(endpoint, "GET")

    def put_items(self, arr_items=None, misc_item_id=None):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
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
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "delete/game/fifa23/item"
        payload = {
            "itemId": arr_items
        }
        return self.send_request(endpoint, "POST", payload)

    def playerpicks(self, id):
        # self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/playerpicks/item/{}/select".format(id)
        return self.send_request(endpoint, "POST")


from time import sleep

if __name__ == "__main__":
    # 创建 API 接口实例
    api = ApiInterface("https://utas.mob.v1.fut.ea.com/ut/", config.G_SID)
    times = 0
    while True:
        times+=1
        print(times)
        api.transfermarket(minb=200+100*times)
        sleep(1)
