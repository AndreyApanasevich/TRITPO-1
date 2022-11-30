from TextNotofocationModel import TextNotification
from datetime import datetime


class NotificationsORM:

    # def __init__(self):

    def add(self, context, chatId):
        TextNotification.create_table()
        TextNotification.create(chat_id=chatId, payload=context['payload'], time=context['time'])

    def show_all(self, chat_id):
        rows = TextNotification.select().where(TextNotification.chat_id == chat_id)
        notification_list = ""
        counter = 1
        for row in rows:
            notification_list += str(counter) + ") " + row.payload + " at " + str(row.time) + "\n"
            counter += 1

        if notification_list == "":
            notification_list = "Nothing to display :("
        return notification_list


    def get_all(self, now):
        return TextNotification.select().where(TextNotification.time <= now)
