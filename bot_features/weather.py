import xml.etree.cElementTree as ElementTree

import requests
import telegram

URL = 'https://export.yandex.ru/weather-ng/forecasts/27612.xml'


def get_weather():
    r = requests.get(URL, verify=False)
    root = ElementTree.XML(r.content)
    fact = root.find('{http://weather.yandex.ru/forecast}fact')
    t = fact.find('{http://weather.yandex.ru/forecast}temperature').text
    verbose = fact.find('{http://weather.yandex.ru/forecast}weather_type').text
    return "{}, {}".format(t, verbose)


def weather_command(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=telegram.ChatAction.TYPING)
    bot.sendMessage(update.message.chat_id, text="Погода в Москве: \n {}".format(get_weather()))


def register_bot_feature(dispatcher):
    dispatcher.addTelegramCommandHandler("weather", weather_command)
    dispatcher.addTelegramRegexHandler(r"^погода$", weather_command)


if __name__ == '__main__':
    print(get_weather())
