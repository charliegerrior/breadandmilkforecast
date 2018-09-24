import requests
from bs4 import BeautifulSoup

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
  for row in rows:
    cells = row.find_all('div', class_="bsapi-table__cell")
    quantity_cell = cells[1]
    quantity = quantity_cell.find('span', class_="bsapi-table__cell-quantity")
    number = [int(s) for s in quantity.get_text().split() if s.isdigit()]
    quantities.append(number[0])

  return quantities
