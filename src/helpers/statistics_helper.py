from datetime import datetime

from helpers.datetime_helper import get_datetimes_in_between


def get_question_count(stats, date=None, q_and_a_identifier=None):
	count = 0

	# date and identifier specified
	if date and q_and_a_identifier:
		# print(self.log_tag, 'Both, date and identifier specified for counting.')
		if date in stats:
			if q_and_a_identifier in stats[date]:
				# print(self.log_tag, 'Adding', self.stats[date][q_and_a_identifier]['count'])
				count += stats[date][q_and_a_identifier]['count']
		# else: print(self.log_tag, 'date is not in stats')
	
	# only date specified
	elif date and not q_and_a_identifier:
		if date in stats:
			for q_set_key in stats[date]:
				count += stats[date][q_set_key]['count']

	# only identifier specified
	elif not date and q_and_a_identifier:
		stats_for_q_and_a_identifier = get_stats_for_q_and_a_identifier(q_and_a_identifier)
		count += stats_for_q_and_a_identifier['correct_count']
		count += stats_for_q_and_a_identifier['deactivated_count']
		count += stats_for_q_and_a_identifier['incorrect_count']

	# nothing specified
	else:
		for date_key, date_value in stats:
			for q_set_key, q_set_value in date_value:
				count += stats[date_key][q_set_key]['count']

	return count

def get_stats_for_q_and_a_identifier(stats, q_and_a_identifier):
	results = {
		'correct_count':0,
		'deactivated_count':0,
		'incorrect_count':0
	}
	for date_key, date_value in stats:
		if q_and_a_identifier in stats[date_key]:
			results['correct_count'] += [stats[date_key][q_and_a_identifier]['correct'][q] for q in stats[date_key][q_and_a_identifier]['correct']]
			results['deactivated_count'] += [stats[date_key][q_and_a_identifier]['deactivated'][q] for q in stats[date_key][q_and_a_identifier]['deactivated']]
			results['incorrect_count'] += [stats[date_key][q_and_a_identifier]['incorrect'][q] for q in stats[date_key][q_and_a_identifier]['incorrect']]
	return results

def get_sorted_dates(stats):
	dates = [date_key for date_key in stats.keys()]
	dates.sort()
	dates = get_datetimes_in_between(dates[0], dates[-1])
	return dates

def get_sorted_date_strings(stats):
	dates = [date_key for date_key in stats.keys()]
	dates.sort()
	dates = get_datetimes_in_between(dates[0], dates[-1])
	return [datetime.strftime(date, '%Y-%m-%d') for date in dates]