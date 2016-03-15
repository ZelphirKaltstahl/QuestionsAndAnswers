from unittest.mock import Mock
from unittest.mock import MagicMock

import json
import pytest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/')


import Application
from InputObservers.DefaultInputEventObserver import DefaultInputEventObserver#
from TrainingState import TrainingState


__author__ = '杨小龙'

file_path_to_test_q_and_a = 'data' + os.sep + 'test_q_and_a.json'
file_path_to_test_training_state = 'data' + os.sep + 'test_state.json'
test_training_state_name = 'test'


@pytest.fixture()
def created_test_q_and_a():
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
def created_test_q_and_a_file(created_test_q_and_a):
	try:
		with open(file_path_to_test_q_and_a, 'w') as output_file:
			json.dump(created_test_q_and_a, output_file, ensure_ascii=False, indent='\t', sort_keys=True)
			assert os.path.exists(file_path_to_test_q_and_a), 'The test Q&A has not been created.'
	except FileNotFoundError as filenotfounderror:
		pytest.fail('The test_q_and_a_file could not be created.')
	except Exception as e:
		raise e
		pytest.fail('Exception occured while trying to write to test_q_and_a_file.')

@pytest.fixture()
@pytest.mark.usefixtures('q_and_a_file')
def created_test_training_state():
	test_training_state = TrainingState()
	try:
		with open(file_path_to_test_q_and_a, 'r') as test_q_and_a_file:
			test_q_and_a_content = json.load(test_q_and_a_file)
			test_training_state.q_and_a = test_q_and_a_content
			test_training_state.deactivated_questions = [0]
			test_training_state.asked_count = 10
			test_training_state.correctly_answered_count = 9
			test_training_state.q_and_a_file_path = file_path_to_test_q_and_a
			test_training_state.training_process = ['+','+','+','+','+','-','+','+','+','+']
			return test_training_state
	except FileNotFoundError as filenotfounderror:
		raise filenotfounderror
		pytest.fail('The test_q_and_a_file was not found.')
	except Exception as e:
		raise e
		pytest.fail('The test_q_and_a_file was found, but something else went wrong.')

@pytest.fixture()
def created_test_training_state_file(created_test_training_state):
	created_test_training_state.save(file_path_to_test_training_state)

@pytest.fixture()
@pytest.mark.usefixtures('q_and_a_file')
def created_test_application(created_test_q_and_a_file):
	Application.input = lambda x: 'd'
	application = Application.Application(file_path_to_test_q_and_a)
	return application

@pytest.fixture
def mock_input_event_subscriber():
	return Mock(spec=DefaultInputEventObserver)


