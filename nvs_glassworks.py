import re
import csv
import os.path
from datetime import date
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

header = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
  'AppleWebKit/537.11 (KHTML, like Gecko) '
  'Chrome/23.0.1271.64 Safari/537.11',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
  'Accept-Encoding': 'none',
  'Accept-Language': 'en-US,en;q=0.8',
  'Connection': 'keep-alive'
}

def write_product_to_file(product):
  """Convert dictionary to csv lines"""
  datestr = date.today().strftime('%Y%m%d')
  filename = f'nvs_glassworks_{datestr}.csv'
  if not os.path.exists(filename):
    with open(filename, 'w', newline='\n', encoding='utf-8') as newfile:
      newfile.write('shop_name,category,artist,name,link,price\n')

  with open(filename, 'a+', newline='\n', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
      product['shop_name'],
      product['category'],
      product['artist'],
      product['name'],
      product['link'],
      product['price'],
    ])

url = 'https://store.nvsglassworks.com/product-category/heady-glass/?ppp=1000'
page = urlopen(Request(url, headers=header))
html = page.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Get artist list to help identify artists
artist_list_raw = soup.find('li', class_='cat-item-20')
artist_links = artist_list_raw.find('ul', class_='children')
artists = [link.text.strip() for link in artist_links if link != '\n']

# Manual additions if I notice items have a different name than the artist listing (happens a lot)
artists.append('Ashes Glass')
artists.append('Envy Glass')
artists.append('Fatboy')
artists.append('FatBoy')
artists.append('GlassKatCreations')
artists.append('Happy Time')
artists.append('Harold Ludeman')
artists.append('Hubbard')
artists.append('Leisure')
artists.append('Logiglass')
artists.append('Ludeman')
artists.append('Manchild Glass')
artists.append('MeadeMade')
artists.append('MIO')
artists.append('Ryglass')
artists.append('Thomas Sanchez')
artists.append('Turtle Time')
artists.append('Vigil')
artists.append('Waugh Street')

# Loop through all the products on the page and EXTRACT. THAT. DATA!
all_items = soup.find_all('li', class_='product')

item_count = 0

for item in all_items:
  link_href = item.find('a').get('href')
  item_img = item.find('img').get('src')
  item_name_price_block = item.find('a').text.strip()

  # TODO: Fix this -- right now it is erroring on sale items because they have a different format
  try:
    item_name, item_price = item_name_price_block.split('\n')
  except:
    pass

  item_price = re.sub(r'[$,]', '', item_price, re.I)
  item_artist = ''
  for count, artist in enumerate(artists):
    if artist in item_name:
      item_artist = artists[count]

  item_dict = {
    'shop_name':    'NVS Glassworks',
    'category':     'Heady Glass',
    'artist':       item_artist,
    'name':         item_name,
    'link':         link_href,
    'price':        item_price,
  }

  item_count += 1
  write_product_to_file(item_dict)

print(f'Total items processed: {item_count}')