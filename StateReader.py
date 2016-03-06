from collections import namedtuple
from xml_parser.XMLParserException import XMLParserException
from xml_parser.XMLParser import XMLParser
from State import State

class StateReader:
	"""This class represents a reader for state files."""
	def __init__(self):
		self.xsd_file_path = 'training_state.xsd'

		self.log_tag = '[STATUS: StatusReader]'
		self.xml_parser = XMLParser()
	
	def read_state(self, training_state_file_path='training_state_test.xml'):
		print(self.log_tag ,'Reading state file ...')
		
		try:
			root_node = self.xml_parser.get_xml_element_tree_root(
				self.xsd_file_path, 
				training_state_file_path
			)
			print(self.log_tag ,'State file read successfully.')
		
		except (XMLParserException) as ex:
			print(self.log_tag ,'Reading state file FAILED.')
			print(self.log_tag ,'State file is invalid.')
			raise ex

		State = namedtuple(
			'TrainingState',
			[
				'questions_file_path',
				'answers_file_path',
				'additional_info_file_path',
				'deactivated_questions',
				'training_process'
			]
		)

		questions_file_path = root_node.find('questions_file_path').text if root_node.find('questions_file_path').text else ''
		answers_file_path = root_node.find('answers_file_path').text if root_node.find('answers_file_path').text else ''
		additional_info_file_path = root_node.find('additional_info_file_path').text if root_node.find('additional_info_file_path').text else ''
		
		deactivated_questions = root_node.find('deactivated_questions').text.split(',', -1) if root_node.find('deactivated_questions').text else []
		training_process = root_node.find('training_process').text.split(',', -1) if root_node.find('training_process').text else []

		read_state = State(
			questions_file_path,
			answers_file_path,
			additional_info_file_path,
			deactivated_questions,
			training_process
		)

		return read_state