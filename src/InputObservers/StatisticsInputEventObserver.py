import os
import json
from datetime import datetime
from InputObservers.InputObserver import InputObserver
from decorators.overrides import overrides

class StatisticsInputEventObserver(InputObserver):
	"""This is the default observer for input events."""
	
	def __init__(self):
		super(InputObserver, self).__init__()

		self.log_tag = '[StatisticsInputEventObserver]'
		self.stats = None
		self.current_q_and_a_identifier = None

		self.incorrect_counts = {}

		self.load_statistics()

	@overrides(InputObserver)
	def update_on_show_all(self):
		# print(self.log_tag, 'show all called')
		pass

	@overrides(InputObserver)
	def update_on_deactivate(self, question_number):
		# print(self.log_tag, 'deactivate called')
		today = datetime.now().strftime('%Y-%m-%d')
		question_number = str(question_number)
		
		if today not in self.stats:
			print(self.log_tag, 'creating new date entry')
			self.create_new_date_entry(today)

		if self.current_q_and_a_identifier not in self.stats[today]:
			print(self.log_tag, 'creating new q_and_a_identifier entry')
			self.create_new_q_and_a_entry(today, self.current_q_and_a_identifier)

		if question_number not in self.stats[today][self.current_q_and_a_identifier]['deactivated']:
			self.create_new_deactivated_entry(today, self.current_q_and_a_identifier, question_number)

		self.stats[today][self.current_q_and_a_identifier]['count'] += 1
		self.stats[today][self.current_q_and_a_identifier]['deactivated'][question_number] += 1

	@overrides(InputObserver)
	def update_on_correct(self, question_number):
		# print(self.log_tag, 'correct called')
		today = datetime.now().strftime('%Y-%m-%d')
		question_number = str(question_number)

		if today not in self.stats:
			self.create_new_date_entry(today)

		if self.current_q_and_a_identifier not in self.stats[today]:
			self.create_new_q_and_a_entry(today, self.current_q_and_a_identifier)

		if question_number not in self.stats[today][self.current_q_and_a_identifier]['correct']:
			self.create_new_correct_entry(today, self.current_q_and_a_identifier, question_number)

		self.stats[today][self.current_q_and_a_identifier]['count'] += 1
		self.stats[today][self.current_q_and_a_identifier]['correct'][question_number] += 1

	@overrides(InputObserver)
	def update_on_incorrect(self, question_number):
		# print(self.log_tag, 'incorrect called')
		today = datetime.now().strftime('%Y-%m-%d')
		question_number = str(question_number)

		if today not in self.stats:
			self.create_new_date_entry(today)

		if self.current_q_and_a_identifier not in self.stats[today]:
			self.create_new_q_and_a_entry(today, self.current_q_and_a_identifier)

		if question_number not in self.stats[today][self.current_q_and_a_identifier]['incorrect']:
			self.create_new_incorrect_entry(today, self.current_q_and_a_identifier, question_number)

		self.stats[today][self.current_q_and_a_identifier]['count'] += 1
		self.stats[today][self.current_q_and_a_identifier]['incorrect'][question_number] += 1

	@overrides(InputObserver)
	def update_on_load_training_state(self, file_path, question_set_identifier):
		# print(self.log_tag, 'load called')
		today = datetime.now().strftime('%Y-%m-%d')
		self.current_q_and_a_identifier = question_set_identifier

		if today not in self.stats:
			self.create_new_date_entry(today)

		if self.current_q_and_a_identifier not in self.stats[today]:
			self.create_new_q_and_a_entry(today, self.current_q_and_a_identifier)

	@overrides(InputObserver)
	def update_on_save_training_state(self, file_path, question_set_identifier):
		# print(self.log_tag, 'save called')
		pass

	@overrides(InputObserver)
	def update_on_show_help(self):
		# print(self.log_tag, 'help called')
		pass

	@overrides(InputObserver)
	def update_on_show_stats(self):
		# print(self.log_tag, 'stats called')
		pass

	@overrides(InputObserver)
	def update_on_exit(self):
		print(self.log_tag, 'exit called')
		# print(json.dumps(self.stats, ensure_ascii=False, indent='\t', sort_keys=True))
		self.save_statistics()

	@overrides(InputObserver)
	def update(self):
		"""general update method for any kind of event"""
		# print(self.log_tag, 'any method called')
		pass

	def load_statistics(self):
		file_path = 'data' + os.path.sep + 'stats.json'
		try:
			with open(file_path, 'r') as input_file:
				self.stats = json.load(input_file)
		except Exception as e:
			print(self.log_tag, 'Error while reading stats. Is the file not readable?')
			raise e

	def save_statistics(self):
		file_path = 'data' + os.path.sep + 'stats.json'
		try:
			with open(file_path, 'w') as output_file:
				json.dump(self.stats, output_file, ensure_ascii=False, indent='\t', sort_keys=True)
		except Exception as e:
			print(self.log_tag, 'Error while saving stats. Is the file not writable?')
			raise e

	def create_new_date_entry(self, date):
		self.stats[date] = {}

	def create_new_q_and_a_entry(self, date, q_and_a_identifier):
		self.stats[date][q_and_a_identifier] = {
			'count': 0,
			'deactivated': {},
			'correct': {},
			'incorrect': {},
		}

	def create_new_incorrect_entry(self, date, q_and_a_identifier, question_number):
		self.stats[date][q_and_a_identifier]['incorrect'][question_number] = 0

	def create_new_correct_entry(self, date, q_and_a_identifier, question_number):
		self.stats[date][q_and_a_identifier]['correct'][question_number] = 0

	def create_new_deactivated_entry(self, date, q_and_a_identifier, question_number):
		self.stats[date][q_and_a_identifier]['deactivated'][question_number] = 0

	# def update_most_difficult_questions(self):
	# 	"""This method updates the keys of the most difficult questions in the stats dictionary, 
	# 	by looking up, which questions have the highest incorrectly answered counts."""
	# 	maximum_questions = 3

	# 	# recalculate the most difficult questions
	# 	sorted_counts = list(self.incorrect_counts.values())
	# 	sorted_counts.sort()
	# 	highest_counts = sorted_counts[-maximum_questions:]
		
	# 	found = 0
	# 	most_difficult_questions_keys = []
	# 	for key,value in self.incorrect_counts.items():
	# 		if found == maximum_questions:
	# 			break
	# 		if value == highest_counts[0]:
	# 			most_difficult_questions_keys.append(key)
	# 			found += 1

	# 	today = datetime.now().strftime('%Y-%m-%d')
		
	# 	if today not in self.stats:
	# 		self.create_new_date_entry(today)

	# 	if self.current_q_and_a_identifier not in self.stats[today]:
	# 		self.create_new_q_and_a_entry(today, self.current_q_and_a_identifier)

	# 	self.stats[today][self.current_q_and_a_identifier]['most_difficult'] = most_difficult_questions_keys