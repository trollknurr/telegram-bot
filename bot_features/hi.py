GREET_TEXT = """
Приветствую тебя, {} {}!

Список доступных комманд:

/weather погода в Москве (alias "погода")
/xkcd последний комикс
"""


def greet_user(bot, update):
    bot.sendMessage(update.message.chat_id,
                    text=GREET_TEXT.format(update.message.from_user.first_name, update.message.from_user.last_name))


def register_bot_feature(dispatcher):
    dispatcher.addTelegramCommandHandler("hi", greet_user)
    dispatcher.addTelegramRegexHandler(r"^привет$", greet_user)
