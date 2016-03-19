from InputObservers.InputObserver import InputObserver

from decorators.overrides import overrides

from FileReader import FileReader

from helpers.directory_helper import file_path_in_data_dir
from helpers.datetime_helper import get_datetimes_in_between
from helpers.color_helper import get_colors

from plotters.QuestionsPerDay import QuestionsPerDay
from plotters.QuestionsPerDayGrouped import QuestionsPerDayGrouped

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import YearLocator, MonthLocator, DayLocator, DateFormatter
from matplotlib.backends.backend_pdf import PdfPages

import time

from datetime import datetime

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

		self.date_format = '%Y-%m-%d'

		self.questions_per_day_grouped_plotter = QuestionsPerDayGrouped()
		self.questions_per_day_plotter = QuestionsPerDay()

	@overrides(InputObserver)
	def update_on_generate_charts(self):
		stats = self.file_reader.read_json(file_path_in_data_dir('stats.json'))
		self.questions_per_day_grouped_plotter.plot(stats)
		self.questions_per_day_plotter.plot(stats)