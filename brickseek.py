import requests
from bs4 import BeautifulSoup
import numpy as np

def getInventory(sku, zip):
  base_url = "https://brickseek.com/walmart-inventory-checker/"
  url_params = {'sku': sku }
  payload = {'search_method': 'sku', 'sku': sku, 'zip': zip, 'sort': 'distance'}
  r = requests.post(base_url, params=url_params, data=payload)

  #print(r.text)

  soup = BeautifulSoup(r.text, 'html.parser')
  table = soup.find('div', class_="bsapi-table")
  rows = table.find_all('div', class_="bsapi-table__row")
  quantities = []
  for row in rows:
    cells = row.find_all('div', class_="bsapi-table__cell")
    quantity_cell = cells[1]
    quantity = quantity_cell.find('span', class_="bsapi-table__cell-quantity")
    print(quantity.get_text())
    number = [int(s) for s in quantity.get_text().split() if s.isdigit()]
    quantities.append(number[0])

  print(quantities)
  oos = 0
  for quantity in quantities:
    if quantity == 0:
      oos+=1
  print oos
  #oos percentage using len(quantities)
  quantities = np.array(quantities)
  print(np.mean(quantities))
  print(np.std(quantities))


getInventory(10450115,28445)

#TODO
#statistics
#parse result
#bread SKU: 13033157
#eggs SKU: 145051970
#milk SKU: 10450115
