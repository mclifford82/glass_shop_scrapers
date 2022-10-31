import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from util.util import write_product_to_file

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

# Cycle through pages, collecting info from each item and then outputting to a csv file
count = 0
base_url = 'https://stokedct.com/collections/all'

# Access first page to get the total item count, divided by 36 rounded up to get the range(1, X, 1) value
page = urlopen(Request(base_url, headers=header))
html = page.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

product_count_text = soup.select('div.number-of-products.pull-right')[0].text
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
    # TODO: This could use expansion. There are definitely some false parsings. Good first pass.
    if '-' in p_fulltitle:
      p_item_artist = re.search(r'(.+)\s?-\s?(.+)', p_fulltitle).group(1).strip()
      p_item_name = re.search(r'(.+)\s?-\s?(.+)', p_fulltitle).group(2).strip()
    else:
      p_item_artist = 'Stoked CT Store'
      p_item_name = p_fulltitle
    
    p_item_img_link = product.find('img')['src']

    p_item_link = 'https://stokedct.com' + product.find('a')['href']
   
    p_item_price = product.find('div', {'class':'price'}).span.text
    p_item_price = re.sub(r'[$,]', '', p_item_price, re.I) # 
    
    item_dict = {
      'shop_name': 'Stoked CT',
      'artist': p_item_artist,
      'name': p_item_name,
      'img': p_item_img_link,
      'link': p_item_link,
      'price': p_item_price,
    }

    write_product_to_file(item_dict)
    count += 1

  print(f'Page {page_num+1} - Current count is {count}')
  
print(f'We fuckin did it! {count} items downloaded!')