# Fortuna-RNG-Python

基于Python语言实现Fortuna算法，可用于生成随机数、随机字节

## 程序概述

1. 测试环境：Windows 11，Python 3.7
2. 第三方库：time，os，hashlib，pyautogui，Crypto，random
3. 程序文件：
   - **entropy_collect.py**    熵源收集
   - **generator.py**    生成器
   - **accumulator.py**    累加器
   - **seed_manager.py**    种子文件管理
   - **main.py**    主函数

## 文件说明

### entropy_collect.py

用于事先收集随机事件

生成种子的熵池需要随机事件源，这个事件源不能由操作系统或者编程语言本身来提供（它们并非真随机，如os.random()方法），因此这里调用第三方库pyautogui中的方法position()，每0.5s获取用户鼠标的坐标(x,y)，将sha256(sha256(x)+sha256(y)+sha256(time.time()))写入熵源

### generator.py

用于Fortuna中的生成器

#### 初始化

- **cipher**    AES加密器
- **block_size**    加密块大小
- **counter**    计数器
- **key_size**    密钥长度
- **key**    AES密钥

#### 重新产生种子

输入为新种子 seed

更新 key = sha256(seed + key)

创建新的AES加密器 cipher = AES.new(key, AES.MODE_CTR,counter)

更新计数器 counter

#### 生成分组

内部函数，仅 generator.py 可调用

输入为生成的分组字节数 n

从一个空字符串 r 开始循环 n 次，每次使得 r += cipher.encrypt(counter)

返回值为 16 * n 字节的随机字符串 r 

#### 生成随机数据

输入为要生成的字节数 n 

要求 0 <= n <= 2 ** 20

调用生成分组函数，取 r = 结果的前 n 个字节

同时更新 key = self.__generate_blocks(2)

返回值为 n 字节的随机数据 r 

### accumulator.py

用于Fortuna中的累加器

#### 初始化

- **pool_num**    熵池数量
- **min_pool_size**    熵池最小规模
- **pool**    熵池
- **reseed_cnt**    重新产生种子的计数器
- **generator**    发生器
- **last_reseed_time**    上一次重新产生种子的时间
- **reseed_itv**    重新产生种子的时间间隔

#### 生成随机数据

输入为要生成的字节数 n

先检查熵池规模是否大于限制，或者距上一次重新产生种子是否超过时间间隔

计数器 reseed_cnt 自增

遍历熵池中的每个池子，若通过分解测试 reseed_cnt % (2 ** i) == 0，则用熵池中的数据重新生成种子 s += hashlib.sha256(self.pool[i]).digest()

同时重置熵池，调用 generator.py 中的方法reseed

更新 last_reseed_time，返回值为调用 generator.py 中的 pseudo_random_data(n)

#### 加入随机事件

输入值为随机源编号 s，池子编号 i，事件数据 e

在 1 <= len(e) <= 32 and 0 <= s <= 255 and 0 <= i <= 31 的前提下

更新池子 pool[i] = pool[i] + (str(s) + str(len(e))).encode() + e

### seed_manager.py

用于Fortuna中的种子文件管理

#### 初始化

- **seed_file**    种子文件名称
- **entropy_file**    源文件名称
- **accumulator**    初始化累加器
- **seed_itv**    重新产生种子文件的时间间隔
- **last_seed_time**    上一次重新产生种子的时间
- **source**    源编号
- **index**    熵池编号

#### 写入种子文件

向种子文件 seed_file 中写入 accumulator.pseudo_random_data(64)

#### 更新种子文件

初始化累加器（状态）

为保证种子文件不为空且长度为64字节，先调用 write_seed_file()

如果超出重新产生种子文件的事件间隔，则重新生成文件

同时更新时间，并向累加器中加入随机事件，这里要随机读取熵源作为随机事件，使 source 和 index 都自增

### main.py

用做Fortuna中的业务函数，可以按照需求随意修改，这里是做的随机字节&随机数两种输出模式

首先初始化累加器，生成器中声明有内部函数，不能直接被用户调用

若已有种子文件，则优先读取；若没有则使用熵源文件中随机的64个字节作为初始种子



