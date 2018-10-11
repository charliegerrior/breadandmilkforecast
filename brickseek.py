import requests
from bs4 import BeautifulSoup
import re

#bread SKU: 13033157
#eggs SKU: 145051970
#milk SKU: 10450115

def getInventory(sku, zip):
  base_url = "https://brickseek.com/walmart-inventory-checker/"
  url_params = {'sku': sku }
  payload = {'search_method': 'sku', 'sku': sku, 'zip': zip, 'sort': 'distance'}
  r = requests.post(base_url, params=url_params, data=payload)
  soup = BeautifulSoup(r.text, 'html.parser')
  table = soup.find('div', class_="bsapi-table")
  rows = table.find_all('div', class_="bsapi-table__row")
  quantities = []
  for row in rows[:-1]:
    quantity_cell = row.find_all('div', class_="bsapi-table__cell")[1]
    quantity = quantity_cell.find('span', class_="bsapi-table__cell-quantity")
    number = [int(s) for s in quantity.get_text().split() if s.isdigit()]
    quantities.append(number[0])
  else:
    address = rows[-1].find_all('address', class_="bsapi-address")[0]
    distanceString = re.search(r'\((.*?)\)', address.get_text(), flags=0)
    distanceMatch = re.search(r'(\d+).?(\d*)', distanceString.group(), flags=0)
    if distanceMatch:
      distance = distanceMatch.group()
    quantity_cell = rows[-1].find_all('div', class_="bsapi-table__cell")[1]
    quantity = quantity_cell.find('span', class_="bsapi-table__cell-quantity")
    number = [int(s) for s in quantity.get_text().split() if s.isdigit()]
    quantities.append(number[0])

  dict = { 'distance' : distance, 'quantities' : quantities}
  return dict
