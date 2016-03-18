import pandas as pd

def get_datetimes_in_between(datetime1, datetime2):
	datetime_list = pd.date_range(datetime1, datetime2).tolist()
	return datetime_list