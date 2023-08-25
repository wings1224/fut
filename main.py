from time import sleep
from ApiInterface import ApiInterface
import config
from User import User

if __name__ == "__main__":
    # 创建 API 接口实例
    api = ApiInterface("https://utas.mob.v1.fut.ea.com/ut/", config.G_SID)
    user = User(config.G_SID, api)

    # user.aotobuypack(pack_id=101, times=50)
    
    # sbc and open pack 
    # broze 3054
    user.sbc3054(times=10)

