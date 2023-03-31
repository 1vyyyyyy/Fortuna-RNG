import random
from Crypto.Util.number import bytes_to_long
from seed_manager import SeedManager
from accumulator import Accumulator

seed_file = "seed"  # 种子文件名称
entropy_file = "entropy"  # 熵源文件名称


def main():
    accumulator = Accumulator()   # 初始化累加器
    try:
        f = open(seed_file, 'rb')   # 优先使用已有的种子文件
    except:
        with open(entropy_file, 'rb') as random_source:   # 若无种子文件则使用熵源文件中随机的64个字节作为初始种子
            max_rand = len(random_source.read()) // 64
            random_source.seek(random.randint(1, max_rand), 0)
            seed = random_source.read(64)
    else:
        try:
            seed = f.read(64)
            assert len(seed) == 64
        finally:
            f.close()
    accumulator.generator.reseed(seed)   # 重新产生种子
    SeedManager().update_seed_file(accumulator)   # 更新种子文件
    # 生成随机数
    print("----随机数生成器^_^----")
    print("输入n/b选择输出模式，输入其他字符退出程序")
    mode = input("请选择输出模式: ")
    if mode == "n":
        while 1:
            byte = input("请输入要生成的随机数长度，输入e退出程序: ")
            if byte == 'e':
                print("程序已退出-_-")
                exit(0)
            else:
                print(bytes_to_long(accumulator.pseudo_random_data(int(byte))))
    elif mode == "b":
        while 1:
            byte = input("请输入要生成的随机字节长度，输入e退出程序: ")
            if byte == 'e':
                print("程序已退出TvT")
                exit(0)
            else:
                print(accumulator.pseudo_random_data(int(byte)))
    else:
        print("程序已退出OvO")
        exit(0)


if __name__ == '__main__':
    main()
