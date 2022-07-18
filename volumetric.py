import os,re
from telegram import Bot
from datetime import datetime ,timedelta
import pandas as pd
 
def main(data: str):
  pass

def sendMessage(data):
    tg_bot = Bot(token=os.environ['TOKEN'])
    channel = os.environ['CHANNEL']
    print("Incoming--Data", data)
    print("formated", main(data))
    try:
        print('--->Sending message to telegram')
        tg_bot.sendMessage(
            channel,
            main(data),
            parse_mode="MARKDOWN",
        )
        return True
    except KeyError:
        print('--->Key error - sending error to telegram')
        tg_bot.sendMessage(
            channel,
            main(data),
            parse_mode="MARKDOWN",
        )
    except Exception as e:
        print("[X] Telegram Error:\n>", e)
    return False