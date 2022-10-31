import re
import csv
import os.path
from datetime import date
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}

url = 'https://store.nvsglassworks.com/product-category/heady-glass/?ppp=5'
page = urlopen(Request(url, headers=header))
html = page.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

#products columns-4
all_items = soup.select('ul.products.columns-4')[0].children

