#!/usr/bin/env python3
import pandas as pd
# from pandas.io import sql
from sqlalchemy import create_engine, types

MYSQL_USER 		= 'root'
MYSQL_PASSWORD 	= 'pass'
MYSQL_HOST_IP 	= '127.0.0.1'
MYSQL_PORT		= '8877'
MYSQL_DATABASE	= 'weight'

engine = create_engine('mysql+mysqlconnector://'+MYSQL_USER+':'+MYSQL_PASSWORD+'@'+MYSQL_HOST_IP+':'+MYSQL_PORT+'/'+MYSQL_DATABASE, echo=False)

# df = pd.read_csv('containers2.csv', skiprows=[0])
df = pd.read_csv('containers1.csv')
# df = pd.DataFrame(data=df)
print(df)

# chunksize = 500

# idx = 1
# for looprows in pd.read_csv("containers2.csv", chunksize=chunksize, usecols=['id', 'lbs'], sep=" "):
# for looprows in df:

# 	if idx == 1: 
# 		exists = 'replace'
# 	else:
# 		exists = 'append'

# 	looprows.to_sql(name=MYSQL_DATABASE, con=engine, if_exists=exists, index=False, chunksize=chunksize)

# 	print(str(chunksize * idx)+" Processed");
# 	idx = idx+1


engine = create_engine('mysql+mysqlconnector://root:pass@localhost:8877/weight')
with engine.connect() as conn, conn.begin():
    df.to_sql('containers_registered', conn, if_exists='replace')
