from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from main import define_tweet, cleaned_and_sentiment

default_args = {
    'owner': 'athoillah',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


dag = DAG(
    default_args=default_args,
    dag_id='etl_twitter_v01',
    description='First Twitter ETL DAG',
    start_date=datetime(2022, 11, 17),
    schedule_interval='@daily'
)

task1 = PythonOperator(
    task_id='Define_Tweet',
    python_callable=define_tweet,
    dag=dag
)

task2 = PythonOperator(
    task_id='Cleaned_and_SentimentAnalysis',
    python_callable=cleaned_and_sentiment,
    dag=dag
)

