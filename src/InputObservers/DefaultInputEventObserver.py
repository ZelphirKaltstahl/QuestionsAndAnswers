from InputObservers.InputObserver import InputObserver
from decorators.overrides import overrides

class DefaultInputEventObserver(InputObserver):
	"""This is the default observer for input events."""
	
	def __init__(self):
		super(DefaultInputEventObserver, self).__init__()
		self.log_tag = '[DefaultInputEventObserver]'
	
	@overrides(InputObserver)
	def update_on_show_all(self):
		print(self.log_tag, 'all was entered!')

	@overrides(InputObserver)
	def update_on_deactivate(self, question_number):
		pass

	@overrides(InputObserver)
	def update_on_correct(self, question_number):
		pass

	@overrides(InputObserver)
	def update_on_incorrect(self, question_number):
		pass

	@overrides(InputObserver)
	def update_on_load_training_state(self, file_path, question_set_identifier):
		pass

	@overrides(InputObserver)
	def update_on_save_training_state(self, file_path, question_set_identifier):
		pass

	@overrides(InputObserver)
	def update_on_show_help(self):
		pass

	@overrides(InputObserver)
	def update_on_show_stats(self):
		pass

	@overrides(InputObserver)
	def update_on_exit(self):
		pass

	@overrides(InputObserver)
	def update(self):
		"""general update method for any kind of event"""
		pass