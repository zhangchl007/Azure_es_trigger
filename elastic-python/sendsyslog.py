#!/usr/bin/env python
# coding=utf-8

import time
import random
import sys, getopt
import os
import requests
import json
import socket
import logging
import logging.handlers

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

my_logger.addHandler(handler)

def createdirs():
    path = "/app/logs"
    if not os.path.exists(path):
       os.makedirs(path)
def writedata(content, path):
    subscriptions, resourceGroups = getMetadata()
    with open(path + "app.log", "a") as f:
        #content1 = content + "VF slot 1 removed" + "\n"
        #content2 = content + "VF slot 1 added" + "\n"
        content3 = content + "\n"
        while True:
            try:
                num = random.randint(1,500)
                if num == 1:
                    my_logger.critical('kernel: [   21.985720] this is critical: VF slot 1 removed ' + "AZURE_SUBSCRIPTION_ID: " + subscriptions + "AZURE_ResourceGroup: " + resourceGroups)
                    my_logger.critical('kernel: [   21.985720] this is critical: VF slot 1 added ' + "AZURE_SUBSCRIPTION_ID: " + subscriptions + "AZURE_ResourceGroup: " + resourceGroups)
                    print("critical")
                    time.sleep(0.1)
                else:
                    f.writelines(content3)
                    time.sleep(0.1)
            except Exception as e:
                print ("write warn log error", str(e))
                break
def getMetadata():
    metadata_url ="http://169.254.169.254/metadata/instance"
    # This must be sent otherwise the request will be ignored
    header = {'Metadata' : 'true'}
    # Current version of the API
    query_params = {'api-version':'2021-02-01'}
    try: 
        resp = requests.get(metadata_url, headers = header, params = query_params)
        data = resp.json()
        resourceid=data['compute']['resourceId']
        subscriptions=resourceid.split('/')[2]
        resourceGroups=resourceid.split('/')[4]
        return subscriptions, resourceGroups 
    except Exception as e:
        print ("write warn log error", str(e))

if __name__ == "__main__":
    # 写入内容
    opts, args = getopt.getopt(sys.argv[1:], "hn:")
    lines=""
    for op, value in opts:
       if op == "-n":
          lines= value
          print(lines)
       elif op == "-h":
          sys.exit()
    if len(sys.argv) < 1:
        print("请输入正确参数: -n")
        sys.exit(1)
    else:
        # 创建的目录
        createdirs()
        path = "/app/logs/"
        print("开始计时(写入日志)")
        t0 = time.time()

        content = "kernel: this is a nic drop: "
        content = socket.gethostname() + ": " + content
        getMetadata()
        writedata(content, path)

        t1 = time.time()
        print("完成时间为：{0}".format(t1 - t0))
