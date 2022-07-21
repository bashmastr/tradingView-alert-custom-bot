from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy

server = 'localhost'
username = 'root'
password = ''
db = 'telegram_bot'
port = '3306'

engine = sqlalchemy.create_engine(f'mysql://{username}:@{server}/{db}') # connect to server

# data = pd.read_sql_table("test_table", con = engine)
# print(data['TIME'].dt.second)
