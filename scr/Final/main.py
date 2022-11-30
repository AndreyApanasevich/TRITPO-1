import mrbot as Bot
import os


def main():
    botToken = os.getenv('YOUR_TELEGRAM_BOT_TOKEN')
    print(botToken)
    Bot.start(botToken)


if __name__ == '__main__':
    main()
