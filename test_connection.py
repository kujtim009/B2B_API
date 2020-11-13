import json
import urllib
import time
import pandas
import pyodbc
import pandas as pd
from sqlalchemy import create_engine, event

DRIVER = "ODBC Driver 17 for SQL Server"
DSN = "208.118.231.180:21201"
DB = "InsertTool"
TABLE = "CBD_Sample_test"
sql_username = "ITRemoteUser"
sql_password = "Remote009I!"
# conn_executemany = create_engine(
#     f"mssql+pyodbc://ITRemoteUser:Remote009I!@{DSN}/{DB}?driver={DRIVER}", fast_executemany=True
quotedLocalPc = urllib.parse.quote_plus(
    "DRIVER={SQL Server};SERVER=208.118.231.180,21201;UID=ITRemoteUser;PWD=Remote009I!;DATABASE=InsertTool;Trusted_Connection=no;")

# quoted = quote_plus(conn)
new_con = 'mssql+pyodbc:///?odbc_connect={}'.format(quotedLocalPc)
# engine = create_engine(new_con)
engine = create_engine(new_con)

engine.execute('select *from Api_Fgx_log')
