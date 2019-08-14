#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import sys
import time
import requests
from bs4 import BeautifulSoup as bfs
from cover import *


HOST = 'https://pinyin.sogou.com/dict/'
TIMEOUT = 30

def getEndPage(uri):
    url = HOST + uri

    res = requests.get(url, timeout=TIMEOUT)
    soup = bfs(res.text, "lxml")

    pageNums = soup.find_all(["span", "default"])
    maxPage = 0
    for nums in pageNums:
        if not nums.text.isdigit(): continue
        if int(nums.text) > maxPage:
            maxPage = int(nums.text)
    return maxPage+1


def getHtml(uri):
    updateTime = []
    result = []

    url = HOST + uri

    res = requests.get(url, timeout=TIMEOUT)
    soup = bfs(res.text, "lxml")

    titleRes = soup.find_all(class_="detail_title")
    btnRes = soup.find_all(class_="dict_dl_btn")
    updateRes = soup.find_all(class_="show_content")
    pageNums = soup.find_all(["span", "default"])
    maxPage = 0
    for nums in pageNums:
        if not nums.text.isdigit(): continue
        if int(nums.text) > maxPage:
            maxPage = int(nums.text)

    for upt in updateRes:
        if upt.contents[0].find('-') < 0: continue
        updateTime.append(upt.contents)
    for tit, btn, upt in zip(titleRes, btnRes, updateTime):
        for tc, bc, uc in zip(tit.children, btn.children, upt):
            result.append({"title": tc.contents[0].strip(), "link": bc.attrs["href"], "updateTime": uc})

    return result

if __name__ == '__main__':
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if PROJECT_DIR not in sys.path:
        sys.path.insert(0, PROJECT_DIR)

    dirs = os.path.dirname(os.path.abspath(__file__)) + '/dict'
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    startTime = int(time.time())
    print("startTime", startTime)
    wordType = [
                   {"uri": "cate/index/1/default/", "dictName": "naturalScience.dic"},     # 自然科学词典
                   {"uri": "cate/index/31/default/", "dictName": "humanities.dic"},        # 人为科学词典
                   {"uri": "cate/index/76/default/", "dictName": "socialScience.dic"},     # 社会科学词典
                   {"uri": "cate/index/96/default/", "dictName": "engineering.dic"},       # 工程与应该用科学词典
                   {"uri": "cate/index/127/default/", "dictName": "agriculture.dic"},      # 农林渔畜词典
                   {"uri": "cate/index/132/default/", "dictName": "medicalScience.dic"},   # 医学词典
                   {"uri": "cate/index/154/default/", "dictName": "art.dic"},              # 艺术词典
                   {"uri": "cate/index/167/default/", "dictName": "chinaCity.dic"},        # 中国城市词典
                   {"uri": "cate/index/367/default/", "dictName": "sport.dic"},            # 运动休闲词典
                   {"uri": "cate/index/389/default/", "dictName": "life.dic"},             # 生活词典
                   {"uri": "cate/index/403/default/", "dictName": "entertainment.dic"},    # 娱乐词典
                   {"uri": "cate/index/436/default/", "dictName": "games.dic"},            # 电子游戏词典
               ]

    for item in wordType:
        dictName = item["dictName"]
        pageNum = getEndPage(item["uri"])
        print(dictName, "pageTotal", pageNum)
        for i in range(1, pageNum):
            uri = item["uri"] + '%d' % i
            print(uri)
            result = getHtml(uri)
            if result:
                for res in result:
                    res = requests.get(res["link"])
                    cover2Content(res.content)
        write2File(dictName)
    print("TotalTime", int(time.time()) - startTime)