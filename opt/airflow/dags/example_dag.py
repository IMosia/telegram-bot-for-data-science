"""
This is an example of a DAG that collects data from the database
It mokes some calculations and sends the results to the telegram
Basically retreves whole table from the database, counts the number of rows
And sends the number of rows to the telegram
"""

from datetime import datetime, timedelta
import os

import psycopg2
import telegram
import dotenv
import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task


# Load environment variables
dotenv.load_dotenv()
DB_HOST = os.getenv('DB_HOST')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DB_PORT = os.getenv('DB_EXTERNAL_PORT')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CREATOR_USER_ID = os.getenv('CREATOR_USER_ID')


# Default arguments for the DAG
default_args = {
    'owner': 'ivan',
    'depends_on_past': False, # If previous task failed, it will not affect the current task
    'start_date': datetime(2024, 10, 10), # Start date of the DAG
    'retries': 1, # If task fails, it will be retried once
    'retry_delay': timedelta(minutes=30), # After failure, retry in 30 minutes
}

# This is a cron expression defining the schedule
# For more information, see https://en.wikipedia.org/wiki/Cron and https://crontab.cronhub.io/
# This particular schedule means that the DAG will run every day at 7:00 UTC
schedule_interval = '0 7 * * *'

def connect_to_get_df(query
                      , host=DB_HOST
                      , port=DB_PORT
                      , database=POSTGRES_DB
                      , user=POSTGRES_USER
                      , password=POSTGRES_PASSWORD
                      ):
    """
    Procedure to connect to the database and get the data in the form of a pandas DataFrame
    According to provided query
    Input:
        query - str - SQL query
    Output:
        df - pd.DataFrame - DataFrame with the data
    """
    # Expression with psycopg2.connect is used to ensure that the connection is closed after the block
    with psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    ) as conn:
        df = pd.read_sql(query, conn)
    return df

@dag(schedule_interval=schedule_interval
     , default_args=default_args
     , catchup=False # 
     , tags=['daily']
     , description="Daily Test DAG")
def daily_dag():
    ########################################################
    # Collecting data from the database
    ########################################################
    @task()
    def get_test_data():
        """
        Collects all data from the test_table
        """
        query = """
            SELECT *
            FROM test_table
        """
        df = connect_to_get_df(query)
        return df

    ########################################################
    # Calculates metrics
    ########################################################

    @task()
    def get_num_rows_from_df(df):
        """
        Count number of rows in collected data
        """
        num_rows = df.shape[0]
        return num_rows

    ########################################################
    # Preparing data for sending and sending
    ########################################################

    @task()
    def send_to_telegram(num_rows):
        """
        Function to send data to telegram
        """
        bot = telegram.Bot(token=BOT_TOKEN)
        text = f"Number of rows in the table: {num_rows}"
        bot.sendMessage(chat_id=CREATOR_USER_ID
                        , text=text)
        return None

    ########################################################
    # Pipeline
    # Description of the order of the tasks
    # And their dependencies
    ########################################################

    df = get_test_data()
    num_rows = get_num_rows_from_df(df)
    send_to_telegram(num_rows)

daily_dag = daily_dag()
