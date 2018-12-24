# python3
# -*- coding: utf-8 -*-
# Filename: jandan_demo.py
"""
输出煎蛋妹子图地址

@author: v1coder
"""

import requests
from bs4 import BeautifulSoup
import base64

headers = {'User-Agent': ''}

url = 'http://jandan.net/top-ooxx'
data = requests.get(url, headers=headers).content
soup = BeautifulSoup(data, 'lxml')
url_tags = soup.find_all('span', class_="img-hash")
for url_tag in url_tags:
    url_hash = url_tag.text
    # base64 to bytes
    url_bytes = base64.b64decode(url_hash)
    # bytes to str
    url = str(url_bytes, encoding='utf-8')
    complete_url = 'http:' + url
    print(complete_url)
