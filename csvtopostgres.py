import psycopg2
  
conn = psycopg2.connect(database="airflow_db",
                        user='airflow_user', password='airflow_pass', 
                        host='127.0.0.1', port='5432'
)
  
conn.autocommit = True
cursor = conn.cursor()
  
sql = """copy twitter_etl.data  from '/home/athoillah/Documents/Local_Twitter_Pipeline/output/twitter_data_original.csv' delimiter ',' CSV HEADER ;"""


cursor.execute(sql)

conn.commit()
conn.close()
