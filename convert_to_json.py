import json
import os

def main():
	german = []
	hanzi = []
	pinyin = []

	with open('data' + os.path.sep + 'HSK2 German', 'r') as input_file:
		for line in input_file:
			german.append(line.strip())

	with open('data' + os.path.sep + 'HSK2 Hanzi', 'r') as input_file:
		for line in input_file:
			hanzi.append(line.strip())

	with open('data' + os.path.sep + 'HSK2 Pinyin', 'r') as input_file:
		for line in input_file:
			pinyin.append(line.strip())

	vocables = []

	for index, question in enumerate(german):
		vocables.append({
			'question':german[index],
			'answer':hanzi[index],
			'info':pinyin[index]
		})

	hsk = {
		'identifier': 'HSK2',
		'questions': vocables
	}

	with open('data' + os.path.sep + 'HSK2.json', 'w') as output_file:
		json.dump(hsk, output_file, ensure_ascii=False, indent='\t', sort_keys=True)

	with open('data' + os.path.sep + 'HSK2.json', 'r') as input_file:
		hsk = json.load(input_file)

	for index, voc in enumerate(hsk['questions']):
		print('VOC #'+str(index), voc)

if __name__ == '__main__':
	main()