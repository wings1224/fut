from time import sleep
from ApiInterface import ApiInterface
import config
from User import User

if __name__ == "__main__":
    # 创建 API 接口实例
    api = ApiInterface("https://utas.mob.v1.fut.ea.com/ut/", config.G_SID)
    user = User(config.G_SID, api)

    times = 0
    # with open('times.txt', 'r') as file:
    #     times = int(file.read())

    while True:
        times += 1
        print('*'*20)
        print("now is {} times".format(times))
        # sbc and open pack 
        # user.aotobuypack(pack_id=101, times=10)

        # daily bronze upgrade
        # user.sbc(times=1,sbc_id=3503)
        # daily silver upgrade
        # user.sbc(times=10,sbc_id=3500)
        # ultimate bronze upgrade
        user.sbc(times=2,sbc_id=3054)
        # ultimate silver upgrade
        user.sbc(times=3,sbc_id=3056)
        # futties crafting upgrade 
        # user.sbc(times=30,sbc_id=3263,need_open=False)
        # 82+ pick
        # user.sbc(times=2,sbc_id=3394,need_open=False)
        # 80+ pick
        user.sbc(times=1,sbc_id=3040,need_open=False)
    
    
    # with open('times.txt', 'w') as file:
    #     file.write(str(times))
    
1