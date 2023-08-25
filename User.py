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
        credits_res = json.loads(self.api.credits())
        self.money = credits_res["credits"]
        # # market_list
        # tradepile_res = json.loads(self.api.tradepile())
        # self.market_list = tradepile_res["auctionInfo"]
        # players_list loop club
        self.player_list = {}
        self.club()

    def club(self):
        start = 0
        players = {}
        while True:
            res = json.loads(self.api.club(start=start, sortby="ovr"))  #value
            # tools.is_valid_json(res)
            player_res = res["itemData"]
            for player in res["itemData"]:
                players[player["id"]]=player
            if len(player_res) < 150:
                break
            start += 150
        self.player_list = players

    def buy(self, pack_id):
        res = self.api.purchased_items(purchased_type='buy', pack_id=pack_id)
        res = json.loads(res)
        return res["itemList"], res["duplicateItemIdList"]
        
    def open_pack(self, pack_id):
        res = self.api.purchased_items(purchased_type='open', pack_id=pack_id)
        res = json.loads(res)
        return res["itemList"], res["duplicateItemIdList"]

    # {"itemId":[143324285368,143324285370,143324285365]}
    def put(self, arr_items=None, misc_item_id=None):
        # 
        self.api.put_items(arr_items=arr_items, misc_item_id=misc_item_id)

    def sell(self, arr_items):
        sell_res = json.loads(self.api.delete_items(arr_items))
        self.money = sell_res["totalCredits"]

    def squad(self, sbc_id, arr_items):
        res1 = json.loads(self.api.squad_init_post(sbc_id=sbc_id))
        res2 = json.loads(self.api.squad_init_get(sbc_id=sbc_id))
        self.api.squad(sbc_id=sbc_id, arr_items=arr_items)
    
    def commit_suqad(self, sbc_id, arr_items):
        sell_res = json.loads(self.api.commit_suqad(sbc_id=sbc_id, arr_items=arr_items))
        list_pack_id = {}
        for val in sell_res['grantedSetAwards']:
            list_pack_id[val['value']] = val

        return list_pack_id
    
    def sbc3054(self, times):
        start=0
        start = 0
        while start<times:
            arr_items = []
            i = 0
            players = self.player_list
            for key, value in players.items():
                if value['rating'] < 65 and ('loans' not in value):
                    arr_items.append(key)
                    i+=1
                if 23 == i:
                    break
            
            if 11>i:
                print("not enough players for sbc2054.")
                break
            
            self.squad(sbc_id=3054, arr_items=arr_items)
            
            list_pack = self.commit_suqad(sbc_id=3054, arr_items=arr_items)
            for pack_id in list_pack.keys():
                items, duplicate_items = self.open_pack(pack_id=pack_id)
                self.handle_pack(items, duplicate_items)
            
            for id in arr_items:
                self.player_list.pop(id)
            start+=1
            print('open pack {} end'.format(start))
            print('*'*10)


    def aotobuypack(self, pack_id, times=5):
        start = 0
        while start<times:
            items, duplicate_items = self.buy(pack_id=pack_id)
            sef.handle_pack(items, duplicate_items)
            start+=1
            print('buy pack {} end'.format(start))
            print('*'*15)
            # sleep(2)

    def handle_pack(self, items, duplicate_items):
        arr_player = []
        list_player = {}
        list_other = {}
        if items is not None:
            for item in items:
                if "player" == item["itemType"]:
                    arr_player.append({"id":item["id"], "pile":"club"})
                    list_player[item["id"]]=item
                # elif "misc" == item["itemType"]:
                #     self.put(misc_item_id=item["id"])
                else:
                    list_other[item["id"]]=item

        list_dup_player = {}
        if duplicate_items is not None:
            # arr_dup_player = []
            for item in duplicate_items:
                if item["itemId"] in list_player:
                    list_dup_player[item["itemId"]]=list_player.pop(item["itemId"])
                    # arr_dup_player.append({"id":item.id, "pile":"trade"})

        if len(arr_player)>0:
            self.put(arr_player)
        if len(list_other)>0 or len(list_dup_player)>0:
            self.sell(list(list_other.keys())+list(list_dup_player.keys()))
            if len(list_dup_player)>0:
                print("{} duplicate players sold.".format(len(list_dup_player)))

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
