__author__ = 'Mim'
# Eugene Mim
# IFLHowl
# 06.07.18

import wmi
import requests
from playsound import playsound
import os
import os
import sched, time
import re
import errno, os, winreg
import ctypes
from ctypes import wintypes
import pubnub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub          import PubNub, SubscribeListener
from bs4 import BeautifulSoup
import requests
import urllib.request
from bs4.element import Comment

url = "index.html"
# Getting the webpage, creating a Response object.
response = requests.get(url)
# Extracting the source code of the page.
data = response.text
# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
soup = BeautifulSoup(data, 'lxml')
# Extracting all the <a> tags into a list.
#tags = soup.find_all('a')
trinket = soup.find("div", {"id": "currentActivity"})
print (trinket)
# Extracting URLs from the attribute href in the <a> tags.
#
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

html = urllib.request.urlopen(url).read()
print(text_from_html(html))




#XXXXXXXXXXXXXXXXXXXXXXXXX
#l("onetwo1").message("hello").pn_async(DatabaseSync)
#XXXXXXXXXXXXXXXXXXXX
# def check_channel():
#
# def ping():
#     try:
#         fetch_lmi_name()
#         payload = {
#             '': classroom_id,
#             }
#         #httpbin.org used for testing purposes.
#         r = requests.post("http://httpbin.org/post", data=payload)
#         # r = requests.post("https://lighthouseprod.herokuapp.com/devices", data=payload)
#         print r.text
#     except:
#         pass

#second try at assigning ID. if flat file is not configured, classroom ID is left blank and program does not ping. Checks this file for info every 60 seconds.
#
print ("Made it")
#
# play_sound()

# try:
#     pingtask.enter(60, 1, ping_loop, (pingtask,))
# #activates loop
#     pingtask.run()
# except:
#     pass
