import sys
import time


for second in range(120, -1, -1):
    # print("%02d:%02d"%(second // 60,second % 60))

    sys.stdout.write(" 倒计时：%02d:%02d" % (second // 60,second % 60) + '\r')
    sys.stdout.flush()

    time.sleep(1)