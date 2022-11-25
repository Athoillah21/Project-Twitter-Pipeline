from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

today = date.today()

default_args = {
    'owner': 'athoillah',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id='etl_twitter_locale',
    description='First Twitter ETL DAG Using BashOperator and PostgresOperator',
    start_date=datetime(2022, 11, 17),
    schedule_interval='0 * * * *'
    ) as dag:


    task1 = BashOperator(
        task_id="Get_Tweet",
        bash_command="python3 /home/athoillah/airflow/dags/code/define.py ",
        dag=dag
    )


    task2 = BashOperator(
        task_id="Cleansing_and_Sentiment_Analysis",
        bash_command="python3 /home/athoillah/airflow/dags/code/analysis.py ",
        dag=dag
    )

    task3 = PostgresOperator(
        task_id='Create_Database_Table',
        postgres_conn_id='twitter_etl_conn',
        sql="""
        CREATE TABLE IF NOT EXISTS twitter_etl.data (
            userr character varying(256),
            id bigint primary key,
            favorite_count integer, 
            retweet_count integer, 
            created_at date, 
            cleaned_tweet character varying(256), 
            polarity float, 
            subjectivity float);"""
    )

    task4 = PostgresOperator(
        task_id='Overwrite_Data_to_Database',
        postgres_conn_id='twitter_etl_conn',
        sql="""
        create temp table tmp_table(like twitter_etl.data);

        COPY tmp_table FROM '/home/athoillah/Documents/Local_Twitter_Pipeline/output/twitter_data.csv' DELIMITER ',' CSV header;

        insert into twitter_etl.data
        select *
        from tmp_table
        on conflict do nothing;

        drop table tmp_table;"""
    )

    
    task6 = BashOperator(
        task_id="Get_Tweet_For_Archive",
        bash_command="python3 /home/athoillah/airflow/dags/code/define_archive.py ",
        dag=dag
    )


    task7 = BashOperator(
        task_id="Cleansing_and_Sentiment_Analysis_For_Archive",
        bash_command="python3 /home/athoillah/airflow/dags/code/analysis_archive.py ",
        dag=dag
    )

    task1 >> task2 >> task3 >> task4
    task6 >> task7

    # task4 = PostgresOperator(
    #     task_id='Truncate_Database',
    #     postgres_conn_id='twitter_etl_conn',
    #     sql="""
    #     truncate  twitter_etl."data";"""
    # )

    # task5 = PostgresOperator(
    #     task_id='Copy_Data_to_Database',
    #     postgres_conn_id='twitter_etl_conn',
    #     sql="""
    #     copy twitter_etl.data  from '/home/athoillah/Documents/Local_Twitter_Pipeline/output/twitter_data.csv' delimiter ',' CSV HEADER;"""
    # )