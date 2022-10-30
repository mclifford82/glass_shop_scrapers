from datetime import date
import os.path
import csv

def write_product_to_file(product):
  """Convert dictionary to csv lines"""
  datestr = date.today().strftime('%Y%m%d')
  filename = f'stokedct_{datestr}.txt'
  if not os.path.exists(filename):
    with open(filename, 'w', newline='\n') as newfile:
      newfile.write('shop_name,artist,name,img,link,price\n')

  with open(filename, 'a+', newline='\n') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
      product['shop_name'],
      product['artist'],
      product['name'],
      product['img'],
      product['link'],
      product['price'],
    ])