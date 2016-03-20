import numpy as np

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter
from matplotlib.backends.backend_pdf import PdfPages

from helpers.directory_helper import file_path_in_data_dir
from helpers.statistics_helper import get_question_count, get_sorted_date_strings

from datetime import datetime

class QuestionsPerDay:
	"""docstring for QuestionsPerDay"""
	def __init__(self):
		super(QuestionsPerDay, self).__init__()

		# datetime plot stuff
		self.days_formatter = DateFormatter('%Y-%m-%d')
		self.months_formatter = DateFormatter('%Y-%m')
		self.years_formatter = DateFormatter('%Y')

		self.day_locator = DayLocator()
		self.month_locator = MonthLocator()
		self.year_locator = YearLocator()

		self.date_format = '%Y-%m-%d'

	def plot(self, stats):
		dates = get_sorted_date_strings(stats)
		questions_counts = [get_question_count(stats, date=date) for date in dates]

		# draw figure
		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))

		ax.xaxis_date()  # tell the axes, that it'll display dates
		ax.xaxis.set_major_formatter(self.days_formatter)  # format the timestamps
		fig.autofmt_xdate(bottom=0.2, rotation=75, ha='right')  # format the whole figure automatically

		ax.set_ylim([0, max(questions_counts)*1.2])
		
		ax.grid(True)
		
		ax.plot(dates, questions_counts, '-', marker='o', linewidth=2.5, solid_capstyle='round', color='#FF6060', label='Number of Questions')
		ax.axhline(y=np.mean(questions_counts), label='Average', linestyle='--')  # plot the average line
		ax.fill_between(dates, 0, questions_counts, facecolor='#FF0000', alpha=0.1)  # color area beneath the line

		today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		ax.set_title('Questions per Day (on ' + today + ')')
		ax.set_xlabel('Dates')
		ax.set_ylabel('Questions')

		# Make a legend
		legend = ax.legend(loc='upper right')

		fig.tight_layout()  # automatically crop figure

		# save the plot as pdf
		with PdfPages(file_path_in_data_dir('questions_per_day.pdf')) as pdf:
			plt.savefig(pdf, format='pdf')
			plt.close()
			
			doc_meta = pdf.infodict()
			doc_meta['Title'] = 'Questions per Day'
			doc_meta['Author'] = 'QuestionsAndAnswers tool, written by Zelphir Kaltstahl'
			doc_meta['Subject'] = 'Questions asked per Day'
			doc_meta['Keywords'] = 'Questions Daily Day Answers'
			doc_meta['CreationDate'] = datetime.now()
			doc_meta['ModDate'] = datetime.now()

	def format_axes(self, ax):

		return ax