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
            headers.setdefault("X-UT-SID", sid)
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

    def purchased_items(self, pack_id, currency="COINS"):
        self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/purchased/items"
        payload = {
            "currency": currency,
            "packId": pack_id
        }
        return send_request(endpoint, "POST", payload)

    def put_items(self, arr_items):
        self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "game/fifa23/item"
        payload = {
            "itemData": arr_items
        }
        return send_request(endpoint, "POST", payload)

    def delete_items(self, arr_items):
        self.base_url = 'https://utas.mob.v1.fut.ea.com/ut/'
        endpoint = "delete/game/fifa23/item"
        payload = {
            "itemId": arr_items
        }
        return send_request(endpoint, "POST", payload)


if __name__ == "__main__":
    # 创建 API 接口实例
    api = ApiInterface(base_url="https://api.example.com")
