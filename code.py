from DataLoader import DataLoader as dl
import numpy as np
import re


def categorizeTransfers(monthlyTransfers):
    categories = {
        "shopping": "AMAZON|MIMOVRSTE",
        "groceries": ".*OSTROZNO|HIPERMARKET|INTERSPAR|HOFER",
        "bills": "TELEKOM|A1",
        "restaurants": "WOLT|MCDONALDS|.*LIMBO.*",
        "subscriptions": "NETFLIX|WANIKANI|LASTFM|SPOTIFY|ICLOUD"
    }
    categorizedData = {x: [] for x in categories}
    categorizedData["other"] = []

    for transferTitle, transferValue in monthlyTransfers.items():
        hasCategory = False
        for category, regexCheck in categories.items():
            if re.match(regexCheck, transferTitle):
                categorizedData[category].append((transferTitle, transferValue))
                hasCategory = True
                break
        if not hasCategory:
            categorizedData["other"].append((transferTitle, transferValue))


    return categorizedData




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


print(categorizeTransfers(bremena[3]))