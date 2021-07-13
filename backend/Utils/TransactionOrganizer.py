from .DataLoader import DataLoader
import numpy as np
import re
from pymongo import MongoClient
from pprint import pprint
import os
from os.path import dirname
from dotenv import load_dotenv
from pytictoc import TicToc


dotenv_path = os.path.join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_URL = os.environ.get("DB_URL")
DATABASE_PORT = int(os.environ.get("DB_PORT"))

class DBhandler:
    """
    DBhandler is a singleton class that connects to the MongDB database.
    It handles the CRUD operations over the categories.
    """
    _db = MongoClient(DATABASE_URL, DATABASE_PORT).BankDetails
    #_categories = ["shopping", "groceries", "bills", "restaurants", "subscriptions"]
    _categories = _db.list_collection_names()

    @classmethod
    def getCategoryNames(cls):
        return cls._db.list_collection_names()

    @classmethod
    def getCategories(cls):
        categories = {}
        for category in cls.getCategoryNames():
            categories[category] = "|".join([x.get("name")for x in cls._db[category].find()])
        return categories
       
    @classmethod
    def dropCategory(cls, category):
        return cls._db[category].drop()

    @classmethod
    def addToCategory(cls, category: str, newTerm: str):
            cls._db[category].insert_one({"name": newTerm})

    @classmethod
    def delFromCategory(cls, category, term):
        cls._db[category].delete_one({"name": term})


class TransactionManager:
    req_num = 0
    transactions = [None for x in range(12)]

    @classmethod
    def logRequest(cls):
        cls.req_num += 1
        return cls.req_num

    @classmethod
    def printTransactions(cls):
        print(cls.transactions)

    @classmethod
    def getTransactions(cls, index):
        if not cls.transactions[index]:
            cls.transactions[index] = Transactions(2021, index + 1)
        return cls.transactions[index]
        #return Transactions(2021, index + 1)


class Transactions:
    """
    Transactions class loads and stores transaction information for a given month and catogerizes the data based on the categories it receives from the database
    """
    #! Static database client

    def __init__(self, year, month, datadir="data"):
        self.transactions = DataLoader.monthlyData(year, month, datadir)

    def _loadCategories(self):
        print("LOADING CATEGORIES")
        return DBhandler.getCategories()

    @property
    def outgoing_cat(self) -> dict:
        t = TicToc()
        t.tic()
        categories = self._loadCategories()
        categorizedOut = {x: {} for x in categories}
        categorizedOut["other"] = {}

        for transTitle, transValue in self.outgoing.items():
            hasCategory = False
            for category, regex in categories.items():
                if re.fullmatch(regex, transTitle) and not regex == '':
                    categorizedOut[category][transTitle] = transValue
                    hasCategory = True
                    break
            if not hasCategory:
                categorizedOut["other"][transTitle] = transValue
        print(t.toc("Categorization operation took: "))
        return categorizedOut

    @property
    def outgoing(self) -> dict:
        result = {}
        for transaction in [x for x in self.transactions if not x.get("BREME") == 0]:
            if transaction.get("NAMEN") in result:
                result[transaction.get("NAMEN")] += transaction.get("BREME")
            else:
                result[transaction.get("NAMEN")] = transaction.get("BREME")
        return result 

    @property
    def incoming(self) -> dict:
        result = {}
        for transaction in [x for x in self.transactions if not x.get("DOBRO") == 0]:
            if transaction.get("NAMEN") in result:
                result[transaction.get("NAMEN")] += transaction.get("DOBRO")
            else:
                result[transaction.get("NAMEN")] = transaction.get("DOBRO")
        return result 

#! Testing
if __name__ == "__main__":
    #! DBhandler 
    #print(DBhandler._categories)

    ##! Transactions
    monthTest = Transactions(2021, 1, datadir="/Users/lenartkovac/Projects/PersonalBankingStats/data")
    #january._loadCategories()
    pprint(monthTest.outgoing_cat)
    #pprint(january.outgoing_cat)

    ##! TransactionManager
    #TransactionManager.printTransactions()
    #print(TransactionManager.getTransactions(0))
    #print(TransactionManager.getTransactions(3))
    #TransactionManager.printTransactions()