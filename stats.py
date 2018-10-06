def getStats(dict):
  quantities = dict['quantities']
  mean = sum(quantities)/len(quantities)

  oos = 0
  for quantity in quantities:
    if quantity == 0:
      oos+=1

  oos_pct = oos/len(quantities) * 100

  item = { 'mean' : '%d' % round(mean), 'percent' : '%d' % round(oos_pct), 'distance' : dict['distance'] }

  return item
