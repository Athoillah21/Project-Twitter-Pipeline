import json
import psycopg2 as pg
from zipfile import ZipFile
import pandas as pd
from sqlalchemy import create_engine



file = '/home/athoillah/Documents/Local_Twitter_Pipeline/output/twitter_data.csv'

database='airflow_db'
user='airflow_user'
password='airflow_pass'
host='localhost'
port='5432'
table_name = 'data'


#Init Posgresql connection
conn = pg.connect(database=database,
                  user=user,
                  password=password,
                  host=host,
                  port=port)

conn.autocommit=True
cursor=conn.cursor()


#Load zipped file to dataframe
df = pd.read_csv(file, skiprows=[0])


#create engine
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

#insert to postgres
df.to_sql(table_name, engine, if_exists='append', index=False, schema='twitter_etl')