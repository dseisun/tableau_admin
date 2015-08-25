import datetime
def previous_sat():
	days_since_sat = (datetime.date.isoweekday(datetime.date.today()) + 1) % 7
	most_recent_sat = datetime.date.today() - datetime.timedelta(days=days_since_sat)
	return most_recent_sat.strftime("%Y-%m-%d")

def previous_day():	
	previous_day = datetime.date.today() - datetime.timedelta(days=1)
	return previous_day.strftime("%Y-%m-%d")

def current_day():
	return datetime.date.today().strftime("%Y-%m-%d")

def current_year():
	return datetime.date.today().strftime("%Y")

def previous_year():
	return str(int(datetime.date.today().strftime("%Y")) - 1)

def parameter_parsing(line):
	line = map(lambda cell: cell.replace('{PREVIOUS_SAT}', previous_sat()), line)
	line = map(lambda cell: cell.replace('{PREVIOUS_DAY}', previous_day()), line)
	line = map(lambda cell: cell.replace('{CURRENT_DAY}', current_day()), line)
	line = map(lambda cell: cell.replace('{CURRENT_YEAR}', current_year()), line)
	line = map(lambda cell: cell.replace('{PREVIOUS_YEAR}', previous_year()), line)
	return line


def parseList(raw_csv_list):
	return map(parameter_parsing, raw_csv_list)
	
