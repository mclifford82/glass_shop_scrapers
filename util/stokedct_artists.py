from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_artist_list(): # Returns a list of tuples (artist name, link)
  url = 'https://stokedct.com'
  page = urlopen(url)
  html = page.read().decode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')

  artist_list = []

  artist_blob = soup.select_one('div.row.menu-list-col')
  artists = artist_blob.find_all('div', class_='col-sm-2')

  for artist in artists:
    # Extract artist name
    name = artist.find('a', {'class': 'title-underline'}).find('span').text
    link = url + artist.find('a')['href']
    artist_list.append((name, link))

  return artist_list

artists = get_artist_list()