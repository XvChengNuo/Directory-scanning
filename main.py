import queue
import threading
import time
import argparse
import requests
import sys
from fake_useragent import UserAgent

parser = argparse.ArgumentParser(description='operation instruction')#使用帮助
parser.add_argument("-u", "--url", dest='url', required=True, help='please input url')#url
parser.add_argument("-p", "--path", dest='path', required=True, help='please input dictionary path')#字典路径
parser.add_argument("-t", "--thread", type=int, dest='thread', default=10, help='set thread')#设置线程
parser.add_argument("-x", "--proxy", type=str, dest='proxy', help='Set up proxy')#设置某个代理
parser.add_argument("-ua", "--random-agent", dest='ua', action='store_true', help='Set ua header randomly.')#设置随机UA头
parser.add_argument("-s", "--second", type=int, dest='second', default=0, help='Set request interval')#设置请求间隔
args = parser.parse_args()


def dim(url):
    if url[-1] == '/':
        url = url[:-1]
    return url

def bruster(url):

    while not q.empty():
        time.sleep(argsec)
        # print('ssssssssssssssssssssss')
        u = url + q.get()
        argset = args.proxy
        argua = args.ua
        http1 = argset
        proxise = {
            'http': http1
        }
        if argua:
            userage = UserAgent()
            UserAge = userage.random
        else:
            UserAge = None
        headers = {"User-Agent":UserAge}
        # print(argset,UserAge,argua,http1)
        rep = requests.get(u, headers=headers, proxies=proxise, verify=False)  # 取出队列里的依次请求
        rep_code = rep.status_code
        # print(rep_code)
        # if rep_code == 200 | rep_code == 302:
        #     print("%s\t%s" % (rep_code, u))
        if rep_code == 404 or rep_code == 200:
            print(rep_code, u)
        # print(time.time() - start_time)
    else:
        sys.exit()

if __name__ == "__main__":
    argpath = args.path
    argsec = args.second
    argurl = args.url
    argthread = args.thread
    argurl = dim(argurl)
    # print(argurl,argpath,argthread)
    q = queue.Queue()
    # start_time = time.time()   判断程序运行时间，看看多线程起用没
    filenames = open(argpath, 'r').readlines()
    for filename in filenames:
        filename = filename.strip()
        q.put(filename)  # 将字典内的元素添加进q队列
    thread_list = []  # 初始化线程
    for _ in range(int(argthread)):  # 初始化五个线程
        t = threading.Thread(target=bruster, args=(argurl,))  # 以targe线程运行的函数生成线程,arges指定传参（即bruster函数接收的参数）
        thread_list.append(t)  # 添加线程
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()# 等待线程执行结束后，回到主线程中