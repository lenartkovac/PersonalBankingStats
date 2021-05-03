import csv
import re

"""
This class loads the csv files generated by the NKBM's online bank as python dictionaries and persorms some basic filtering to make future processing easier
"""
class DataLoader:
    @staticmethod
    def monthlyData(year: int, month: int, directory="./data") -> [dict()]:
        dicts = []
        if not directory[-1] == '/':
            directory += '/'
        with open(f"{directory}{year}_{month:02}.csv", "r", encoding="cp1250") as csvfile:
            readerDict = csv.DictReader(csvfile, delimiter=";")
            for row in readerDict:

                #? change money values to use period instead of the comma as the decimal separator,
                #? as well as parse them from string to float types, as these values will be used for numerical purposes

                row["BREME"] = float(row.get("BREME").replace(",", ".")) if not row.get("BREME") == '' else 0.0
                row["DOBRO"] = float(row.get("DOBRO").replace(",", ".")) if not row.get("DOBRO") == '' else 0.0

                #? Get rid of spaces in the front or back of the code and convert to all upperstring, for easier processing later on
                row["NAMEN"] = row.get("NAMEN").strip()
                row["NAMEN"] = row.get("NAMEN").upper()

                #? process some commonly appearing data to limit it to only useful information
                if re.match("AMZN|AMAZON", row["NAMEN"]):
                    row["NAMEN"] = "AMAZON"
                if re.match(".*LENKO.JAPAN", row["NAMEN"]):
                    row["NAMEN"] = "SPOTIFY"
                if re.match(".*LAST FM", row["NAMEN"]):
                    row["NAMEN"] = "LASTFM"
                if re.match(".*NETFLIX", row["NAMEN"]):
                    row["NAMEN"] = "NETFLIX"
                if re.match("APPLE.COM/BILL", row["NAMEN"]):
                    row["NAMEN"] = "ICLOUD"
                if re.match("WOLT", row["NAMEN"]):
                    row["NAMEN"] = "WOLT"
                if re.match(".*A1.*", row["NAMEN"]):
                    row["NAMEN"] = "A1"
                if re.match("HOFER", row["NAMEN"]):
                    row["NAMEN"] = "HOFER"
                if re.match("TELEKOM", row["NAMEN"]):
                    row["NAMEN"] = "TELEKOM"
                if re.match("MCDONALDS", row["NAMEN"]):
                    row["NAMEN"] = "MCDONALDS"
                if re.match("POLOG GOTOVINE", row["NAMEN"]):
                    row["NAMEN"] = "POLOG GOTOVINE"

                dicts.append(row)
        return dicts

#! Testing
if __name__ == "__main__":
    data = DataLoader.monthlyData(2021, 2)
    print([x["NAMEN"] for x in data])