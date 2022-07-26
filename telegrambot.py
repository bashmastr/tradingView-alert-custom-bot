import os,re
from telegram import Bot
from datetime import datetime ,timedelta
import pandas as pd
 
def get_profit_excel(pair : str):

  df = pd.read_excel('Profit-Percentages.xlsx')
  row = df[ (df.PAIRS.str.contains(pair))]
  return (row)

def calculatePrices( currentPrice : float, timeFrame : any, pair = None , stopLoss = 7 ):
  stopLoss = get_profit_excel(pair)['STOP_LOSS'].values[0]
  priceDict = {}

  if str(timeFrame) == '1d' or str(timeFrame) == 'D': #  D for one day timeframe 
    oneDayProfit = float(get_profit_excel(pair)['ONE_DAY_PROFIT'].values[0]) / 100
    oneDayProfitValue= float(currentPrice) * oneDayProfit 
    priceDict['TP'] = float(currentPrice) + oneDayProfitValue 
    stopLossValue = float(currentPrice) * float(stopLoss/100)
    priceDict['SL'] = float(currentPrice)- stopLossValue

    priceDict['TP'] = str( round( priceDict['TP'], 4 ) ) + ' ==> ' +  str(get_profit_excel(pair)['ONE_DAY_PROFIT'].values[0]) + ' %'
    priceDict['SL'] = str( round( priceDict['SL'], 4 )) + ' ==> -' +  str(stopLoss) + ' %'


  elif str(timeFrame) == '240':
    fourHourProfit = float(get_profit_excel(pair)['FOUR_HOUR_PROFIT'].values[0]) / 100
    fourHourProfitValue= float(currentPrice) * fourHourProfit 
    priceDict['TP'] = float(currentPrice) + fourHourProfitValue 

    stopLossValue = float(currentPrice) * float(stopLoss/100)
    priceDict['SL'] = float(currentPrice)-stopLossValue
    priceDict['TP'] = str( round( priceDict['TP'], 4 ) ) + ' ==> ' +  str(get_profit_excel(pair)['FOUR_HOUR_PROFIT'].values[0]) + ' %'
    priceDict['SL'] = str( round( priceDict['SL'], 4 )) + ' ==> -' +  str(stopLoss) + ' %'

  else:
     priceDict['TP'] = 0.0
     priceDict['SL'] = 0.0


  # TPpercent = round(  ((float(priceDict['TP']) - float(currentPrice))   /  float(currentPrice))  * 100 , 2)
  # SLpercent = round(  ((float(priceDict['SL']) - float(currentPrice))   /  float(currentPrice))  * 100 , 2)

  # priceDict['TP'] = str( round( priceDict['TP'], 4 ) ) + ' ==> ' +  str(get_profit_excel(pair)['ONE_DAY_PROFIT']) + ' %'
  # priceDict['SL'] = str( round( priceDict['SL'], 4 )) + ' ==> ' +  str(stopLoss) + ' %'

  return priceDict


def UAETimeFormat(timee : str):

  timee = re.sub("[a-z]|[A-Z]", "", timee)
  timee = timee.strip()
  date_time_obj = datetime.strptime(timee, '%Y-%m-%d%H:%M:%S')
  UAETime = date_time_obj +  timedelta(hours=4)
  return str(UAETime)

def requiredFormat (data : dict):
  result = ''
  for key, value in enumerate(data):
    result += f" {value} = {data[value]} \n"
  return result

def main(data : str): 

  url = 'https://www.tradingview.com/chart/7GGx5HmW/?symbol=BINANCE%3A'

  dataToStr = str(data,"utf-8")
  dataRem = dataToStr.split()
  dataRem = re.sub("\n|\s","", dataToStr)
  dataRem = dataRem.replace('\\n', "")
  dataToList = dataRem.split(',')
  dataFormated = {}

  for row in dataToList:
    key , value = row.split("=")
    dataFormated[key] = value

  PnLDict =  calculatePrices(dataFormated['CurrentPrice'], dataFormated['TimeFrame'],dataFormated['Pair'])
  
  if dataFormated['TimeFrame'] == '240':
    dataFormated['TimeFrame']='4h'
  else:
    dataFormated['TimeFrame']='D'
    
  dataFormated['TP']    = PnLDict['TP'] 
  dataFormated['SL']    = PnLDict['SL']
  dataFormated['URL']    = url + dataFormated['Pair']
  dataFormated['time'] = UAETimeFormat(dataFormated['time'])

  return requiredFormat(dataFormated)
  
def sendMessage(data):
    tg_bot = Bot(token="5434032639:AAGDmDprsGYFYZI3SanqGj9A6MaNM-rOJCo")
    channel = "-1001646160782"
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