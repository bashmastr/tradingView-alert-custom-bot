import os,re
from telegram import Bot
from datetime import datetime ,timedelta
import pandas as pd
from server  import *
from db_connection  import *
import logging

from parse import compile
from parse import *

TIMEDIFF = 60 # in seconds


def parse_payload(payload: str) -> dict:

    # payload = b'Pair= FLMUSDT,\nRemarks= 4/5 check ltf volume,\nAlert For= 1d SG,\nTimeFrame= Dsdf,\nCurrentPrice= 0.1215,\nVolume= 12917005, \ntime= 2022-07-13T05:07:19Z'
    if type(payload) == bytes : payload = payload.decode("utf-8") #bytes string to string (byte string start with b'somethin' -> 'something)

    p = compile("Pair= {TICKER},\\nRemarks= {REMARKS},\\nAlert For= 1d SG,\\nTimeFrame= {TIMEFRAME},\\nCurrentPrice= {CURRENTPRICE},\\nVolume= {VOLUME}, \\ntime= {TIME}")
    dic = p.parse(payload)
    
    return dic.named  # .named convert dic result to simple dic

def main(payload: str) -> bool:

    print(f"main->payload -- {payload}")
    dic = parse_payload(payload)
    payload_df = pd.DataFrame( dic ,index=[0])
    payload_df['TIME'] = pd.to_datetime(payload_df['TIME']) + timedelta(hours=4)
    print(f"main->Palyload_df -- {payload_df}")
    print(f"main->Inserting to database -- {payload_df.size}")
    payload_df.to_sql(  'volumetric', 
                        con= engine,
                        index=False,
                        if_exists="append")
                        
    ticker = payload_df['TICKER'][0]
    print("ticker---", ticker)
    df = pd.read_sql(f"""
                    SELECT *,
                    TIMESTAMPDIFF(SECOND, v1.TIME, v2.TIME) as diff
                    FROM volumetric v1 ,  volumetric v2
                    where v1.TICKER = '{ticker}'
                    and v1.TICKER =  v2.TICKER
                    and v1.ID <> v2.ID
                    and v2.ID = (SELECT MAX(ID) FROM volumetric where TICKER = '{ticker}')
                    and TIMESTAMPDIFF(SECOND, v1.TIME, v2.TIME) <= {TIMEDIFF};
                    """, 
                    con=engine)
    if df.empty:
        return "False"
    else:
        return "True"

def sendMessage(data):
    # tg_bot = Bot(token=os.environ['TOKEN'])
    # channel = os.environ['CHANNEL']
    print("Incoming--Data", data)
    # print("formated", main(data))
    return main(data)
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
            "hi",
            parse_mode="MARKDOWN",
        )
    except Exception as e:
        print("[X] Telegram Error:\n>", e)
    return False