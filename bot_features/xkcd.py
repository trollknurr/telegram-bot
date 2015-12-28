import requests
import telegram

LAST_LINK = 'http://xkcd.com/info.0.json'
MESSAGE_TEMPLATE = """
*{alt}*
"""


def get_xkcd_random_image(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=telegram.ChatAction.TYPING)
    r = requests.get(LAST_LINK)
    data = r.json()
    bot.sendMessage(update.message.chat_id,
                    text=MESSAGE_TEMPLATE.format(alt=data['alt']),
                    parse_mode=telegram.ParseMode.MARKDOWN)
    bot.sendPhoto(chat_id=update.message.chat_id,
                  photo=data['img'])


def register_bot_feature(dispatcher):
    dispatcher.addTelegramCommandHandler("xkcd", get_xkcd_random_image)
