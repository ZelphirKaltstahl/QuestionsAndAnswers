import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter
from matplotlib.backends.backend_pdf import PdfPages

from helpers.directory_helper import file_path_in_data_dir
from helpers.statistics_helper import get_sorted_dates, get_sorted_date_strings, get_question_count
from helpers.color_helper import get_colors

from datetime import datetime

class QuestionsPerDayGrouped:
	"""docstring for QuestionsPerDayGrouped"""
	def __init__(self):
		super(QuestionsPerDayGrouped, self).__init__()

		# datetime plot stuff
		self.days_formatter = DateFormatter('%Y-%m-%d')
		self.months_formatter = DateFormatter('%Y-%m')
		self.years_formatter = DateFormatter('%Y')

		self.day_locator = DayLocator()
		self.month_locator = MonthLocator()
		self.year_locator = YearLocator()

		self.date_format = '%Y-%m-%d'

	def plot(self, stats):
		q_and_a_set_identifiers = set()
		for identifier_list in stats.values():
			for identifier in identifier_list:
				q_and_a_set_identifiers.add(identifier)
		q_and_a_set_identifiers = sorted(q_and_a_set_identifiers)

		dates = get_sorted_dates(stats)
		date_strings = get_sorted_date_strings(stats)
		colors = get_colors(len(q_and_a_set_identifiers))

		raw_data = {}
		
		for identifier in q_and_a_set_identifiers:
			raw_data[identifier] = []

		for date in date_strings:
			for identifier in q_and_a_set_identifiers:
				raw_data[identifier].append(get_question_count(stats, date=date, q_and_a_identifier=identifier))

		dataframe = pd.DataFrame(raw_data, columns=q_and_a_set_identifiers)

		# start drawing
		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
		
		ax.xaxis_date()  # tell the axes, that it'll display dates
		ax.xaxis.set_major_formatter(self.days_formatter)  # format the timestamps
		ax.grid(True)

		# Set the bar width
		bar_width = 0.9

		# positions of the left bar-boundaries
		bars_left_border_pos = [(index + 1) for index in range(len(date_strings))]

		# positions of the x-axis ticks (center of the bars as bar labels)
		tick_pos = [index + (bar_width / 2) for index in bars_left_border_pos] 

		# Create a bar plot, in position bar_1
		margin_bottom = np.zeros(len(date_strings))
		for index, identifier in enumerate(q_and_a_set_identifiers):
			values = list(dataframe[identifier].values)
			# print(self.log_tag, 'Values for', identifier, values)
			ax.bar(
				dates, values, 
				align='center', width=bar_width, label=identifier, alpha=0.5, color=colors[index], bottom=margin_bottom, linewidth=1
			)
			margin_bottom += values
			# print(self.log_tag, 'margin_bottom:', margin_bottom)

		ax.axhline(y=np.mean(margin_bottom), label='Average', linestyle='--')  # plot the average line
		ax.set_ylim(bottom=0)

		fig.autofmt_xdate(bottom=0.2, rotation=75, ha='right')  # format the whole figure automatically

		today = datetime.now().strftime('%Y-%m-%d')
		ax.set_title('Questions per Day (on ' + today + ')')
		ax.set_xlabel('Dates')
		ax.set_ylabel('Questions')

		# Make a legend
		legend = ax.legend(loc='upper right')

		fig.tight_layout()  # automatically crop figure

		# save the plot as pdf
		with PdfPages(file_path_in_data_dir('questions_per_day_grouped.pdf')) as pdf:
			plt.savefig(pdf, format='pdf')
			plt.close()
			
			doc_meta = pdf.infodict()
			doc_meta['Title'] = 'Questions per Day (grouped)'
			doc_meta['Author'] = 'QuestionsAndAnswers tool, written by Zelphir Kaltstahl'
			doc_meta['Subject'] = 'Questions asked per Day'
			doc_meta['Keywords'] = 'Questions Daily Day Answers'
			doc_meta['CreationDate'] = datetime.now()
			doc_meta['ModDate'] = datetime.now()