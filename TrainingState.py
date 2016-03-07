import json

class TrainingState:
	"""docstring for TrainingState"""
	def __init__(self):
		super(TrainingState, self).__init__()
		self.log_tag = '[STATUS: TrainingState]'

		self.q_and_a = {}
		self.deactivated_questions = []
		self.asked_count = 0
		self.correctly_answered_count = 0
		self.q_and_a_file_path = ''
		self.training_process = []

	def save(self, file_path):
		try:
			with open(file_path, 'w') as output_file:
				output_content = {
					'q_and_a_file_path': self.q_and_a_file_path,
					'deactivated_questions': self.deactivated_questions,  #','.join([str(item) for item in self.deactivated_questions]),
					'training_process': self.training_process
				}
				json.dump(output_content, output_file, ensure_ascii=False, indent='\t', sort_keys=True)
				print(self.log_tag, 'Successfully saved state.')
		except Exception as e:
			print(self.log_tag, 'Error while saving state. Is the file not writable?')
			raise e

	def load(self, file_path):
		# try to read state
		try:
			with open(file_path, 'r') as input_file:
				read_state = json.load(input_file)

				# try to read q&a which is mentioned in the state file
				q_and_a_file_path = read_state['q_and_a_file_path']
				try:
					with open(q_and_a_file_path, 'r') as q_and_a_file:
						# set application state from read save state
						self.q_and_a = json.load(q_and_a_file)
						self.q_and_a_file_path = q_and_a_file_path
						self.training_process = read_state['training_process']
						self.deactivated_questions = read_state['deactivated_questions']
						self.asked_count = len(self.training_process)
						self.correctly_answered_count = self.training_process.count('+') + self.training_process.count('d')
						print(self.log_tag, 'Successfully loaded state.')

				except Exception as e:
					print(self.log_tag, 'Error while reading Q&A file ' + q_and_a_file_path + '. Is the file not readable?')
					raise e

		except Exception as e:
			print(self.log_tag, 'Error while reading state. Is the file not readable?')
			raise e