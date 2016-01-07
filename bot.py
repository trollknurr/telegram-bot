import os
import sys
import logging

import bot_features.weather
import bot_features.hi
import bot_features.xkcd
import bot_features.chess

from telegram import Updater

token = os.environ['BOT_TOKEN']

# Set up logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = \
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

logger = logging.getLogger(__name__)

updater = Updater(token, workers=4)
dp = updater.dispatcher

close_callbacks = list()

bot_features.weather.register_bot_feature(dp)
bot_features.hi.register_bot_feature(dp)
bot_features.xkcd.register_bot_feature(dp)
close_callbacks.append(bot_features.chess.register_bot_feature(dp))

update_queue = updater.start_polling(poll_interval=2, timeout=10)


def shut_down():
    updater.stop()
    for callback in close_callbacks:
        callback()


while True:
    try:
        text = input()
    except KeyboardInterrupt:
        shut_down()
        break

    # Gracefully stop the event handler
    if text == 'stop':
        shut_down()
        break
