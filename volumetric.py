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
    # payload = b'Pair= FORTHUSDT,\nRemarks= 6p na 3k-myfav,\nAlert For= Pumping volume,\nTimeFrame= 1,\nVolume= 3k+,\nCurrentPrice= 3.86,\ntime= 2022-07-28T15:24:16Z'
    # payload = b'Pair= FLMUSDT,\nRemarks= 4/5 check ltf volume,\nAlert For= 1d SG,\nTimeFrame= Dsdf,\nCurrentPrice= 0.1215,\nVolume= 12917005, \ntime= 2022-07-13T05:07:19Z'
    if type(payload) == bytes : payload = payload.decode("utf-8") #bytes string to string (byte string start with b'somethin' -> 'something)

    dataRem = re.sub("\n"," ", payload)
    dataRem = dataRem.replace("\\n"," ")
    dataToList = dataRem.split(',')

    dataFormated = {}
    for row in dataToList:
        key , value = row.split("=")
        key = key.strip().upper()
        value = value.strip()
        dataFormated[key] = value
    print('payload after parse', dataFormated)
    return dataFormated

def requiredFormat (data : dict):

    result = ''
    for key, value in enumerate(data):
        result += f" {value}  =  {str(data[value])}  \n"
    return result

def sendMessage(data):

    tg_bot = Bot(token="5575339974:AAFUjuF1zV8bZ3HeoEePkpBlErnYBi9AS_U")
    channel = "-1001787592229"

    try:
        print('--->Sending message to telegram')
        tg_bot.sendMessage(
            channel,
            data,
            parse_mode="MARKDOWN",
        )
        return True
    except KeyError:
        print('--->Key error - sending error to telegram')
        tg_bot.sendMessage(
            channel,
            data,
            parse_mode="MARKDOWN",
        )
    except Exception as e:
        print("[X] Telegram Error:\n>", e)        
    return False


def main(payload: str):
    url = 'https://www.tradingview.com/chart/7GGx5HmW/?symbol=BINANCE%3A'
    # print(f"main->payload -- {payload}")
    dic = parse_payload(payload)
    payload_df = pd.DataFrame( dic ,index=[0])

    payload_df['TIME'] = pd.to_datetime(payload_df['TIME']) + timedelta(hours=4)
    # print(f"main->Palyload_df -- {payload_df}")
    # print(f"main->Inserting to database -- {payload_df.size}")
    payload_df.rename(columns = {'PAIR':'TICKER'}, inplace = True)

    payload_df = payload_df[['TICKER', 'REMARKS', 'CURRENTPRICE','VOLUME', 'TIMEFRAME', 'TIME']]

    payload_df.to_sql(  'volumetric',
                        con= engine,
                        index=False,
                        if_exists="append")
    print("ticker ----",payload_df['TICKER'][0])
    ticker = payload_df['TICKER'][0]
    # print("ticker---", ticker)
    df = pd.read_sql(f"""
                    SELECT *,

                TIMESTAMPDIFF(SECOND, v2.TIME, v1.TIME) AS diff 
                from volumetric v1, volumetric v2
                where v1.id = (SELECT max(id) FROM volumetric
                        WHERE TICKER = '{ticker}')
                and   v2.id = (  
                    SELECT MAX(id) from volumetric 
                        where id <> (
                            SELECT max(id) FROM volumetric 
                            WHERE TICKER = '{ticker}') 
                    and  TICKER = '{ticker}')
                and TIMESTAMPDIFF(SECOND, v2.TIME, v1.TIME) <= 119
                    """, 
                    con=engine)
    dic['URL'] = url + dic['PAIR']
    dic['TIME'] = payload_df['TIME'][0]
    print("dataframe" , dic)
    if df.empty:
        return False
    else:
        
        RESULT = requiredFormat(dic)
        sendMessage(RESULT)
        return True

