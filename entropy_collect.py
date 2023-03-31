import time
import os
import pyautogui as pag
import hashlib

# 熵源文件
entropy_file = "entropy"

# 利用鼠标指针位置和时间戳收集熵源
try:
    while True:
        x, y = pag.position()
        with open(entropy_file, "ab") as f:   # 向熵源中写入随机事件 x + y + time
            f.write(hashlib.sha256(hashlib.sha256(str(x).encode()).digest()
                                   + hashlib.sha256(str(y).encode()).digest()
                                   + hashlib.sha256(str(time.time()).encode()).digest()).digest())
        # 每隔0.5s写入一次文件 , 并执行清屏
        time.sleep(0.5)
        # 执行系统清屏指令
        os.system('cls')
except KeyboardInterrupt:
    exit(0)
