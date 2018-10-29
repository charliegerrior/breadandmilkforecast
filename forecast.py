import requests
from bs4 import BeautifulSoup
import re

from app import db
from app.models import Forecast

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

def addForecast(forecast):
  db_forecast = Forecast(region = forecast["region"], bread_mean = forecast["bread"]["mean"], bread_percent = forecast["bread"]["percent"], bread_distance = forecast["bread"]["distance"], eggs_mean = forecast["eggs"]["mean"], eggs_percent = forecast["eggs"]["percent"], eggs_distance = forecast["eggs"]["distance"], milk_mean = forecast["milk"]["mean"], milk_percent = forecast["milk"]["percent"], milk_distance = forecast["milk"]["distance"], tp_mean = forecast["tp"]["mean"], tp_percent = forecast["tp"]["percent"], tp_distance = forecast["tp"]["distance"])
  db.session.add(db_forecast)
  db.session.commit()

def updateForecast(db_forecast, forecast):
  db_forecast.timestamp = datetime.utcnow()
  db_forecast.eggs_mean = forecast["eggs"]["mean"]
  db_forecast.eggs_percent = forecast["eggs"]["percent"]
  db_forecast.eggs_distance = forecast["eggs"]["distance"]
  db_forecast.bread_mean = forecast["bread"]["mean"]
  db_forecast.bread_percent = forecast["bread"]["percent"]
  db_forecast.bread_distance = forecast["bread"]["distance"]
  db_forecast.milk_mean = forecast["milk"]["mean"]
  db_forecast.milk_percent = forecast["milk"]["percent"]
  db_forecast.milk_distance = forecast["milk"]["distance"]
  db_forecast.tp_mean = forecast["tp"]["mean"]
  db_forecast.tp_percent = forecast["tp"]["percent"]
  db_forecast.tp_distance = forecast["tp"]["distance"]
  db.session.commit()

def convertForecast(db_forecast):
  forecast = { 'region' : db_forecast.region, 'bread' : { 'mean' : db_forecast.bread_mean, 'percent' : db_forecast.bread_percent, 'distance' : db_forecast.bread_distance }, 'eggs' : { 'mean' : db_forecast.eggs_mean, 'percent' : db_forecast.eggs_percent, 'distance' : db_forecast.eggs_distance }, 'milk' : { 'mean' : db_forecast.milk_mean, 'percent' : db_forecast.milk_percent, 'distance' : db_forecast.milk_distance }, 'tp' : { 'mean' : db_forecast.tp_mean, 'percent' : db_forecast.tp_percent, 'distance' : db_forecast.tp_distance } }

  return forecast
