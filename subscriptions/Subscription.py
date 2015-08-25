import csv
import urllib2
import ListParamSub
import sys
class Subscription:
	def __init__(self, csv_path,top):
		self.raw_csv_list = list(csv.reader(open(csv_path, 'r')))
		self.csv_list = ListParamSub.parseList(self.raw_csv_list)
		self.csv_headers = self.csv_list[0]
		self.csv_body = self.csv_list[1:top+1]
		self.sub_rows = [SubscriptionRow(self.csv_headers, l) for l in self.csv_body]
		self.validity_check()

	def validity_check(self):
		#All lines have same num params
		num_cols = map(lambda x: len(x), self.csv_list)
		if max(num_cols) <> min(num_cols):
			raise Exception("Malformed CSV: Each row doesn't have the same number of columns")

	def num_param(self):
		 len(filter(lambda header: header.startswith('Param'), self.csv_headers))

	def unique_emails(self):
	 	return {row.csv_dict['Email'] for row in self.sub_rows}

	def unique_reports(self):
	 	return {row.url() for row in self.sub_rows}



class SubscriptionRow:
	def __init__(self, csv_headers, csv_row):
		self.csv_dict = self.csv_to_dict(csv_headers, csv_row)
		self.parameters = sorted(filter(lambda header: header.startswith('Param'), csv_headers))
		self.param_nums = map(lambda param: int(param[5:]), self.parameters)
		self.values = sorted(filter(lambda header: header.startswith('Value'), csv_headers))
		self.value_nums = map(lambda value: int(value[5:]), self.values)
		self.saved_path = '' #Assigned at runtime when the file export gets stored. Absolute path
		self.validity_check()

	def validity_check(self):
		if len(self.param_nums) <> len(set(self.param_nums)):
			raise Exception("Duplicate parameter key found")
		if self.value_nums <> self.param_nums:
			raise Exception("Parameters and values don't match up")
	
	def csv_to_dict(self,csv_headers, csv_row):
		return dict(zip(csv_headers, csv_row))

	def param_keyvalue(self):
		return {self.csv_dict[self.parameters[i]]:self.csv_dict[self.values[i]] for i, v in enumerate(self.parameters)}

	def url(self):
		url = self.csv_dict['URL'] + '?'
		for i,param_num in enumerate(self.param_nums):
			if i > 0:
				url += "&"
			param = urllib2.quote(self.csv_dict["Param" + str(param_num)])
			value = urllib2.quote(self.csv_dict["Value" + str(param_num)])
			url = url + param + '=' + value
		return url
