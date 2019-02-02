#!/usr/bin/python
# coding: utf-8

from fbchat import Client
from fbchat.models import *
# import fbchat
# https://fbchat.readthedocs.io/en/master/api.htm

import json

import hashlib
import os
import time
import requests
import sys

urlStr = sys.argv[1]
url = "http://" + urlStr
folder = "Data"
ext = ".txt"
cuteName = "of Benjamin"
currentTime = time.time() * 1 # 1000 milliseconds
websiteContent = requests.get(url, auth=('user', 'password'))
text = websiteContent.text.encode("ascii", "ignore")
sha224 = hashlib.sha224(text)
#print(text)

if not os.path.isdir(folder):
    os.mkdir(folder)
urlStr = urlStr.replace("/", "\\")
filePath = os.path.join(folder, urlStr)

def writeDefault():
    file = open(filePath, "w")
    file.write(str(currentTime) + "\n")
    file.write(sha224.hexdigest())
    file.close()
    exit()

def writeLog():
    file = open(os.path.join(folder, urlStr + "-" + str(currentTime)), "w")
    file.write(text)
    file.close()

if os.path.isfile(filePath):
    file = open(filePath, "r")
    lines = file.readlines()
    file.close()
    if currentTime > long(float(lines[0].replace("\n", ""))) + 3600: # 3 600 000 consider that after more than 1 hour, people don't care about receiving notifications
        writeDefault()
    else:
        if sha224.hexdigest() != lines[1]:
            #print("changed !")

            cookies = {}
            try:
                with open('session.json', 'r') as f:
                    cookies = json.load(f)
            except:
                pass

            client = Client("email", "password", session_cookies=cookies)

            #group = client.searchForGroups("Group name")[0]
            #print(group.uid)
            #print(group.name)
            client.send(Message(text='The website has been updated.'), thread_id=FOUND_YOUR_THREAD_ID, thread_type=ThreadType.GROUP)

            with open('session.json', 'w') as f:
                json.dump(client.getSession(), f)

            writeLog()
            writeDefault()
        else:
            writeDefault()
else:
    writeDefault()
