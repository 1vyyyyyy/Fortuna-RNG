import hashlib
import time
from generator import Generator


class Accumulator:
    # 初始化
    def __init__(self):
        self.pool_num = 32  # 熵池数量
        self.min_pool_size = 64  # 熵池最小规模
        self.pool = [b'\0'] * self.pool_num  # 初始化熵池
        self.reseed_cnt = 0  # 初始化重新产生种子的计数器
        self.generator = Generator()  # 初始化发生器
        self.last_seed_time = time.time()  # 上一次重新产生种子的时间
        self.reseed_itv = 0.1  # 重新产生种子的时间间隔

    # 生成随机数据
    def pseudo_random_data(self, n):
        if len(self.pool[0]) >= self.min_pool_size or time.time() - self.last_seed_time > self.reseed_itv:
            self.reseed_cnt += 1   # 计数器自增
            s = b''
            for i in range(self.pool_num):
                if self.reseed_cnt % (2 ** i) == 0:   # 分解测试
                    s += hashlib.sha256(self.pool[i]).digest()    # 用熵池中的数据生成种子
                    self.pool[i] = b'\0'   # 熵池重置
            self.generator.reseed(s)   # 重新产生种子
            self.last_seed_time = time.time()   # 记录此次重新产生种子的时间
        return self.generator.pseudo_random_data(n)

    # 加入随机事件
    def add_random_event(self, s, i, e):  # s为随机源编号，i为池子编号，e为事件数据
        assert 1 <= len(e) <= 32 and 0 <= s <= 255 and 0 <= i <= 31
        self.pool[i] = self.pool[i] + (str(s) + str(len(e))).encode() + e
