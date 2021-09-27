from pymongo.common import CONNECT_TIMEOUT
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

DATABASE_URL = os.environ.get('DB_URL')
DATABASE_PORT = int(os.environ.get('DB_PORT'))
DATABASE_TIMEOUT_MS = int(os.environ.get('DB_TIMEOUT_MS'))

class DBhandler:
    """
    DBhandler is a singleton class that connects to the MongDB database.
    It handles the CRUD operations over the categories.
    """
    _db = MongoClient(DATABASE_URL, DATABASE_PORT, serverSelectionTimeoutMS=DATABASE_TIMEOUT_MS).BankDetails

    @classmethod
    def getCategoryNames(cls):
        #return cls._db.list_collection_names()
        categoryNames = cls._db.list_collection_names()
        categoryNames.append("other")
        return categoryNames
        #return cls._db.list_collection_names().append("other")

    @classmethod
    def getCategories(cls):
        categories = {}
        for category in cls._db.list_collection_names():
            categories[category] = "|".join([x.get("name")for x in cls._db[category].find()])
        return categories
       
    @classmethod
    def dropCategory(cls, category):
        return cls._db.drop_collection(category)

    @classmethod
    def addToCategory(cls, category: str, newTerm: str, session=None):
            cls._db[category].insert_one({"name": newTerm}, session=session)

    @classmethod
    def delFromCategory(cls, category, term, session=None):
        cls._db[category].delete_one({"name": term}, session=session)


class Transactions:
    """
    Transactions class loads and stores transaction information for a given month and catogerizes the data based on the categories it receives from the database
    """
    #! Static database client

    def __init__(self, year, month, datadir="data"):
        self._year = year
        self._month = month
        self.transactions = DataLoader.monthlyData(year, month, datadir)
    
    def __str__(self):
        return f"Transactions for {self._year}.{self._month:02}"

    def __repr__(self):
        return self.__str__()

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

class TransactionManager:
    transactions = {}

    @classmethod
    def printTransactions(cls):
        print(cls.transactions)

    @classmethod
    def getTransactions(cls, year: int, month: int, datadir="data") -> Transactions:
        if not cls.transactions.get(year):
            cls.transactions[year] = {}

        if not cls.transactions[year].get(month):
            cls.transactions[year][month] = Transactions(year, month, datadir)

        return cls.transactions[year][month]


#! Testing
if __name__ == "__main__":
    #! DBhandler 
    #print(DBhandler._categories)

    ##! Transactions
    #monthTest = Transactions(2021, 1, datadir="/Users/lenartkovac/Projects/PersonalBankingStats/data")
    #january._loadCategories()
    #pprint(monthTest.outgoing_cat)
    #pprint(january.outgoing_cat)

    ##! TransactionManager
    TransactionManager.printTransactions()
    print(TransactionManager.getTransactions(2021, 1, '../../data'))
    print(TransactionManager.getTransactions(2020, 3, '../../data'))
    TransactionManager.printTransactions()