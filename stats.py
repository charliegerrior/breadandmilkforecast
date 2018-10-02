from __future__ import division
import numpy as np

def getStats(quantities):
  np_quantities = np.array(quantities)
  mean = np.mean(np_quantities)
  #std = np.std(np_quantities)

  oos = 0
  for quantity in quantities:
    if quantity == 0:
      oos+=1

  oos_pct = oos/len(quantities) * 100

  item = { 'stores' : len(quantities), 'oos' : oos, 'mean' : "%d" % round(mean), 'percent' : round(oos_pct) }

  return item
