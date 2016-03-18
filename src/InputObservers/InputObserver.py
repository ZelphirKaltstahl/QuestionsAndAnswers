from abc import ABCMeta, abstractmethod

class InputObserver:
	__metaclass__ = ABCMeta

	@abstractmethod
	def update_on_show_all(self):
		pass

	@abstractmethod
	def update_on_deactivate(self, question_number):
		pass

	@abstractmethod
	def update_on_correct(self, question_number):
		pass

	@abstractmethod
	def update_on_incorrect(self, question_number):
		pass

	@abstractmethod
	def update_on_load_training_state(self, file_path, question_set_identifier):
		pass

	@abstractmethod
	def update_on_save_training_state(self, file_path, question_set_identifier):
		pass

	@abstractmethod
	def update_on_show_help(self):
		pass

	@abstractmethod
	def update_on_show_stats(self):
		pass

	@abstractmethod
	def update_on_generate_charts(self):
		pass

	@abstractmethod
	def update_on_exit(self):
		pass

	@abstractmethod
	def update(self):
		"""general update method for any kind of event"""
		pass