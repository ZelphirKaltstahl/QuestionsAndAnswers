import json
from datetime import datetime

class StatisticsWriter:
	"""docstring for StatisticsWriter"""
	def __init__(self):
		super(StatisticsWriter, self).__init__()
		
	def save(self):
		today = datetime.now().strftime('%Y-%m-%d')

		a = {
			today: {
				'HSK1': {
					'count':97,
					'correct':20,
					'incorrect':77,
					'most_difficult':10,
					'learned':15
				},
				'HSK2': {
					'count':23,
					'correct':20,
					'incorrect':3,
					'most_difficult':13,
					'learned':12
				}
			}
		}

		print(a[today].keys())

		with open('stats.json', 'w') as stats_file:
			json.dump(a, stats_file, ensure_ascii=False, indent=4)

		with open('stats.json', 'r') as stats_file:
			b = json.load(stats_file)		

		assert a == b, 'test'

		print(b[today].keys())

if __name__ == '__main__':
	writer = StatisticsWriter()
	writer.save()