import sys
import random
import os

class DataGenerator:
	income =  '1;SI56040010034522289;SI56040010034522289;22.01.2021;22.01.2021;100,00;;EUR;POLOG GOTOVINE BA01172N;;;;;;;;'
	outcome = '1;SI56040010034522289;SI56040010034522289;02.02.2021;30.01.2021;;29,95;EUR;PAYPAL *PADDLE.COM;;;;KOVA� LENART;;;;'

	@staticmethod
	def _getMonthMaxDay(month: int) -> int:
		return {
			1: 31,
			2: 28,
			3: 31,
			4: 30,
			5: 31,
			6: 30,
			7: 31,
			8: 31,
			9: 30,
			10: 31,
			11: 30,
			12: 31
		}.get(month, -1)

	@staticmethod
	def _getRandomIncomingTitle():
		incomeStatements = [
			'salary',
			'income',
			'payback from friend',
			'refund'
		]
		return incomeStatements[random.randint(0, len(incomeStatements) - 1)]

	@staticmethod
	def _getRandomOutgoingTitle():
		outcomeStatement = [
			'Grocery store A',
			'Grocery store B',
			'Grocery store C',
			'Gas station',
			'Train ticket',
			'Bus ticket',
			'Gas bill',
			'Water bill',
			'Electric bill',
			'Phone bill',
			'Internet bill',
			'Car repair',
			'Sports store A',
			'Sports store B',
			'Sports store C',
			'Clothing store A',
			'Clothing store B',
			'Clothing store C',
			'Movie Streaming service',
			'Birthday present',
			'Anniversary gift',
			'GYM subscription',
			'Movie tickets',
			'Restaurant A',
			'Restaurant B',
			'Restaurant C',
			'Pet store A',
			'Pet store B',
			'Pet store C',
			'Bar A',
			'Bar B',
			'Bar C'
		]
		return outcomeStatement[random.randint(0, len(outcomeStatement) - 1)]


	@staticmethod
	def _validateInput(fileName: str, path: str):
		if len(fileName) < 1:
			print(f'ERROR: FileName \'{fileName}\' cannot be empty')
			sys.exit(1)

		if len(path) < 1:
			print('ERROR: path name cannot be empty')
			sys.exit(1)

		if not os.path.exists(path):
			print(f'ERROR: path \'{path}\' does not exist')
			sys.exit(1)


	@classmethod
	def _generateLine(cls, date: str, ratio=0.7) -> str:
		IBAN = 'SI12345679087654321'
		amount = round(random.random() * random.randint(1, 1000), 2)

		if random.random() > ratio:
			return f'1;{IBAN};{IBAN};{date};{date};{amount};;EUR;{cls._getRandomIncomingTitle()};;;;;;;;'
		else:
			return f'1;{IBAN};{IBAN};{date};{date};;{amount};EUR;{cls._getRandomOutgoingTitle()};;;;Test User;;;;'


	@classmethod
	def generateFile(cls, fileName: str, path: str):

		cls._validateInput(fileName, path)

		if not fileName[-4:] == '.csv':
			fileName += '.csv'

		filePath = os.path.join(path, fileName)


		if os.path.exists(filePath):
			print(f'ERROR: File \'{filePath}\' already exists, exiting...')
			return

		header = '�T. IZPISKA;POGODBA;RA�UN;DATUM KNJI�ENJA;DATUM VALUTE;DOBRO;BREME;VALUTA;NAMEN;SKLIC V DOBRO;SKLIC V BREME;UDELE�ENEC - RA�UN;UDELE�ENEC - NAZIV;UDELE�ENEC - BIC;KODA NAMENA;PRILIV V IZVORNI VALUTI;ODLIV V IZVORNI VALUTI;IZVORNA VALUTA\n'
		year = int(fileName[0:4])
		month = int(fileName[5:7])
		ratio = 0.7
		maxDay = cls._getMonthMaxDay(month)

		days = sorted([random.randint(1, maxDay) for x in range(random.randint(15, 60))])
		try:
			with open(filePath, 'x') as file:
				file.write(header)
				for day in days:
					date = f'{day:02}.{month:02}.{year:04}'
					file.write(cls._generateLine(date, ratio)+'\n')
			print(f'Successfully created {filePath}')

		except Exception as e:
			print(f'Error occured: {e}. Aborting')
			if (os.path.exists(filePath)):
				os.remove(f'{filePath}')
				sys.exit(1)

		finally:
			print(f'DataGenerator finished creating {filePath}. Exiting...')


def main():
	path = '.'
	name = '2021_01'
	if len(sys.argv) > 1:
		name = sys.argv[1]

	if len(sys.argv) > 2:
		path = sys.argv[2]

	DataGenerator.generateFile(name, path)
	

if __name__ == '__main__':
	main()