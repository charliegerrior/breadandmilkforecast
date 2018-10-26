import requests
from bs4 import BeautifulSoup
import re

staples = {'milk' : 10450115, 'eggs' : 145051970, 'bread' : 120099533, 'tp' : 549419637}

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

def getStats(dict):
  quantities = dict['quantities']
  mean = sum(quantities)/len(quantities)

  oos = 0
  for quantity in quantities:
    if quantity == 0:
      oos+=1
  oos_pct = (oos/len(quantities)) * 100

  item = { 'mean' : int(round(mean)), 'percent' : int(round(oos_pct)), 'distance' : round(float(dict['distance'])) }

  return item

def getForecast(region):

  forecast = { 'region' : region, 'bread' : getStats(getInventory(staples['bread'],region)), 'eggs' : getStats(getInventory(staples['eggs'],region)), 'milk' : getStats(getInventory(staples['milk'],region)), 'tp' : getStats(getInventory(staples['tp'],region)) }

  return forecast
