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
        user.aotobuypack(pack_id=101, times=30)
        # broze 3054
        # user.sbc3054(times=10)
        # user.sbc(times=25,sbc_id=3263,need_open=False)
        user.sbc(times=55,sbc_id=3056)
        user.sbc(times=45,sbc_id=3054)
        user.sbc(times=25,sbc_id=3056)
        user.sbc(times=5,sbc_id=3263,need_open=False)
        # 82+ pick
        # user.sbc(times=2,sbc_id=3394,need_open=False)
    
    
    # with open('times.txt', 'w') as file:
    #     file.write(str(times))
    
1