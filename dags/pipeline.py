from datetime import datetime, timedelta
from connect_mongo import connect_to_mongo
from readfile import list_file_names_in_folder
from extract import extract
from store_raw_in_mongo import store_in_mongo
from find_doccuments_byid import find_documents_by_ids
from training import training
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from web_scrape import scrape
import json
import logging
default_args = {
    'owner': 'tumrabert',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}
def list_files_task():
    try:
        folder_path = "../data"
        return list_file_names_in_folder(folder_path)
    except Exception as e:
        logging.error(f"Error in list_files_task: {e}")
        raise

def get_list_files_to_extract(task_instance):
    try:
        list_files = task_instance.xcom_pull(task_ids='list_files')
        return extract(list_files)
    except Exception as e:
        logging.error(f"Error in get_list_files_to_extract: {e}")
        raise

def do_store_in_mongo(task_instance):
    try:
        client=connect_to_mongo()
        data = task_instance.xcom_pull(task_ids='extract_information')
        store_in_mongo(client,data)
    except Exception as e:
        logging.error(f"Error in do_store_in_mongo: {e}")
        raise

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        logging.error(f"Error in read_json_file: {e}")
        raise
def do_fetch_cursor_from_ids():
    try:
        client=connect_to_mongo()
        ids = read_json_file('../scopus_ids.json')
        return find_documents_by_ids(client,ids)
    except Exception as e:
        logging.error(f"Error in do_fetch_cursor_from_ids: {e}")
        raise

def do_train_and_predict(task_instance):
    try:
        return training(task_instance.xcom_pull(task_ids='fetch_cursor_from_ids'))
    except Exception as e:
        logging.error(f"Error in do_train_and_predict: {e}")
        raise

def do_store_result_from_training(task_instance):
    try:
        client=connect_to_mongo()
        data = task_instance.xcom_pull(task_ids='train_and_predict')
        store_in_mongo(client,data)
    except Exception as e:
        logging.error(f"Error in do_store_result_from_training: {e}")
        raise

with DAG(
    dag_id='Scopus_pipeline',
    default_args=default_args,
    description='This is our first dag that we write',
    schedule_interval='@hourly'
) as dag:

    scraping_files = PythonOperator(
        task_id='scrape_by_api',
        python_callable=scrape,
        dag=dag,
    )
    list_files = PythonOperator(
        task_id='list_files',
        python_callable=list_files_task,
        dag=dag,
    )
    
    extract_task = PythonOperator(
        task_id='extract_information',
        python_callable=get_list_files_to_extract,
        provide_context=True,
        dag=dag,
    )
    store_raw_task = PythonOperator(
        task_id='store_raw_into_mongo',
        python_callable=do_store_in_mongo,
        dag=dag,
    )
    
    fetch_cursor_from_ids = PythonOperator(
        task_id='fetch_cursor_from_ids',
        python_callable=do_fetch_cursor_from_ids,
        provide_context=True,
        dag=dag,
    )
    
    train_and_predict = PythonOperator(
        task_id='train_and_predict',
        python_callable=do_train_and_predict,
        provide_context=True,
        dag=dag,
    )
    
    store_result_from_training = PythonOperator(
        task_id='store_result_from_training',
        python_callable=do_store_result_from_training,
        dag=dag,
    )
    
    delete_files = BashOperator(
        task_id='delete_files',
        bash_command='rm -rf ../data/*',
        dag=dag,
    )
    