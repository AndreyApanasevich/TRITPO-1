from dparser import Parser
from TextNotofocationProcessor import NotificationsORM
from datetime import datetime
from log import Log

class DialogProcessor:
	def __init__(self):
		self.__open_dialogs = {};
		self.__notifications = NotificationsORM();

	def prepare_values(self):
		return {'tstart':0, 'tend': 0}

	def process_text(self, content, chat_id):
		current_context = self.prepare_values();
		if(chat_id in self.__open_dialogs):
			current_context = self.__open_dialogs[chat_id];

		parser = Parser();
		content = content.lower();
		current_context.pop('error', None)
		parser.parse_time(content, current_context)
		parser.parse_text_payload(content, current_context)

		if('error' in current_context):
			return current_context['error']

		preview = self.add_notification(current_context, chat_id)
		current_context.pop(chat_id, None)
		return preview

	def add_notification(self, context, chat_id):
		self.__notifications.add(context, chat_id)
		preview = "Создано '" + context['payload'] + "' at " + str(context['time'])
		Log(preview);
		# print("Log: %s - %s" %(datetime.now(), preview))
		return preview