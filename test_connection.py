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


conn_executemany = create_engine(
    f"mssql+pyodbc://ITRemoteUser:Remote009I!@{DSN}/{DB}?driver={DRIVER}", fast_executemany=True
)

conn_executemany.execute('select *from Api_Fgx_log')
