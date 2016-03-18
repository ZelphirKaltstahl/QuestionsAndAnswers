from unittest.mock import Mock
from unittest.mock import MagicMock

import json
import pytest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/')

from FileReader import FileReader

__author__ = '杨小龙'


file_path_to_test_q_and_a = 'data' + os.sep + 'test_q_and_a.json'
file_path_to_test_training_state = 'data' + os.sep + 'test_state.json'
test_training_state_name = 'test'


class TestFileReader:
	"""test class for the Application class"""
	def setup(self):
		pass

	def teardown(self):
		pass

	@classmethod
	def setup_class(cls):
		pass
	
	@classmethod
	def teardown_class(cls):
		pass

	def setup_method(self, method):
		self.file_reader = FileReader()
		self.file_path = os.path.join('data', 'testfile.txt')

	def teardown_method(self, method):
		try:
			os.remove(self.file_path)
		except OSError as e:
			pass

	@pytest.mark.unit
	def test_read_file(self):
		lines = [
			'first line',
			'second line',
			'third line',
			'fourth line',
			'fifth line',
			'sixth line'
		]
		with open(self.file_path, 'w') as output_file:
			for line in lines:
				output_file.write(line + '\n')

		read_lines = self.file_reader.read_file(self.file_path)

		for lineno, line in enumerate(lines):
			assert line == read_lines[lineno], 'Not all read lines match.'

		for lineno, line in enumerate(read_lines):
			assert line == lines[lineno], 'Not all read lines match.'

	@pytest.mark.unit
	def test_read_json(self):
		json_content = {}
		json_content['identifier'] = 'HSK1'
		json_content['questions'] = []
		json_content['questions'].append({
			"answer": "我",
			"info": "wǒ",
			"question": "ich"
		})
		json_content['questions'].append({
			"answer": "的",
			"info": "de",
			"question": "von, (besitzanzeigendes Partikel)"
		})
		json_content['questions'].append({
			"answer": "你",
			"info": "nǐ",
			"question": "du"
		})

		with open(self.file_path, 'w') as output_file:
			json.dump(json_content, output_file, ensure_ascii=False, indent='\t', sort_keys=True)

		read_json_content = self.file_reader.read_json(self.file_path)
		assert json_content == read_json_content, 'JSON content was not loaded correctly.'