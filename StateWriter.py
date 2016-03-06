from collections import namedtuple
from xml_parser.XMLParser import XMLParser
from lxml import etree

class StateWriter:
	"""This class represents a state file writer, which can save the current state of vocable training to a file."""
	def __init__(self):
		self.xsd_file_path = 'training_state.xsd'
		self.log_tag = 'STATUS: StatusWriter'
		self.xml_parser = XMLParser()
		
	def save_state(self, training_state, training_state_file_path='training_state.xml'):
		print('[', self.log_tag ,'] Saving state file ...', sep='')

		xml_root_node = self.create_xml_for_state(training_state)
		if self.xml_parser.validate_tree(self.xsd_file_path, xml_root_node):
			self.xml_parser.write_xml_file(
				training_state_file_path, 
				xml_root_node,
			)
			print('[', self.log_tag ,'] State file saved successfully.', sep='')
		else:
			print('[', self.log_tag ,'] State invalid!', sep='')
			print('[', self.log_tag ,'] Could not save state file successfully!', sep='')

	def create_xml_for_state(self, training_state):
		root_node = etree.Element("save_state")
		etree.SubElement(root_node, 'questions_file_path').text = training_state.questions_file_path
		etree.SubElement(root_node, 'answers_file_path').text = training_state.answers_file_path
		etree.SubElement(root_node, 'additional_info_file_path').text = training_state.additional_info_file_path

		# deactivated_questions_text = ','.join([str(elem) for elem in training_state.deactivated_questions])
		# if not deactivated_questions_text: deactivated_questions_text = ''

		# training_process_text = ','.join(training_state.training_process)
		# if not training_process_text: training_process_text = ''

		etree.SubElement(root_node, 'deactivated_questions').text = ','.join([str(elem) for elem in training_state.deactivated_questions])
		etree.SubElement(root_node, 'training_process').text = ','.join([str(elem) for elem in training_state.training_process])

		return root_node