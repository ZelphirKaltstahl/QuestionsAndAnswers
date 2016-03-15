from unittest.mock import Mock
from unittest.mock import MagicMock

import json
import pytest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/')


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
		pass

	def teardown_method(self, method):
		# Application.input = input
		# try:
		# 	os.remove(file_path_to_test_q_and_a)
		# 	os.remove(file_path_to_test_training_state)
		# except OSError as e:
		# 	pass
		pass

	@pytest.mark.unit
	def test_read_file(self):
		pass

	@pytest.mark.unit
	def test_read_json(self):
		pass