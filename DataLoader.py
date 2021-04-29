import csv
import re

class DataLoader:
    @staticmethod
    def monthlyData(year: int, month: int) -> [dict()]:
        dicts = []
        with open(f"./data/{year}_{month:02}.csv", "r", encoding="cp1250") as csvfile:
            readerDict = csv.DictReader(csvfile, delimiter=";")
            for row in readerDict:

                #? change money values to use period instead of the comma as the decimal separator,
                #? as well as parse them from string to float types, as these values will be used for numerical purposes

                row["BREME"] = float(row.get("BREME").replace(",", ".")) if not row.get("BREME") == '' else 0
                row["DOBRO"] = float(row.get("DOBRO").replace(",", ".")) if not row.get("DOBRO") == '' else 0
                row["NAMEN"] = row.get("NAMEN").strip()

                #? collect all amazon tags under one name
                if re.match("^AMZN Mktp|^Amazon", row["NAMEN"]):
                    row["NAMEN"] = "AMAZON"

                dicts.append(row)
        return dicts