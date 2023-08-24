from ApiInterface import ApiInterface
import config

class User:
    def __init__(self, sid=config.G_SID, api=None, money=None, players_list=None, market_list=None):
        self.sid = sid
        self.api = ApiInterface("https://utas.mob.v1.fut.ea.com/ut/", sid)

    def buy(self, item):
        res = self.api.purchased_items(101)
        res = json.loads(res)
        
        if item in self.market_list and self.money >= self.market_list[item]:
            self.money -= self.market_list[item]
            # 执行购买逻辑，比如将物品添加到玩家的物品列表中
        else:
            print("购买失败：资金不足或物品不在市场上")

    def put(self, item, price):
        # 将物品添加到市场列表中，设定价格
        pass

    def sell(self, item):
        if item in self.players_list:
            # 执行出售逻辑，增加金钱并从玩家的物品列表中移除物品
            pass
        else:
            print("出售失败：物品不在玩家的物品列表中")

    def query(self):
        print("当前资金:", self.money)
        print("玩家物品列表:", self.players_list)
        print("市场物品列表:", self.market_list)


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
