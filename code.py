from DataLoader import DataLoader as dl
import numpy as np

months = [1, 2, 3, 4]

transferData = [dl.monthlyData(2021, x) for x in months]

bremena = []

for monthlyData in transferData:
    monthlyBreme = {}
    for breme in [x for x in monthlyData if not x.get("BREME") == 0]:
        if breme.get("NAMEN") in monthlyBreme:
            monthlyBreme[breme.get("NAMEN")] += breme.get("BREME")
        else:
            monthlyBreme[breme.get("NAMEN")] = breme.get("BREME")
    bremena.append(monthlyBreme)



#print(february)
#print([(x.get("NAMEN"), x.get("BREME")) for x in february if not x.get("BREME") == ''])
#print([x.get("NAMEN") for x in march if not x.get("BREME") == ''])
#print([x.get("NAMEN") for x in april if not x.get("BREME") == ''])