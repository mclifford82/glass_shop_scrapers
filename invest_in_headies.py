import re
import csv
import os.path
from datetime import date
from bs4 import BeautifulSoup
from urllib.request import urlopen
from util.util import write_product_to_file

url_list = [
  'https://investinheadies.com/collections/recycler',
  'https://investinheadies.com/collections/jammer',
  'https://investinheadies.com/collections/mini-tube',
  'https://investinheadies.com/collections/sculpture'
  'https://investinheadies.com/collections/flower-pieces', 
  'https://investinheadies.com/collections/pearls-marbles', 
  'https://investinheadies.com/collections/pendants', 
  'https://investinheadies.com/collections/drink-ware', 
  'https://investinheadies.com/collections/jars', 
  'https://investinheadies.com/collections/quartz', 
  'https://investinheadies.com/collections/mood-mats', 
  #'https://investinheadies.com/collections/caps', 
  #'https://investinheadies.com/collections/chains', 
  #'https://investinheadies.com/collections/dab-tools', 
  #'https://investinheadies.com/collections/torches', 
  #'https://investinheadies.com/collections/temperature-devices', 
  #'https://investinheadies.com/collections/accessories', 
  #'https://investinheadies.com/collections/apparel', 
  #'https://investinheadies.com/collections/stickers'
]

def write_product_to_file(product):
  """Convert dictionary to csv lines"""
  datestr = date.today().strftime('%Y%m%d')
  filename = f'investinheadies_{datestr}.csv'
  if not os.path.exists(filename):
    with open(filename, 'w', newline='\n', encoding='utf-8') as newfile:
      newfile.write('shop_name,category,artist,name,link,price,sale_flag\n')

  with open(filename, 'a+', newline='\n', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
      product['shop_name'],
      product['category'],
      product['artist'],
      product['name'],
      product['link'],
      product['price'],
      product['sale_flag'],
    ])

for url in url_list:
  # Keep track of what page we're on for this category, resets with each loop
  url_page_count = 1
  product_count = 0
  category_name = re.search(r'.*/(.+)$', url, re.I).group(1).title()

  print(f'Working on: {category_name} ... ', end='')
  
  for page_num in range(2):
    try:
      page_url = url + f'?page={page_num+1}'
      page_raw = urlopen(page_url)  
      page_html = page_raw.read().decode('utf-8')
      page_soup = BeautifulSoup(page_html, 'html.parser')
    except:
      pass

    all_items_raw = page_soup.find_all('a', {'class':'grid-link'})

    for item in all_items_raw:
      item_link = f'https://investinheadies.com' + item['href']
      item_name = item.find('p', {'class':'grid-link__title'}).text
      item_artist = ''
      on_sale_flag = 0

      can_parse_artist = re.search(r'(.+)\s+-\s+(.+)', item_name, re.I)

      if can_parse_artist != None:
        item_artist = can_parse_artist.group(1)
        item_name = can_parse_artist.group(2)

      item_price_raw = item.find('p', {'class':'grid-link__meta'})
      on_sale = item.find('s', {'class':'grid-link__sale_price'})
      
      if on_sale != None:
        on_sale_flag = 1
        item_price = list(item_price_raw.children)[-1].strip()
        item_price = re.sub(r'[$,]', '', item_price, re.I)
      else:
        on_sale_flag = 0
        item_price = re.search(r'\$([0-9.,]+)', str(item_price_raw)).group(1)
        item_price = re.sub(r'[$,]', '', item_price, re.I)

      item_dict = {
        'shop_name': 'Invest In Headies',
        'category':category_name,
        'artist': item_artist,
        'name': item_name,
        'link': item_link,
        'price': item_price,
        'sale_flag':on_sale_flag,
      }

      product_count += 1
      write_product_to_file(item_dict)

  print(f'{product_count} processed.')
