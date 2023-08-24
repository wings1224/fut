import json
from ApiInterface import ApiInterface
import config
import tools

class User:
    def __init__(self, sid=config.G_SID, api=None, money=None, players_list=None, market_list=None):
        self.sid = sid
        self.api = result = api if api is not None else ApiInterface(
            "https://utas.mob.v1.fut.ea.com/ut/", sid)
        # init accountinfo
        # money
        # credits_res = json.loads(self.api.credits())
        # self.money = credits_res["credits"]
        # # market_list
        # tradepile_res = json.loads(self.api.tradepile())
        # self.market_list = tradepile_res["auctionInfo"]
        # # players_list loop club
        # self.player_list = {}
        # self.club()

    def club(self):
        start = 0
        while True:
            res = json.loads(self.api.club(start=start, sortby="rating"))
            # tools.is_valid_json(res)
            player_res = res["itemData"]
            for player in res["itemData"]:
                self.player_list[player["id"]]=player
            if len(player_res) < 90:
                break
            start += 90

    def buy(self, pack_id):
        res = self.api.purchased_items(pack_id)
        res = json.loads(res)
        return res["itemList"], res["duplicateItemIdList"]

    # {"itemId":[143324285368,143324285370,143324285365]}
    def put(self, arr_items=None, misc_item_id=None):
        # 
        self.api.put_items(arr_items=arr_items, misc_item_id=misc_item_id)

    def sell(self, arr_items):
        sell_res = json.loads(self.api.delete_items(arr_items))
        self.money = sell_res["totalCredits"]
        

    def query(self):
        print("money:", self.money)
        print("player_list:", self.player_list)
        print("market_list:", self.market_list)


if __name__ == "__main__":
    # 创建一个用户实例
    user1 = User(money=100, players_list=["item1", "item2"], market_list={
                 "item3": 50, "item4": 30})

    # 进行操作示例
    user1.query()
    user1.buy("item3")
    user1.put("item1", 70)
    user1.sell("item2")
    user1.query()
