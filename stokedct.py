import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from util.artists import artists

# base_url = 'https://stokedct.com/collections/'
# url_list = [
#   base_url + artist.lower().replace(' ', '-') 
#   for artist in artists
#]

url_list = ['https://stokedct.com/collections/steve-h',]

product_list = []

for url in url_list:
  artist_page = urlopen(url)
  artist_html = artist_page.read().decode('utf-8')
  artist_soup = BeautifulSoup(artist_html, 'html.parser')

  products = artist_soup.find_all("div", {"class": "product_inside"})
  
  for product in products:
    p_fulltitle = product.find('img')['alt']
    
    # Extract item name after the hyphen (is this consistent for all artists)
    p_item_name = re.search(r'-\s(.+)', p_fulltitle).group(1)
    
    p_item_img_link = product.find('img')['src']

    p_item_link = 'https://stokedct.com' + product.find('a')['href']

    p_item_desc = product.find('div', {'class':'description'}).text
    p_item_desc = p_item_desc.replace(u"\u00A0", " ") #remove non breaking spaces
    
    p_item_price = product.find('div', {'class':'price'}).span.text

    p_item_old_price = product.select('span.old-price.hide')[0].text
    
    item_dict = {
      'name': p_item_name,
      'img': p_item_img_link,
      'link': p_item_link,
      'desc': p_item_desc,
      'price': p_item_price,
      'old_price': p_item_old_price,
    }

    print(item_dict)
