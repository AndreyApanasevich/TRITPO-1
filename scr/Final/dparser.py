from datetime import datetime, time, timedelta

class Parser:

	def __init__(self):
		self.__relative_keys = ['через', 'спустя']
		self.__absolute_keys = ['сегодня', 'завтра', 'послезавтра']
		self.__keyword = 'напомни'
		self.__err_usage = "Используй: Напомни *когда* *что*"
		self.__digits_worlds = {'один': 1, 'одну': 1, 'две' : 2, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5, 'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9, 'десять': 10}
		self.__dimention_worlds = {'час': 'hour', 'мин': 'min', 'ден': 'day', 'дня': 'day', 'нед': 'week'}

	def parse_time(self, instring, context):
		if (self.__keyword in instring):
			# check if instring contains any elements of relative_keys
			if (any(elem in instring for elem in self.__relative_keys)):
				self.parse_relative(instring, context)
			elif (any(elem in instring for elem in self.__absolute_keys)):
				self.parse_absolute(instring, context)
			else:
				context['error'] = self.__err_usage
		else:
			if (self.contain_native(instring)):
				self.parse_native(instring, context)
			else:
				context['error'] = self.__err_usage

	def parse_regular_digit(self, data, structure):
		try:
			structure['digit'] = int(data)
			return True
		except ValueError:
			print(data)
			if (data in self.__digits_worlds):
				structure['digit'] =  self.__digits_worlds[data]
				return True
			else:
				return False

	def parse_dimention(self, data, structure):
		if (data[:3] in self.__dimention_worlds):
			structure['dimention'] = self.__dimention_worlds[data[:3]]

	def ismin(self, structure):
		if (structure['dimention'] == 'min'):
			return True;
		return False;

	def ishour(self, structure):
		if (structure['dimention'] == 'hour'):
			return True;
		return False;

	def isday(self, structure):
		if (structure['dimention'] == 'day'):
			return True;
		return False;

	def isweek(self, structure):
		if (structure['dimention'] == 'week'):
			return True;
		return False;

	def parse_relative(self, instring, context):
		# ex: напоини через [3] часа
		indata = instring.split(' ')
		structure = {'digit': 1, 'dimention': 'nope'}

		parse_index = indata.index(self.__keyword) + 2
		isdigit = self.parse_regular_digit(indata[parse_index], structure)
		if(isdigit):
			parse_index = parse_index + 1

		self.parse_dimention(indata[parse_index], structure)

		if ('nope' in structure.values()):
			context['error'] = "Не указано когда!"
		else:
			rel_minutes = self.ismin(structure) * structure['digit'];
			rel_hours = self.ishour(structure) * structure['digit'];
			rel_deys = (self.isday(structure) + self.isweek(structure) * 7) * structure['digit'];

			ttime = datetime.now() +  timedelta(days= rel_deys, hours=rel_hours, minutes=rel_minutes)
			context['time'] = ttime
			context['tend'] = instring.find(indata[parse_index]) + len(indata[parse_index]) + 1



	def parse_day(self, data, structure):
		if (data in self.__absolute_keys):
			structure['tday'] = self.__absolute_keys.index(data)
			return True
		else:
			return False

	def parse_complex_time(self, data, structure):
		if (not self.contain_native(data) and data in self.__digits_worlds):
			data =  str(self.__digits_worlds[data])

		if (':' not in data):
			data = data + ':00'
		time = 	datetime.strptime(data, '%H:%M').time()
		structure['ttime'] = time

	def parse_absolute(self, instring, context):
		# ex: напомги завтра в 8
		indata = instring.split(' ')
		structure = {'tday': 0, 'ttime': time(8, 0)}
		parse_index = indata.index(self.__keyword, 0) + 1

		isday = self.parse_day(indata[parse_index], structure);
		if(isday and ((parse_index + 1) < len(indata)) and ('в' == indata[parse_index + 1])):
			parse_index = parse_index + 2
			self.parse_complex_time(indata[parse_index], structure)

		context['tend'] = instring.find(indata[parse_index]) + len(indata[parse_index]) + 1

		now = datetime.now()
		ttime = datetime(now.year, now.month, now.day + structure['tday'], hour=structure['ttime'].hour, minute=structure['ttime'].minute, second=0)
		context['time'] = ttime

		if ('error' in structure):
			context['error'] = "Непонятное чет время"

	def contain_native(self, instring):
		return any(char.isdigit() for char in instring)

	def parse_native(self, instring, context):
		context['error'] = "Непонятное время"

	def parse_text_payload(self, instring, context):
		dstart = context['tend']
		res = instring[dstart:]
		if ('error' in context):
			return
		elif (len(res) == 0 and 'payload' not in context or context['tend'] == 0):
			context['error'] = self.__err_usage
		else:
			context['payload'] = res;