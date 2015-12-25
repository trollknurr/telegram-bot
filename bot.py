import os
import bot_features.weather

from telegram import Updater

token = os.environ['BOT_TOKEN']
updater = Updater(token, workers=4)

dp = updater.dispatcher

bot_features.weather.register_bot_feature(dp)

update_queue = updater.start_polling(poll_interval=5, timeout=10)

while True:
    text = input()

    # Gracefully stop the event handler
    if text == 'stop':
        updater.stop()
        break
