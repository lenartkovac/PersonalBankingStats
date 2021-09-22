import os
import sys
from datetime import date
from Utils import DataGenerator

yearRange = 10

def processCommandParams(params):

	overwriteFiles = False
	dataDir = 'data'
	endYear = date.today().year
	endMonth = date.today().month
	startMonth = 1
	startYear = endYear - 10

	for param in params:
		if param.startswith('overwriteFiles'):
			overwriteFiles = bool(param.split('=')[1])

		if param.startswith('dataDir'):
			dataDir = param.split('=')[1]
		
		if param.startswith('startYear'):
			startYear = int(param.split('=')[1])

		if param.startswith('endYear'):
			endYear = int(param.split('=')[1])

		if param.startswith('startMonth'):
			startMonth = int(param.split('=')[1])

		if param.startswith('endMonth'):
			endMonth = int(param.split('=')[1])

	print(f'Input Params:')
	print(f'\tdataDir: {dataDir}')
	print(f'\tstartYear: {startYear}')
	print(f'\tendYear: {endYear}')
	print(f'\tstartMonth: {startMonth}')
	print(f'\tendMonth: {endMonth}')
	print(f'\toverwriteFiles: {overwriteFiles}')
	print('-' * 30)

	return dataDir, startYear, startMonth, endYear, endMonth, overwriteFiles


def main():

	dataDir, startYear, startMonth, endYear, endMonth, overwriteFiles = processCommandParams(sys.argv)

	if not os.path.exists(dataDir):
		os.mkdir(dataDir)

	for year in range(startYear, endYear + 1):
		path = os.path.join(dataDir, str(year))
		print(path)

		if not os.path.exists(path):
			os.mkdir(path)

		maxMonth = endMonth if year == endYear else 12
		for month in range(startMonth, maxMonth + 1):
			fileName = f'{year}_{month:02}.csv'
			filePath = os.path.join(path, fileName)

			if overwriteFiles and os.path.exists(filePath):
				os.remove(filePath)
			
			DataGenerator.generateFile(fileName, path)


if __name__ == '__main__':
	main()
