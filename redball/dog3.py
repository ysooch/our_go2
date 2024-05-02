import threading
import queue
import time
# 쓰레드간 채널(큐)
q = queue.Queue()
# 입력받아서 다른 쓰레드에 보내주는 곳
def first_thread():
    print("channel publisher wait for input")
    q.put(input())
    print("channel publisher end for input")
# 받아서 쓰는 곳
def second_thread(): 
    time.sleep(5)
    print("channel scriber wait for 5 sec")
    try:
        item = q.get_nowait()
        print(item)
    except:
        print("there is no item in queue")
    print("channel scriber end")
# thread 생성
thread1 = threading.Thread(target=first_thread, args=())
thread2 = threading.Thread(target=second_thread, args=())
# thread 시작
thread1.start()
thread2.start()