class TestApplication:
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
		Application.input = input
		try:
			os.remove(file_path_to_test_q_and_a)
			os.remove(file_path_to_test_training_state)
		except OSError as e:
			pass

	@pytest.mark.unit
	def test_register_input_event_subscriber(self, created_test_application):
		test_subscriber = DefaultInputEventObserver()
		count_before = len(created_test_application.input_event_subscribers)
		created_test_application.register_input_event_subscriber(test_subscriber)
		count_after = len(created_test_application.input_event_subscribers)
		# check count
		msg = 'Not exactly one subscriber has been registered.'
		assert count_after - count_before == 1, msg
		# check identity
		msg = 'The last registered subscriber is not the one the test registered.'
		assert created_test_application.input_event_subscribers[-1] is test_subscriber, msg

	@pytest.mark.unit
	def test_unsubscribe_input_event_subscriber(self, created_test_application):
		test_subscriber = DefaultInputEventObserver()
		count_before = len(created_test_application.input_event_subscribers)
		list_of_subscribers_before = [subscriber for subscriber in created_test_application.input_event_subscribers]
		created_test_application.register_input_event_subscriber(test_subscriber)
		
		# check registered
		msg = 'The test subscriber is not registered.'
		assert test_subscriber in created_test_application.input_event_subscribers, msg
		
		created_test_application.unsubscribe_input_event_subscriber(test_subscriber)
		
		# check unsubscribed
		msg = 'The test subscriber has not been unsubscribed.'
		assert test_subscriber not in created_test_application.input_event_subscribers, msg

		count_after = len(created_test_application.input_event_subscribers)

		# check count afterwards equals count before
		msg = 'count of subscribers afterwards is not equal to count before registering and unsubscribing the subscriber'
		assert count_before == count_after, msg

		list_of_subscribers_after = [subscriber for subscriber in created_test_application.input_event_subscribers]

		# check identities of subscribers before and after
		msg = 'subscriber, which was in list of subscribers before is not in the list of subscribers afterwards'
		for subscriber in list_of_subscribers_before:
			assert subscriber in list_of_subscribers_after, msg

		msg = 'subscriber, which was in list of subscribers after is not in the list of subscribers before'
		for subscriber in list_of_subscribers_after:
			assert subscriber in list_of_subscribers_before, msg

	@pytest.mark.unit
	def test_notify_input_event_subscribers_on_correct(self, created_test_application, mock_input_event_subscriber):
		created_test_application.register_input_event_subscriber(mock_input_event_subscriber)

		file_path = created_test_application.state.q_and_a_file_path
		random_index = 0
		identifier = created_test_application.state.q_and_a['identifier'],
		event = '+'
		
		assert not mock_input_event_subscriber.update_on_correct.called, 'update_on_correct should not have been called yet'

		created_test_application.notify_input_event_subscribers(file_path, random_index, identifier, event)
		
		mock_input_event_subscriber.update_on_correct.assert_called_once_with(random_index)
		mock_input_event_subscriber.update.assert_called_once_with()

	@pytest.mark.unit
	def test_notify_input_event_subscribers_on_incorrect(self, created_test_application, mock_input_event_subscriber):
		created_test_application.register_input_event_subscriber(mock_input_event_subscriber)
		
		random_index = 0
		event = '-'
		
		assert not mock_input_event_subscriber.update_on_incorrect.called, 'update_on_incorrect should not have been called yet'

		created_test_application.notify_input_event_subscribers(
			created_test_application.state.q_and_a_file_path, 
			random_index, 
			created_test_application.state.q_and_a['identifier'], 
			event
		)
		
		mock_input_event_subscriber.update_on_incorrect.assert_called_once_with(random_index)
		mock_input_event_subscriber.update.assert_called_once_with()

	@pytest.mark.unit
	def test_notify_input_event_subscribers_on_deactivate(self, created_test_application, mock_input_event_subscriber):
		created_test_application.register_input_event_subscriber(mock_input_event_subscriber)
		
		random_index = 0
		event = 'd'
		
		assert not mock_input_event_subscriber.update_on_deactivate.called, 'update_on_deactivate should not have been called yet'

		created_test_application.notify_input_event_subscribers(
			created_test_application.state.q_and_a_file_path, 
			random_index, 
			created_test_application.state.q_and_a['identifier'], 
			event
		)
		
		mock_input_event_subscriber.update_on_deactivate.assert_called_once_with(random_index)
		mock_input_event_subscriber.update.assert_called_once_with()

	@pytest.mark.unit
	def test_notify_input_event_subscribers_on_show_all(self, created_test_application, mock_input_event_subscriber):
		created_test_application.register_input_event_subscriber(mock_input_event_subscriber)
		
		random_index = 0
		event = 'all'
		
		assert not mock_input_event_subscriber.update_on_show_all.called, 'update_on_show_all should not have been called yet'

		created_test_application.notify_input_event_subscribers(
			created_test_application.state.q_and_a_file_path, 
			random_index, 
			created_test_application.state.q_and_a['identifier'], 
			event
		)
		
		mock_input_event_subscriber.update_on_show_all.assert_called_once_with()
		mock_input_event_subscriber.update.assert_called_once_with()

	@pytest.mark.unit
	def test_notify_input_event_subscribers_on_load(self, created_test_application, mock_input_event_subscriber):
		created_test_application.register_input_event_subscriber(mock_input_event_subscriber)
		
		random_index = 0
		event = 'load'
		
		assert not mock_input_event_subscriber.update_on_load_training_state.called, 'update_on_load_training_state should not have been called yet'

		created_test_application.notify_input_event_subscribers(
			created_test_application.state.q_and_a_file_path, 
			random_index, 
			created_test_application.state.q_and_a['identifier'], 
			event
		)
		
		mock_input_event_subscriber.update_on_load_training_state.assert_called_once_with(
			created_test_application.state.q_and_a_file_path, 
			created_test_application.state.q_and_a['identifier']
		)
		mock_input_event_subscriber.update.assert_called_once_with()

	@pytest.mark.unit
	def test_notify_input_event_subscribers_on_save(self, created_test_application, mock_input_event_subscriber):
		created_test_application.register_input_event_subscriber(mock_input_event_subscriber)
		
		random_index = 0
		event = 'save'
		
		assert not mock_input_event_subscriber.update_on_save_training_state.called, 'update_on_save_training_state should not have been called yet'

		created_test_application.notify_input_event_subscribers(
			created_test_application.state.q_and_a_file_path, 
			random_index, 
			created_test_application.state.q_and_a['identifier'], 
			event
		)
		
		mock_input_event_subscriber.update_on_save_training_state.assert_called_once_with(
			created_test_application.state.q_and_a_file_path, 
			created_test_application.state.q_and_a['identifier']
		)
		mock_input_event_subscriber.update.assert_called_once_with()

	@pytest.mark.unit
	def test_notify_input_event_subscribers_on_show_help(self, created_test_application, mock_input_event_subscriber):
		created_test_application.register_input_event_subscriber(mock_input_event_subscriber)
		
		random_index = 0
		event = '?'
		
		assert not mock_input_event_subscriber.update_on_show_help.called, 'update_on_show_help should not have been called yet'

		created_test_application.notify_input_event_subscribers(
			created_test_application.state.q_and_a_file_path, 
			random_index, 
			created_test_application.state.q_and_a['identifier'], 
			event
		)
		
		mock_input_event_subscriber.update_on_show_help.assert_called_once_with()
		mock_input_event_subscriber.update.assert_called_once_with()

	@pytest.mark.unit
	def test_notify_input_event_subscribers_on_show_stats(self, created_test_application, mock_input_event_subscriber):
		created_test_application.register_input_event_subscriber(mock_input_event_subscriber)
		
		random_index = 0
		event = 'stats'
		
		assert not mock_input_event_subscriber.update_on_show_stats.called, 'update_on_show_stats should not have been called yet'

		created_test_application.notify_input_event_subscribers(
			created_test_application.state.q_and_a_file_path, 
			random_index, 
			created_test_application.state.q_and_a['identifier'], 
			event
		)
		
		mock_input_event_subscriber.update_on_show_stats.assert_called_once_with()
		mock_input_event_subscriber.update.assert_called_once_with()

	@pytest.mark.unit
	def test_notify_input_event_subscribers_on_exit(self, created_test_application, mock_input_event_subscriber):
		created_test_application.register_input_event_subscriber(mock_input_event_subscriber)
		
		random_index = 0
		event = 'exit'
		
		assert not mock_input_event_subscriber.update_on_exit.called, 'update_on_exit should not have been called yet'

		created_test_application.notify_input_event_subscribers(
			created_test_application.state.q_and_a_file_path, 
			random_index, 
			created_test_application.state.q_and_a['identifier'], 
			event
		)
		
		mock_input_event_subscriber.update_on_exit.assert_called_once_with()
		mock_input_event_subscriber.update.assert_called_once_with()

	@pytest.mark.unit
	def test_load_training_state(self, created_test_application, created_test_training_state_file):
		assert os.path.isfile(file_path_to_test_training_state), 'file was not created'

		Application.input = lambda x: test_training_state_name
		created_test_application.load_state(ask_file_name=True)

		file_path = created_test_application.extend_data_file_path(test_training_state_name, state=True)
		with open(file_path, 'r') as test_file:
			read_state = json.load(test_file)
			
			with open(read_state['q_and_a_file_path'], 'r') as test_q_and_a_file:
				read_q_and_a = json.load(test_q_and_a_file)

				assert created_test_application.state.q_and_a == read_q_and_a, 'the application did not load the correct training state'
				assert created_test_application.state.deactivated_questions == read_state['deactivated_questions'], 'the application did not load the correct training state'
				assert created_test_application.state.asked_count == len(read_state['training_process']), 'the application did not load the correct training state'
				assert created_test_application.state.correctly_answered_count == read_state['training_process'].count('+'), 'the application did not load the correct training state'
				assert created_test_application.state.q_and_a_file_path == read_state['q_and_a_file_path'], 'the application did not load the correct training state'
				assert created_test_application.state.training_process == read_state['training_process'], 'the application did not load the correct training state'

		created_test_application.load_state(ask_file_name=False)

		file_path = created_test_application.extend_data_file_path('training', state=True)
		
		with open(file_path, 'r') as test_file:
			read_state = json.load(test_file)
			
			with open(read_state['q_and_a_file_path'], 'r') as test_q_and_a_file:
				read_q_and_a = json.load(test_q_and_a_file)

				assert created_test_application.state.q_and_a == read_q_and_a, 'the application did not load the correct training state'
				assert created_test_application.state.deactivated_questions == read_state['deactivated_questions'], 'the application did not load the correct training state'
				assert created_test_application.state.asked_count == len(read_state['training_process']), 'the application did not load the correct training state'
				assert created_test_application.state.correctly_answered_count == read_state['training_process'].count('+'), 'the application did not load the correct training state'
				assert created_test_application.state.q_and_a_file_path == read_state['q_and_a_file_path'], 'the application did not load the correct training state'
				assert created_test_application.state.training_process == read_state['training_process'], 'the application did not load the correct training state'

	@pytest.mark.unit
	def test_save_training_state(self, created_test_application, created_test_training_state):
		Application.input = lambda x: created_test_application.extend_data_file_path(test_training_state_name, state=True)
		created_test_application.state = created_test_training_state
		created_test_application.save_state(ask_file_name=True)

		file_path = created_test_application.extend_data_file_path(test_training_state_name, state=True)

		with open(file_path, 'r') as test_file:
			read_state = json.load(test_file)
			
			with open(read_state['q_and_a_file_path'], 'r') as test_q_and_a_file:
				read_q_and_a = json.load(test_q_and_a_file)

				assert created_test_application.state.q_and_a == read_q_and_a, 'the application did not load the correct training state'
				assert created_test_application.state.deactivated_questions == read_state['deactivated_questions'], 'the application did not load the correct training state'
				assert created_test_application.state.asked_count == len(read_state['training_process']), 'the application did not load the correct training state'
				assert created_test_application.state.correctly_answered_count == read_state['training_process'].count('+'), 'the application did not load the correct training state'
				assert created_test_application.state.q_and_a_file_path == read_state['q_and_a_file_path'], 'the application did not load the correct training state'
				assert created_test_application.state.training_process == read_state['training_process'], 'the application did not load the correct training state'

	@pytest.mark.unit
	def test_get_random_index(self, created_test_application):
		for x in range(1000):
			random_index = created_test_application.get_random_index()
			assert random_index >= 0 and random_index < len(created_test_application.state.q_and_a['questions'])

	@pytest.mark.unit
	def test_ask(self):
		pass

	@pytest.mark.unit
	def test_quiz(self):
		pass

	@pytest.mark.unit
	def test_extend_data_file_path(self, created_test_application):
		msg = 'file name nor correctly extended to path'
		assert created_test_application.extend_data_file_path('test', state=False) == 'data' + os.sep + 'test.json', msg
		assert created_test_application.extend_data_file_path('test', state=True) == 'data' + os.sep + 'test_state.json', msg
		assert created_test_application.extend_data_file_path('abc', state=False) == 'data' + os.sep + 'abc.json', msg
		assert created_test_application.extend_data_file_path('abc', state=True) == 'data' + os.sep + 'abc_state.json', msg