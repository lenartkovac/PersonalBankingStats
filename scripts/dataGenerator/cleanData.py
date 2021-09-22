
import os
import sys
from datetime import date
from Utils import DataGenerator

yearRange = 10

def processCommandParams(params):

	dataDir = 'data'

	for param in params:
		if param.startswith('dataDir'):
			dataDir = param.split('=')[1]


	files = sorted(
		map(lambda x: int(x), 
			filter(lambda x: x.isnumeric(), os.listdir(dataDir))
		))

	if len(files) < 1:
		startYear = 0
		endYear = -1
	else:
		startYear = files[0]
		endYear = files[-1]

	for param in params:
		
		if param.startswith('startYear'):
			startYear = int(param.split('=')[1])

		if param.startswith('endYear'):
			endYear = int(param.split('=')[1])

	print(f'Input Params:')
	print(f'\tdataDir: {dataDir}')
	print(f'\tstartYear: {startYear}')
	print(f'\tendYear: {endYear}')
	print('-' * 30)

	return dataDir, startYear, endYear


def main():

	dataDir, startYear, endYear, = processCommandParams(sys.argv)

	for year in range(startYear, endYear + 1):
		path = os.path.join(dataDir, str(year))
		print(path, end=": ")

		try:
			if os.path.exists(path):
				for file in os.listdir(path):
					os.remove(os.path.join(path, file))

				os.rmdir(path)
				print('Deleted successfully')
			else:
				print('Not Deleted: Does not Exist!')
		except Exception as e:
			print('Not Deleted: Error occured ', e)
	print('Deleting finished')
			


if __name__ == '__main__':
	main()
