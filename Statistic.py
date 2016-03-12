from Helper import truncate_number
from math import floor

class Statistic:
	"""This class computes statistics."""
	def __init__(self):
		super(Statistic, self).__init__()
	
	@staticmethod
	def correctly_answered_count(training_process):
		correctly_answered_count = training_process.count('d')
		correctly_answered_count += training_process.count('+')
		return correctly_answered_count

	@staticmethod
	def calculate_longest_streak(training_process, streak_characters):
		longest_streak = 0
		current_streak = 0
		for (index, character) in enumerate(training_process):
			if character in streak_characters:
				current_streak += 1
			else:
				if current_streak > longest_streak or index == len(training_process):
					longest_streak = current_streak
				current_streak = 0
		return longest_streak

	@staticmethod
	def print_stats(training_process):
		if len(training_process) - 1 != 0:  # -1 is for the still unanswered question
			percentage_wrong_answers = 100.0 / (len(training_process) - 1) * training_process.count('-')
			percentage_wrong_answers = truncate_number(percentage_wrong_answers, 3)
		else:
			percentage_wrong_answers = 0.0

		if len(training_process) - 1 != 0:  # -1 is for the still unanswered question
			percentage_correct_answers = 100.0 / (len(training_process) - 1) * (training_process.count('d') + training_process.count('+'))
			percentage_correct_answers = truncate_number(percentage_correct_answers, 3)
		else:
			percentage_correct_answers = 0.0

		title = 'YOUR PERFORMANCE' 
		lines = [
			'Questions asked: ' + str(len(training_process)) + ' (1 unanswered)',
			'Questions correctly answered: ' + str(training_process.count('d') + training_process.count('+')),
			'% (correct answers): ' + str(percentage_correct_answers) + '%',
			'% (correct answers): ' + str(percentage_wrong_answers) + '%',
			'Longest streak (correct answers): ' + str(Statistic.calculate_longest_streak(training_process, ['+','d'])),
			'Longest streak (wrong answers): ' + str(Statistic.calculate_longest_streak(training_process, ['-'])),
			'Deactivated questions: ' + str(training_process.count('d'))
		]
		boxed_lines = Statistic.box_lines(lines, title)
		for line in boxed_lines: print(line)

	@staticmethod
	def box_lines(lines, title):
		"""This method draws a box around lines of text, using the unicode boy characters.
		It is taking the length of all lines into account."""
		title = ' ' + title + ' '
		longest_line = 0
		for line in lines:
			if len(line) > longest_line:
				longest_line = len(line)
		if len(title) > longest_line:
			longest_line = len(title)

		boxed_lines = []

		# create beginning border
		beginning_line = '\n╔' + ('═' * (longest_line)) + '╗'

		# insert title
		offset = floor((longest_line - (len(title))) / 2)
		beginning_line = beginning_line[:offset + 1] + ' ' + title + ' ' + beginning_line[offset + 1 + len(title):]
		boxed_lines.append(beginning_line)

		# create in between lines
		for line in lines:
			placeholder_spaces = ' ' * (longest_line - len(line))
			boxed_lines.append('║ ' + line + placeholder_spaces + ' ║')

		# create ending border
		ending_line = '╚' + ('═' * (longest_line + 2)) + '╝\n'
		boxed_lines.append(ending_line)

		return boxed_lines		

	@staticmethod
	def print_result(training_process):
		if len(training_process) != 0:
			percentage_correct_answers = 100 / len(training_process) * (training_process.count('d') + training_process.count('+'))
			percentage_correct_answers = truncate_number(percentage_correct_answers, 3)
		else:
			percentage_correct_answers = 0.0
		
		print("\nasked: ", len(training_process), "\nanswered: ", percentage_correct_answers, "% correctly\n", sep='', end='\n')