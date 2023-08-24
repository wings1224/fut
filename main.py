from time import sleep
from ApiInterface import ApiInterface
import config
from User import User

if __name__ == "__main__":
    # 创建 API 接口实例
    api = ApiInterface("https://utas.mob.v1.fut.ea.com/ut/", config.G_SID)
    user = User(config.G_SID, api)
    start = 0
    while start<10:
        # todo buy broze pack
        items, duplicate_items = user.buy(pack_id=101)
        arr_player = []
        list_other = {}
        for item in items:
            if "player" == item["itemType"]:
                arr_player.append({"id":item["id"], "pile":"club"})
            # elif "misc" == item["itemType"]:
            #     user.put(misc_item_id=item["id"])
            else:
                list_other[item["id"]]=item

        list_dup_player = {}
        # arr_dup_player = []
        for item in duplicate_items:
            if item["itemId"] in arr_player:
                list_dup_player[item["itemId"]]=arr_player[arr_player]
                # arr_dup_player.append({"id":item.id, "pile":"trade"})
                del arr_player[item["itemId"]]

        user.sell(list(list_other.keys())+list(list_dup_player.keys()))
        user.put(arr_player)
        start+=1
        print('*'*10)
        print('pack {}'.format(start))
        # sleep(2)
    