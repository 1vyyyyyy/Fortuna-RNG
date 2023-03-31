import time
import random


class SeedManager:
    # 初始化
    def __init__(self):
        self.seed_file = "seed"  # 种子文件名称
        self.entropy_file = "entropy"  # 熵源文件名称
        self.accumulator = None  # 初始化累加器
        self.seed_itv = 600  # 重新产生种子文件的时间间隔
        self.last_seed_time = time.time()  # 上一次重新产生种子的时间
        self.source = 0   # 源编号
        self.index = 0   # 熵池编号

    # 写入种子文件
    def write_seed_file(self):
        with open(self.seed_file, 'wb') as f:
            f.write(self.accumulator.pseudo_random_data(64))

    # 更新种子文件
    def update_seed_file(self, accumulator):
        self.accumulator = accumulator
        self.write_seed_file()
        # 超过时间间隔，则重新产生一次种子文件
        if time.time() - self.last_seed_time >= self.seed_itv:
            with open(self.seed_file, 'rb+') as f:
                s = f.read()
                assert len(s) == 64
                self.accumulator.generator.reseed(s)
                f.seek(0)  # 文件指针移到开头
                f.truncate()  # 清空文件
                f.write(self.accumulator.pseudo_random_data(64))   # 重新写入文件
            self.last_seed_time = time.time()   # 更新时间

        # 向累加器中添加随机事件
        with open(self.entropy_file, 'rb') as random_event_source:
            max_rand = len(random_event_source.read()) // 32
            random_event_source.seek(random.randint(1, max_rand), 0)
            event = random_event_source.read(random.randint(1, 32))  # 随机读取熵源，作为随机事件
            self.accumulator.add_random_event(s=self.source, i=self.index, e=event)
            self.source = (self.source + 1) % 256
            self.index = (self.index + 1) % 32   # 编号都自增
