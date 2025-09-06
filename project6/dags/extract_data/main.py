from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import zipfile
import os

DATA_DIR = '/opt/airflow/data'
DATA_FILE = 'daaa.zip'

def extract_zip():
    zip_path = os.path.join(DATA_DIR, DATA_FILE)
    extract_to = os.path.join(DATA_DIR, "extracted")
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {zip_path} to {extract_to}")

with DAG(
    dag_id="extract_zip_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # run manually
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_zip",
        python_callable=extract_zip
    )