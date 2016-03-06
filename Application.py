import sys
import random
from collections import namedtuple
from StateReader import StateReader
from StateWriter import StateWriter
from Helper import truncate_number
from xml_parser.XMLParserException import XMLParserException
from FileReader import FileReader
from Statistic import Statistic

class Application:
	"""docstring for Application"""

	def __init__(self, questions_file_path, answers_file_path, additional_info_file_path=None):
		self.log_tag = '[STATUS: Application]'

		self.file_reader = FileReader()
		self.state_reader = StateReader()
		self.state_writer = StateWriter()
		
		self.deactivated_questions = []
		self.asked_count = 0
		self.correctly_answered_count = 0

		self.questions = self.file_reader.read_file(questions_file_path)
		if additional_info_file_path:
			self.additional_infos = self.file_reader.read_file(additional_info_file_path)
		self.answers = self.file_reader.read_file(answers_file_path)

		self.questions_file_path = questions_file_path
		self.answers_file_path = answers_file_path
		self.additional_info_file_path = additional_info_file_path

		self.training_process = []

	def run(self):
		self.quiz()

	def load_state(self, ask_file_name=False):
		try:
			if ask_file_name:
				try:
					training_state_file_name = input('Enter a file name (default: training_state):')
					if training_state_file_name == '': training_state_file_name = 'training_state'
					training_state_file_name += '.xml'
					read_state = self.state_reader.read_state(training_state_file_name)
				except (Exception) as e:
					print(self.log_tag, 'Error while reading state. Is the file name not usable?')
			else:
				read_state = self.state_reader.read_state('training_state.xml')

			try:
				# extract information from that state
				self.questions = self.file_reader.read_file(read_state.questions_file_path)
				self.additional_infos = self.file_reader.read_file(read_state.answers_file_path)
				self.answers = self.file_reader.read_file(read_state.additional_info_file_path)
				
				if read_state.deactivated_questions:
					print(self.log_tag, read_state.deactivated_questions)
					self.deactivated_questions = [int(i) for i in read_state.deactivated_questions]

				if read_state.training_process:
					self.training_process = read_state.training_process

				self.asked_count = len(self.training_process)
				self.correctly_answered_count = self.training_process.count('+') + self.training_process.count('d')
			
			except (UnboundLocalError) as e:
				print(self.log_tag, 'Could not read training state.')

		except (XMLParserException) as e:
			print(self.log_tag, 'State file could not be used.')
		

	def save_state(self, ask_file_name=False):
		State = namedtuple('TrainingState', ['questions_file_path', 'answers_file_path', 'additional_info_file_path', 'deactivated_questions', 'training_process'])
		training_state = State(
			self.questions_file_path,
			self.answers_file_path,
			self.additional_info_file_path,
			self.deactivated_questions,
			self.training_process
		)
		if ask_file_name:
			try:
				training_state_file_name = input('Enter a file name (default: training_state):')
				if training_state_file_name == '': training_state_file_name = 'training_state'
				training_state_file_name += '.xml'
				self.state_writer.save_state(training_state, training_state_file_path=training_state_file_name)
			except (Exception) as e:
				print(self.log_tag, 'Error while saving state. Is the file name not usable?')
		else:
			self.state_writer.save_state(training_state, 'training_state.xml')

	def print_help(self):
		print(
			'\nAvailable commands:',
			'!d:deactivate',
			'all:print all',
			'exit:exit',
			'?:help',
			'+:mark correctly answered',
			'-:mark wrongly answered',
			'save/write/persist:save training state',
			'load/read/restore:load training state',
			'stats:print statistics\n',
			sep='\n',
			end='\n'
		)

	def get_random_index(self):
		random_index = random.randint(0, len(self.questions)-1)
		while random_index in self.deactivated_questions:
			random_index = random.randint(0, len(self.questions)-1)
		return random_index

	# this method could be refactored to use dict of action objects, which implement an ABC with a required method execute, which executes the actions on specific inputs
	def ask(self):
		random_index = self.get_random_index()
		self.training_process.append('?')

		while(True):
			input("Translate: \"" + self.questions[random_index] + "\"")
			print('Answer: ', self.answers[random_index], ' (', self.additional_infos[random_index], ')', sep='')
			user_input = input("Command ('?' for help):").lower()

			if user_input == "!d":
				self.training_process[-1] = 'd'
				self.deactivated_questions.append(random_index)
				print(self.log_tag, 'Question deactivated.')
				return
			elif user_input == "all":
				self.print_all(sel.questions, self.answers)
				return
			elif user_input == 'exit': sys.exit(0)
			elif user_input == '?': self.print_help()
			elif user_input == '+':
				self.training_process[-1] = '+'
				return
			elif user_input == '-':
				self.training_process[-1] = '-'
				return
			elif user_input in ['load', 'read', 'restore']:
				self.load_state(ask_file_name=True)
				if random_index in self.deactivated_questions:
					random_index = self.get_random_index()
			elif user_input in ['save', 'write', 'persist']: self.save_state(ask_file_name=True)
			elif user_input == 'stats': Statistic.print_stats(self.training_process)
			else: continue

	def quiz(self):
		print('\n' + self.log_tag, 'Starting quiz ...', end='\n\n')
		while(True):
			try:
				if len(self.deactivated_questions) < len(self.questions):
					self.ask() # here the input logic is happening
					Statistic.print_result(self.training_process)
				else:
					print(self.log_tag, 'All questions deactivated. Exiting now...')
					sys.exit(0)
			
			except (KeyboardInterrupt, EOFError) as interrupt:
				print()
				self.save_state()
				print(self.log_tag, 'Exiting application ...')
				sys.exit(0)