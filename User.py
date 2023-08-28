import json
from ApiInterface import ApiInterface
import config
import tools


class User:
    def __init__(self, sid=config.G_SID, api=None, money=None, players_list=None, market_list=None):
        self.sid = sid
        self.api = result = api if api is not None else ApiInterface(
            "https://utas.mob.v1.fut.ea.com/ut/", sid)
        self.cfg_sbc = {
            3054: {"player_total_numbers": 22, "player_numbers": 11, "sortby": "ovr", "sort": "asc", "min_ovr": 0, "max_ovr": 64}
            , 3056: {"player_total_numbers": 22, "player_numbers": 11, "sortby": "ovr", "sort": "asc", "min_ovr": 65, "max_ovr": 74}
            , 3263: {"player_total_numbers": 22, "player_numbers": 11, "sortby": "ovr", "sort": "asc", "min_ovr": 75, "max_ovr": 82, "common_player_numbers":11, "rare_player_numbers":0}
            , 3394: {"player_total_numbers": 22, "player_numbers": 11, "sortby": "ovr", "sort": "asc", "min_ovr": 75, "max_ovr": 82, "common_player_numbers":6, "rare_player_numbers":5}
        }
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

        self.check_pruchsed_items()

    def check_pruchsed_items(self):
        res = self.api.purchased_items()
        if False == tools.is_valid_json(res):
            print('get items failed! err: {}'.format(res))
        res = json.loads(res)
        items = res["itemData"]
        duplicate_items = None
        if "duplicateItemIdList" in res:
            duplicate_items = res['duplicateItemIdList']

        # high value player pause
        if duplicate_items is not None:
            for dup_item in duplicate_items:
                dup_item_id = dup_item["itemId"]
                for item in items:
                    if "player" == item["itemType"] and True == item['untradeable'] and item["rareflag"] not in [0, 1] and item["rating"]>88 and dup_item_id == item["id"]:
                        print('high value player(rareflag:{}, rating:{}).'.format(item["rareflag"], item["rating"]))
                        exit(1)
        self.handle_pack(items, duplicate_items)

    def club(self):
        start = 0
        players = {}
        while True:
            res = self.api.club(start=start, sortby="ovr")  # value
            if tools.is_valid_json(res):
                res = json.loads(res)
            else:
                print("get player list failed!")
                break
            # tools.is_valid_json(res)
            player_res = res["itemData"]
            for player in res["itemData"]:
                players[player["id"]] = player
            if len(player_res) < 150:
                break
            start += 150
        self.player_list = players
        with open('player_list.json', 'w') as file:
            file.write(json.dumps(self.player_list))

    def buy(self, pack_id):
        res = self.api.purchased_items(purchased_type='buy', pack_id=pack_id)
        if config.E_CLIENT_ERROR_471 == res:
            res = self.api.purchased_items()
            if False == tools.is_valid_json(res):
                return False
        if False == tools.is_valid_json(res):
            return False
            
        return res

    def open_pack(self, pack_id):
        res = self.api.purchased_items(purchased_type='open', pack_id=pack_id)
        if False == tools.is_valid_json(res):
            return res
        res = json.loads(res)
        return res

    # {"itemId":[143324285368,143324285370,143324285365]}
    def put(self, arr_items=None, misc_item_id=None):
        res = self.api.put_items(arr_items=arr_items, misc_item_id=misc_item_id)
        if False == tools.is_valid_json(res):
            return False
        res = json.loads(res)
        # '{"itemData":[{"id":147766805837,"reason":"Duplicate Item Type","pile":"club","success":false,"errorCode":472},{"id":147766805835,"reason":"Duplicate Item Type","pile":"club","success":false,"errorCode":472}]}'
        for item in res['itemData']:
            if False == item['success']:
                print('put item failed. err: {}'.format(item['reason']))
                return False
        return res

    def sell(self, arr_items):
        res = self.api.delete_items(arr_items)
        if tools.is_valid_json(res):
            sell_res = json.loads(res)
            self.money = sell_res["totalCredits"]
            return sell_res
        else:
            return res
        

    def squad(self, sbc_id, arr_items):
        self.api.squad_init_get(sbc_id=sbc_id)
        return self.api.squad(sbc_id=sbc_id, arr_items=arr_items)

    def commit_suqad(self, sbc_id, arr_items):
        res = self.api.commit_suqad(sbc_id=sbc_id, arr_items=arr_items)
        if tools.is_valid_json(res):
            res = json.loads(res)
        else:
            return res
        
        list_pack_id = {}
        for val in res['grantedSetAwards']:
            list_pack_id[val['value']] = val

        return list_pack_id
    # {"player_total_numbers":22, "player_numbers": 11, "sortby": "ovr","sort": "asc", "min_ovr": 0, "max_ovr": 64, "rare_numbers": 0}

    def pick(self):
        res = self.api.purchased_items()
        if False == tools.is_valid_json(res):
            return res
        res = json.loads(res)
        for item in res["itemData"]:
            if 'misc' != item['itemType']:
                continue
            open_res = self.api.put_items(misc_item_id=item['id'])
            if False==tools.is_valid_json(open_res):
                print("pick player open items failed.")
                return open_res
            max_rating_player = max(open_res["itemData"], key=lambda player: player['value'])
            player_res = self.api.playerpicks(max_rating_player['assetId'])
            if False == tools.is_valid_json(player_res):
                print("pick player failed.")
                return player_res
            player = json.loads(player_res)
            print("pick player(rating:{}, rareflag:{})".format(player['rating'], player['rareflag']))
            

    def sbc(self, times, sbc_id, need_open=True):
        start = 0
        while start < times:
            arr_items = []
            i = 0
            common_player_numbers = 0
            rare_player_numbers = 0
            players = self.player_list
            for key, value in players.items():
                if value['rating'] <= self.cfg_sbc[sbc_id]['max_ovr'] and value['rating'] >= self.cfg_sbc[sbc_id]['min_ovr'] and ('loans' not in value):
                    # handle rare numbers
                    if "common_player_numbers" in self.cfg_sbc[sbc_id] and common_player_numbers < self.cfg_sbc[sbc_id]['common_player_numbers'] and 0 == value['rareflag']:
                        arr_items.append(key)
                        i += 1
                        common_player_numbers+=1
                        if self.cfg_sbc[sbc_id]['player_total_numbers'] < i:
                            break

                    if "rare_player_numbers" in self.cfg_sbc[sbc_id] and rare_player_numbers < self.cfg_sbc[sbc_id]['rare_player_numbers'] and 1 == value['rareflag']:
                        arr_items.append(key)
                        i += 1
                        rare_player_numbers+=1
                        if self.cfg_sbc[sbc_id]['player_total_numbers'] < i:
                            break

                    if "common_player_numbers" not in self.cfg_sbc[sbc_id] and "rare_player_numbers" not in self.cfg_sbc[sbc_id]:
                        arr_items.append(key)
                        i += 1
                        rare_player_numbers+=1
                        if self.cfg_sbc[sbc_id]['player_total_numbers'] < i:
                            break
                

            if self.cfg_sbc[sbc_id]['player_numbers'] > i:
                print("not enough players for sbc {}.".format(sbc_id))
                break

            self.api.squad_init_post(sbc_id=sbc_id)
            self.squad(sbc_id=sbc_id, arr_items=arr_items)

            ret = self.commit_suqad(sbc_id=sbc_id, arr_items=arr_items)
            if config.E_NETWORK_ERROR == ret:
                continue
            if config.E_CLIENT_ERROR == ret:
                continue
            list_pack = ret
            print('sbc {} No.{}.'.format(sbc_id, start+1))

            # if 3394 == sbc_id:
            #     self.pick()
            #     continue

            if need_open :
                for pack_id in list_pack.keys():
                    res = self.open_pack(pack_id=pack_id)
                    if False == tools.is_valid_json(res):
                        if config.E_CLIENT_ERROR_471 == res:
                            res = self.api.purchased_items()
                            if False == tools.is_valid_json(res):
                                print('open pack No.{} failed! err: {}'.format(start+1, res))
                                continue
                            res = json.loads(res)
                            
                    # if "itemData" in res:
                    #     items = res["itemData"]
                    # if "itemList" in res:
                    #     items = res["itemList"]
                        
                    # duplicate_items = None
                    # if "duplicateItemIdList" in res:
                    #     duplicate_items = res['duplicateItemIdList']

                    # # high value player pause
                    # if duplicate_items is not None:
                    #     for dup_item in duplicate_items:
                    #         dup_item_id = dup_item["itemId"]
                    #         for item in items:
                    #             if "player" == item["itemType"] and item["rareflag"] not in [0, 1] and item["rating"]>88 and dup_item_id == item["id"]:
                    #                 print('high value player(rareflag:{}, rating:{}).'.format(item["rareflag"], item["rating"]))
                    #                 exit(0)
                            
                    # self.handle_pack(items, duplicate_items)
                    self.check_pruchsed_items()
                print('open pack No.{} end.'.format(start+1))

            for index, id in enumerate(arr_items):
                if index < self.cfg_sbc[sbc_id]['player_numbers']:
                    self.player_list.pop(id)
                else:
                    break
            start += 1
            print('*'*20)
    
    def handle_item(self):
        res = self.api.purchased_items()
        if False == tools.is_valid_json(res):
            return res
        res = json.loads(res)
        items = res["itemList"]
        duplicate_items = res["duplicateItemIdList"]
        self.handle_pack(items, duplicate_items)

    def aotobuypack(self, pack_id, times=5):
        start = 0
        while start < times:
            res = self.buy(pack_id=pack_id)
            if False == tools.is_valid_json(res):
                print('buy pack {} failed!'.format(start))
                print('*'*15)
                continue
            res = json.loads(res)
            items = []
            if 'itemList' in res:
                items = res["itemList"]
            elif 'itemData' in res:
                items = res["itemData"]
            else:
                print("res error: {}".format(res))
                continue
            duplicate_items = res["duplicateItemIdList"]

            # high value player pause
            if duplicate_items is not None:
                for dup_item in duplicate_items:
                    dup_item_id = dup_item["itemId"]
                    for item in items:
                        if "player" == item["itemType"] and item["rareflag"] not in [0, 1] and item["rating"]>88 and dup_item_id == item["id"]:
                            print('high value player(rareflag:{}, rating:{}).'.format(item["rareflag"], item["rating"]))
                            return duplicate_items
                
            self.handle_pack(items, duplicate_items)
            start += 1
            print('buy pack {} end'.format(start))
            print('*'*15)
            # sleep(2)

    def handle_pack(self, items, duplicate_items):
        arr_player = []
        arr_player_trade = []
        list_player = {}
        list_other = {}
        if items is not None:
            for item in items:
                if "player" == item["itemType"]:
                    arr_player.append({"id": item["id"], "pile": "club"})
                    list_player[item["id"]] = item
                # elif "misc" == item["itemType"]:
                #     self.put(misc_item_id=item["id"])
                else:
                    list_other[item["id"]] = item

        list_dup_player = {}
        if duplicate_items is not None:
            for item in duplicate_items:
                if item["itemId"] in list_player:
                    player = list_player.pop(item["itemId"])
                    if True == player['untradeable']:
                        list_dup_player[item["itemId"]] = player
                    else:
                        arr_player_trade.append({"id":item["itemId"], "pile":"trade"})

        if len(arr_player_trade) > 0:
            res = self.put(arr_player_trade)
            if False == res:
                return res

        if len(arr_player) > 0:
            res = self.put(arr_player)
            if False == res:
                return res
            
            self.player_list.update(list_player)
            with open('player_list2.json', 'w') as file:
                file.write(json.dumps(self.player_list))
        if len(list_other) > 0 or len(list_dup_player) > 0:
            self.sell(list(list_other.keys())+list(list_dup_player.keys()))
            if len(list_dup_player) > 0:
                print("{} duplicate players sold.".format(len(list_dup_player)))

    def query(self):
        print("money:", self.money)
        print("player_list:", self.player_list)
        print("market_list:", self.market_list)


if __name__ == "__main__":
    # 创建一个用户实例
    user1 = User()
