from InputObservers.InputObserver import InputObserver
from decorators.overrides import overrides
from FileReader import FileReader
from helpers.directory_helper import file_path_in_data_dir
from helpers.datetime_helper import get_datetimes_in_between
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

import time

class ChartGenerator(InputObserver):
	"""This class generates charts from logged statistics of questions and answers training.
	It also calculates some learning advice based on ones training statistics."""
	
	def __init__(self):
		super(ChartGenerator, self).__init__()
		self.log_tag = '[ChartGenerator]'
		self.file_reader = FileReader()
		self.stats = None

		# datetime plot stuff
		self.days_formatter = DateFormatter('%Y-%m-%d')
		self.months_formatter = DateFormatter('%Y-%m')
		self.years_formatter = DateFormatter('%Y')

		self.day_locator = DayLocator()
		self.month_locator = MonthLocator()
		self.year_locator = YearLocator()

		font = {
			'family': 'Bitstream Vera Sans',
			'weight': 'normal',
			'size': 11
		}

		mpl.rc('font', **font)

	@overrides(InputObserver)
	def update_on_generate_charts(self):
		self.stats = self.file_reader.read_json(file_path_in_data_dir('stats.json'))
		self.generate_questions_per_day_chart()

	def generate_questions_per_day_chart(self):
		print(self.log_tag, 'Generating chart ...')

		dates_count = len(self.stats)
		print(self.log_tag, 'Plotting for', dates_count, 'days ...')
		
		dates_to_counts = {}

		# iterate through all days having logged statistics
		for date_key, date_value in self.stats.items():
			# print(self.log_tag, 'adding key:', pd.to_datetime(date_key, format='%Y-%m-%d'))
			# print(self.log_tag, 'adding value:', self.get_question_count(date=date_key))

			dates_to_counts[pd.to_datetime(date_key, format='%Y-%m-%d')] = self.get_question_count(date=date_key)
			#dates_to_counts[time.strptime(date_key, '%Y-%m-%d')] = self.get_question_count(date=date_key)

		assert len(dates_to_counts.keys()) == len(dates_to_counts.values()), 'not same dimension'

		dates = sorted(dates_to_counts.keys())
		dates = get_datetimes_in_between(dates[0], dates[-1])
		dates.sort()
		
		questions_counts = []

		for date in dates:
			count = 0
			if date in dates_to_counts:
				count = dates_to_counts[date]
			questions_counts.append(count)

		self.plot_questions_per_day(dates, questions_counts)

	def plot_questions_per_day(self, dates, questions_counts):
		fig, ax = plt.subplots(nrows=1, ncols=1)

		ax.xaxis_date()  # tell the axes, that it'll display dates
		ax.xaxis.set_major_formatter(self.days_formatter)  # format the timestamps
		fig.autofmt_xdate(bottom=0.2, rotation=75, ha='right')  # format the whole figure so that 
		
		ax.grid(True)
		
		ax.plot(dates, questions_counts, '-', marker='o', linewidth=2.5, solid_capstyle='round', color='#FF6060', label='Number of Questions')
		ax.axhline(y=np.mean(questions_counts), label='Average', linestyle='--')  # plot the average line
		ax.fill_between(dates, 0, questions_counts, facecolor='#FF0000', alpha=0.1)  # color area beneath the line

		ax.set_title('Questions per Day')
		ax.set_xlabel('Dates')
		ax.set_ylabel('Questions')

		# ax.set_xticks(rotation=75)

		# Make a legend
		legend = ax.legend(loc='upper right')

		plt.show()

	def get_question_count(self, date=None, q_and_a_identifier=None):
		count = 0

		# date and identifier specified
		if date and q_and_a_identifier:
			if date in self.stats:
				if q_and_a_identifier in self.stats[date]:
					count += self.stats[date][q_and_a_identifier]['count']
		
		# only date specified
		elif date and not q_and_a_identifier:
			if date in self.stats:
				for q_set_key in self.stats[date]:
					count += self.stats[date][q_set_key]['count']

		# only identifier specified
		elif not date and q_and_a_identifier:
			stats_for_q_and_a_identifier = self.get_stats_for_q_and_a_identifier(q_and_a_identifier)
			count += stats_for_q_and_a_identifier['correct_count']
			count += stats_for_q_and_a_identifier['deactivated_count']
			count += stats_for_q_and_a_identifier['incorrect_count']

		# nothing specified
		else:
			for date_key, date_value in self.stats:
				for q_set_key, q_set_value in date_value:
					count += self.stats[date_key][q_set_key]['count']

		return count

	def get_stats_for_q_and_a_identifier(self, q_and_a_identifier):
		results = {
			'correct_count':0,
			'deactivated_count':0,
			'incorrect_count':0
		}
		for date_key, date_value in self.stats:
			if q_and_a_identifier in self.stats[date_key]:
				results['correct_count'] += [self.stats[date_key][q_and_a_identifier]['correct'][q] for q in self.stats[date_key][q_and_a_identifier]['correct']]
				results['deactivated_count'] += [self.stats[date_key][q_and_a_identifier]['deactivated'][q] for q in self.stats[date_key][q_and_a_identifier]['deactivated']]
				results['incorrect_count'] += [self.stats[date_key][q_and_a_identifier]['incorrect'][q] for q in self.stats[date_key][q_and_a_identifier]['incorrect']]
		return results