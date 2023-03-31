import math
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Counter


class Generator:
    # 初始化
    def __init__(self):
        self.cipher = None
        self.block_size = AES.block_size   # 这里用了AES算法，故要求块大小与AES加密的块大小相等
        self.counter = Counter.new(nbits=self.block_size * 8, initial_value=0, little_endian=True)    # 初始化计数器
        self.key_size = 32   # 密钥长度 = 32
        self.key = self.key = b'\0' * self.key_size   # 初始化密钥

    # 重新产生种子
    def reseed(self, seed):
        self.key = hashlib.sha256(seed + self.key).digest()    # 计算种子+密钥的SHA256哈希值，得到用于AES加密的新密钥
        self.cipher = AES.new(self.key, AES.MODE_CTR,counter=self.counter)    # 创建AES加密器
        self.counter()   # 计数器自增

    # 生成分组
    def __generate_blocks(self, n):   # 内部函数，故需要在前面加__
        assert self.key and self.counter
        r = b''
        for i in range(n):
            r += self.cipher.encrypt(self.counter())
        return r   # 返回16*n字节的随机字节字符串r

    # 生成随机数据
    def pseudo_random_data(self, n):
        assert 0 <= n <= 2 ** 20   # 允许输出字节数的范围
        r = self.__generate_blocks(math.ceil(n // 16) if n >= 16 else 1)[:n]   # 取生成的前n个字节，这里n // 16要向上取整，保证分组数足够
        self.key = self.__generate_blocks(2)   # 生成2个字节 = 16位的密钥
        return r   # 返回n字节的随机数据







