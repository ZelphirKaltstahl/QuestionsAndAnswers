from unittest.mock import Mock
from unittest.mock import MagicMock

import sys, os
import json
import pytest


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/')


file_path_to_test_q_and_a = 'data' + os.sep + 'test_q_and_a.json'
file_path_to_test_training_state = 'data' + os.sep + 'test_state.json'
test_training_state_name = 'test'

@pytest.fixture()
def q_and_a():
	test_q_and_a = {}
	test_q_and_a['identifier'] = 'HSK1'
	test_q_and_a['questions'] = []
	test_q_and_a['questions'].append({
		"answer": "我",
		"info": "wǒ",
		"question": "ich"
	})
	test_q_and_a['questions'].append({
		"answer": "的",
		"info": "de",
		"question": "von, (besitzanzeigendes Partikel)"
	})
	test_q_and_a['questions'].append({
		"answer": "你",
		"info": "nǐ",
		"question": "du"
	})
	return test_q_and_a

@pytest.fixture()
def q_and_a_file():
	try:
		with open(file_path_to_test_q_and_a, 'w') as output_file:
			json.dump(created_test_q_and_a, output_file, ensure_ascii=False, indent='\t', sort_keys=True)
			assert os.path.exists(file_path_to_test_q_and_a), 'The test Q&A has not been created.'
	except FileNotFoundError as filenotfounderror:
		pytest.fail('The test_q_and_a_file could not be created.')
	except Exception as e:
		raise e
		pytest.fail('Exception occured while trying to write to test_q_and_a_file.')