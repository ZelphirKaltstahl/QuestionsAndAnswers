import sys, os
import random
from collections import namedtuple

from xml_parser.XMLParserException import XMLParserException
from FileReader import FileReader
from Statistic import Statistic
from TrainingState import TrainingState

from InputObservers.ChartGenerator import ChartGenerator
from InputObservers.DefaultInputEventObserver import DefaultInputEventObserver
from InputObservers.StatisticsInputEventObserver import StatisticsInputEventObserver

from helpers.number_helper import truncate_number

class Application:
	"""docstring for Application"""

	def __init__(self, q_and_a_file_path):
		super(Application, self).__init__()
		self.log_tag = '[STATUS: Application]'

		self.file_reader = FileReader()
		
		# TRAINING STATE
		self.state = TrainingState()
		self.state.q_and_a_file_path = q_and_a_file_path

		# Publish Subscribe
		self.input_event_subscribers = []

		print(self.log_tag, 'adding subscribers for input events')
		new_subscriber = DefaultInputEventObserver()
		self.register_input_event_subscriber(new_subscriber)
		print(self.log_tag, 'default input observer added as subscriber for input events')
		
		new_statistics_input_subscriber = StatisticsInputEventObserver()
		self.register_input_event_subscriber(new_statistics_input_subscriber)
		print(self.log_tag, 'statistics input subscriber added as subscriber for input events')

		chart_generator = ChartGenerator()
		self.register_input_event_subscriber(chart_generator)
		print(self.log_tag, 'chart generator added as subscriber for input events')


		# Q&A Data
		self.state.q_and_a = self.file_reader.read_json(q_and_a_file_path)
		self.notify_input_event_subscribers(
			self.state.q_and_a_file_path, 0, self.state.q_and_a['identifier'], event='load'
		)

	def run(self):
		self.quiz()

	def load_state(self, ask_file_name=False):
		file_name = 'training'  # set to default file name
		
		if ask_file_name:
			file_name = input('Enter a file name (default: training_state):')
			if file_name == '':
				file_name = 'training'  # if the user enters nothing use default value
		
		file_path = self.extend_data_file_path(file_name, state=True)
		self.state.load(file_path)

	def save_state(self, ask_file_name=False):
		file_name = 'training'

		if ask_file_name:
			file_name = input('Enter a file name (default: training_state):')
			if file_name == '':
				file_name = 'training'  # if the user enters nothing use default value
		
		file_path = self.extend_data_file_path(file_name, state=True)
			
		self.state.save(file_path)

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

	def ask(self):
		random_index = self.get_random_index()
		self.state.training_process.append('?')

		question_answered = False
		while(not question_answered):
			input("Translate: \"" + self.state.q_and_a['questions'][random_index]['question'] + "\"")

			print('Answer: ', self.state.q_and_a['questions'][random_index]['answer'], ' (', self.state.q_and_a['questions'][random_index]['info'], ')', sep='')
			user_input = input("Command ('?' for help):").lower()

			self.notify_input_event_subscribers(
				self.state.q_and_a_file_path,
				random_index,
				self.state.q_and_a['identifier'],
				event=user_input
			)

			if user_input == "d":
				self.state.training_process[-1] = 'd'
				self.state.deactivated_questions.append(random_index)
				print(self.log_tag, 'Question deactivated.')
				question_answered = True
			elif user_input == "all":
				self.print_all()
				question_answered = True
			elif user_input == 'exit': sys.exit(0)
			elif user_input == '?': self.print_help()
			elif user_input == '+':
				self.state.training_process[-1] = '+'
				question_answered = True
			elif user_input == '-':
				self.state.training_process[-1] = '-'
				question_answered = True
			elif user_input in ['load', 'read', 'restore']:
				self.load_state(ask_file_name=True)
				if random_index in self.state.deactivated_questions:
					random_index = self.state.get_random_index()
			elif user_input in ['save', 'write', 'persist']: self.save_state(ask_file_name=True)
			elif user_input == 'stats': Statistic.print_stats(self.state.training_process)

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
				self.notify_input_event_subscribers(
					self.state.q_and_a_file_path,
					0,
					self.state.q_and_a['identifier'],
					event='exit'
				)
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
				if event == '+':
					subscriber.update_on_correct(question_number)
				elif event == '-':
					subscriber.update_on_incorrect(question_number)
				elif event == 'd':
					subscriber.update_on_deactivate(question_number)
				elif event == '?':
					subscriber.update_on_show_help()
				elif event == 'all':
					subscriber.update_on_show_all()
				elif event == 'stats':
					subscriber.update_on_show_stats()
				elif event in ['charts', 'plot', 'diagram', 'advice']:
					subscriber.update_on_generate_charts()
				elif event in ['load', 'read', 'restore']:
					subscriber.update_on_load_training_state(file_path, question_set_identifier)
				elif event in ['save', 'write', 'persist']:
					subscriber.update_on_save_training_state(file_path, question_set_identifier)
				elif event == 'exit':
					subscriber.update_on_exit()

				# general update, something has been put in
				subscriber.update()
				
	def unsubscribe_input_event_subscriber(self, subscriber):
		try:
			self.input_event_subscribers.remove(subscriber)
		except ValueError as error:
			print(self.log_tag, 'Tried to remove subscriber, which does not exist in list of subscribers.')
	
	def extend_data_file_path(self, file_name, state=False):
		if state:
			return os.path.join('data', file_name + '_state' + '.json')
		else:
			return os.path.join('data', file_name + '.json')
				
				
				

