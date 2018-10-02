def getStats(quantities):
  mean = sum(quantities)/len(quantities)

  oos = 0
  for quantity in quantities:
    if quantity == 0:
      oos+=1

  oos_pct = oos/len(quantities) * 100

  item = { 'mean' : round(mean), 'percent' : round(oos_pct) }

  return item
