import os
import sys
import logging
import bot_features.weather
import bot_features.hi

from telegram import Updater

token = os.environ['BOT_TOKEN']

# Set up logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = \
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

logger = logging.getLogger(__name__)


updater = Updater(token, workers=4)
dp = updater.dispatcher

bot_features.weather.register_bot_feature(dp)
bot_features.hi.register_bot_feature(dp)

update_queue = updater.start_polling(poll_interval=5, timeout=10)

while True:
    text = input()

    # Gracefully stop the event handler
    if text == 'stop':
        updater.stop()
        break
