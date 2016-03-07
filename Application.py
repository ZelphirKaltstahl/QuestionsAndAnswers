import sys
import random
from collections import namedtuple
from Helper import truncate_number
from xml_parser.XMLParserException import XMLParserException
from FileReader import FileReader
from Statistic import Statistic
from TrainingState import TrainingState
from DefaultInputEventObserver import DefaultInputEventObserver

class Application:
	"""docstring for Application"""

	def __init__(self, q_and_a_file_path):
		super(Application, self).__init__()
		self.log_tag = '[STATUS: Application]'

		self.file_reader = FileReader()
		
		# TRAINING STATE
		self.state = TrainingState()
		self.state.q_and_a_file_path = q_and_a_file_path

		# Q&A Data
		self.state.q_and_a = self.file_reader.read_json(q_and_a_file_path)

		# Publish Subscribe
		self.input_event_subscribers = []
		new_subscriber = DefaultInputEventObserver()
		self.register_input_event_subscriber(new_subscriber)

	def run(self):
		self.quiz()

	def load_state(self, ask_file_name=False):
		if ask_file_name:
			file_name = input('Enter a file name (default: training_state):')
			if file_name == '':
				file_name = 'training'  # if the user enters nothing use default value
		else:
			file_name = 'training_state'  # set to default file name
		file_name = 'data/' + file_name
		file_name += '_state.json'  # always add file ending

		self.state.load(file_name)

	def save_state(self, ask_file_name=False):
		if ask_file_name:
			file_name = input('Enter a file name (default: training_state):')
			if file_name == '':
				file_name = 'training'  # if the user enters nothing use default value
		else:
			file_name = 'training'
		file_name = 'data/' + file_name
		file_name += '_state.json'  # always add file ending
			
		self.state.save(file_name)


	def print_help(self):
		print(
			'\nAvailable commands:',
			'all:print all',
			'd:deactivate',
			'?:help',
			'+:mark correctly answered',
			'-:mark wrongly answered',
			'save/write/persist:save training state',
			'load/read/restore:load training state',
			'stats:print statistics\n',
			'exit:exit',
			sep='\n',
			end='\n'
		)

	def get_random_index(self):
		random_index = random.randint(0, len(self.state.q_and_a['questions'])-1)
		while random_index in self.state.deactivated_questions:
			random_index = random.randint(0, len(self.state.q_and_a['questions'])-1)
		return random_index

	# this method could be refactored to use dict of action objects, which implement an ABC with a required method execute, which executes the actions on specific inputs
	def ask(self):
		random_index = self.get_random_index()
		self.state.training_process.append('?')

		while(True):
			input("Translate: \"" + self.state.q_and_a['questions'][random_index]['question'] + "\"")
			print('Answer: ', self.state.q_and_a['questions'][random_index]['answer'], ' (', self.state.q_and_a['questions'][random_index]['info'], ')', sep='')
			user_input = input("Command ('?' for help):").lower()

			if user_input == "d":
				self.state.training_process[-1] = 'd'
				self.state.deactivated_questions.append(random_index)
				print(self.log_tag, 'Question deactivated.')
				return
			elif user_input == "all":
				self.print_all()
				return
			elif user_input == 'exit': sys.exit(0)
			elif user_input == '?': self.print_help()
			elif user_input == '+':
				self.state.training_process[-1] = '+'
				return
			elif user_input == '-':
				self.state.training_process[-1] = '-'
				return
			elif user_input in ['load', 'read', 'restore']:
				self.load_state(ask_file_name=True)
				if random_index in self.state.deactivated_questions:
					random_index = self.state.get_random_index()
			elif user_input in ['save', 'write', 'persist']: self.save_state(ask_file_name=True)
			elif user_input == 'stats': Statistic.print_stats(self.state.training_process)
			
			self.notify_input_event_subscribers(user_input, self.q_and_a.)  # TODO

	def quiz(self):
		print('\n' + self.log_tag, 'Starting quiz ...', end='\n\n')
		while(True):
			try:
				if len(self.state.deactivated_questions) < len(self.state.q_and_a['questions']):
					self.ask() # here the input logic is happening
					Statistic.print_result(self.state.training_process)
				else:
					print(self.log_tag, 'All questions deactivated. Exiting now...')
					sys.exit(0)
			
			except (KeyboardInterrupt, EOFError) as interrupt:
				print()
				self.save_state()
				print(self.log_tag, 'Exiting application ...')
				sys.exit(0)

	def print_all(self):
		for index, question in enumerate(self.state.q_and_a['questions']):
			print('\nquestion #', index, ':', sep='')
			for key,val in question.items():
				print("{} : {}".format(key, val))

	def register_input_event_subscriber(self, subscriber):
		self.input_event_subscribers.append(subscriber)

	def notify_input_event_subscribers(self, file_path, question_number, question_set_identifier, event=None):
		if event == None:
			for subscriber in self.input_event_subscribers:
				subscriber.update()
		else:
			for subscriber in self.input_event_subscribers:
				if user_input == '+':
					subscriber.update_on_correct(question_number)
				elif user_input == '-':
					subscriber.update_on_incorrect(question_number)
				elif user_input == 'd':
					subscriber.update_on_deactivate(question_number)
				elif user_input == '?':
					subscriber.update_on_show_help()
				elif user_input == 'all':
					subscriber.update_on_show_all()
				elif user_input == 'stats':
					subscriber.update_on_show_stats()
				elif user_input in ['load', 'read', 'restore']:
					subscriber.update_on_load_training_state(file_path, question_set_identifier)
				elif user_input in ['save', 'write', 'persist']:
					subscriber.update_on_save_training_state(file_path, question_set_identifier)
				elif user_input == 'exit':
					subscriber.update_on_exit()
				
	def unsubscribe_input_event_subscriber(self, subscriber):
		del self.input_event_subscribers[subscriber]
				
				
				
				

