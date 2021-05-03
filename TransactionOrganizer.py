from DataLoader import DataLoader as dl
import numpy as np
import re

"""
TransactionOrganizer class is used to identify and group together transaction at same businesses,
as well as group them into meaningful categories which give the numbers some qualitative value
"""

class TransactionOrganizer:
    @staticmethod
    def categorizeOutgoingTraffic(transactions: dict) -> dict:
        categories = {
            "shopping": "AMAZON|MIMOVRSTE",
            "groceries": ".*OSTROZNO|HIPERMARKET|INTERSPAR|HOFER",
            "bills": "TELEKOM|A1",
            "restaurants": "WOLT|MCDONALDS|.*LIMBO.*",
            "subscriptions": "NETFLIX|WANIKANI|LASTFM|SPOTIFY|ICLOUD"
        }
        categorizedData = {x: {} for x in categories}
        categorizedData["other"] = {}

        for transTitle, transValue in transactions.items():
            hasCategory = False
            for category, regexCheck in categories.items():
                if re.match(regexCheck, transTitle):
                    categorizedData[category][transTitle] = transValue
                    hasCategory = True
                    break
            if not hasCategory:
                categorizedData["other"][transTitle] = transValue
        return categorizedData

    @staticmethod
    def gatherOutgoingTraffic(transactions: dict) -> dict:
        summary = {}
        for transaction in [x for x in transactions if not x.get("BREME") == 0]:
            if transaction.get("NAMEN") in summary:
                summary[transaction.get("NAMEN")] += transaction.get("BREME")
            else:
                summary[transaction.get("NAMEN")] = transaction.get("BREME")
        return summary

    @staticmethod
    def gatherIncomingTraffic(transactions: dict) -> dict:
        summary = {}
        for transaction in [x for x in transactions if not x.get("DOBRO") == 0]:
            if transaction.get("NAMEN") in summary:
                summary[transaction.get("NAMEN")] += transaction.get("DOBRO")
            else:
                summary[transaction.get("NAMEN")] = transaction.get("DOBRO")
        return summary


#! Testing
if __name__ == "__main__":
    months = [1, 2, 3, 4]
    transferData = [dl.monthlyData(2021, x) for x in months]

    bremena = [TransactionOrganizer.gatherOutgoingTraffic(x) for x in transferData]
    dobro = [TransactionOrganizer.gatherIncomingTraffic(x) for x in transferData]
    for month in bremena:
        print(month)
        print('-' * 30)

    print('-' * 30)

    for month in dobro:
        print(month)
        print('-' * 30)

    organizedData = TransactionOrganizer.categorizeOutgoingTraffic(bremena[0])
    #print(organizedData)

    for category, value in organizedData.items():
        print(f"{category}: {value}")
