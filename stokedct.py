import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
from util.util import write_product_to_file

# Cycle through pages, collecting info from each item and then outputting to a csv file
count = 0
base_url = 'https://stokedct.com/collections/all'

# access first page to get the total item count, divided by 36 rounded up to get the range(1, X, 1) value
p = urlopen(base_url)
h = p.read().decode('utf-8')
s = BeautifulSoup(h, 'html.parser')

product_count_text = s.select('div.number-of-products.pull-right')[0].text
product_count = int(re.search(r'(\d+)\s.+', product_count_text, re.I).group(1))
page_count = round(product_count / 36) + 1

url_list = [
  f'https://stokedct.com/collections/all?page={page}'
  for page in range(1, page_count, 1)
]

for page_num, url in enumerate(url_list):
  artist_page = urlopen(url)
  artist_html = artist_page.read().decode('utf-8')
  artist_soup = BeautifulSoup(artist_html, 'html.parser')

  products = artist_soup.find_all("div", {"class": "product_inside"})

  for product in products:
    p_fulltitle = product.find('img')['alt']
    
    # Extract item name after the hyphen if one is present. If not, take the whole name
    if '-' in p_fulltitle:
      p_item_artist = re.search(r'(.+)\s?-\s?(.+)', p_fulltitle).group(1).strip()
      p_item_name = re.search(r'(.+)\s?-\s?(.+)', p_fulltitle).group(2).strip()
    else:
      p_item_artist = 'Stoked CT Store'
      p_item_name = p_fulltitle
    
    p_item_img_link = product.find('img')['src']

    p_item_link = 'https://stokedct.com' + product.find('a')['href']

    #p_item_desc = product.find('div', {'class':'description'}).text
    #p_item_desc = p_item_desc.replace(u"\u00A0", " ") #remove non breaking spaces
    
    p_item_price = product.find('div', {'class':'price'}).span.text
    p_item_price = re.sub(r'[$,]', '', p_item_price, re.I) # 

    #p_item_old_price = product.select('span.old-price.hide')[0].text
    
    item_dict = {
      'artist': p_item_artist,
      'name': p_item_name,
      'img': p_item_img_link,
      'link': p_item_link,
      #'desc': p_item_desc,
      'price': p_item_price,
      #'old_price': p_item_old_price,
    }

    write_product_to_file(item_dict)
    count += 1

  print(f'Page {page_num+1} - Current count is {count}')
  
print(f'We fuckin did it! {count} items downloaded!')