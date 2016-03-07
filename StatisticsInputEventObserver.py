import json
from datetime import datetime
from Observer import Observer
from decorators.overrides import overrides

class StatisticsInputEventObserver(Observer):
	"""This is the default observer for input events."""
	
	def __init__(self):
		super(DefaultInputEventObserver, self).__init__()
	
	@overrides(Observer)
	def update_on_show_all(self):
		pass

	@overrides(Observer)
	def update_on_deactivate(self, question_number):
		pass

	@overrides(Observer)
	def update_on_correct(self, question_number):
		pass

	@overrides(Observer)
	def update_on_incorrect(self, question_number):
		pass

	@overrides(Observer)
	def update_on_load_training_state(self, file_path, question_set_identifier):
		pass

	@overrides(Observer)
	def update_on_save_training_state(self, file_path, question_set_identifier):
		pass

	@overrides(Observer)
	def update_on_show_help(self):
		pass

	@overrides(Observer)
	def update_on_show_stats(self):
		pass

	@overrides(Observer)
	def update_on_exit(self):
		pass

	@overrides(Observer)
	def update(self):
		"""general update method for any kind of event"""
		pass