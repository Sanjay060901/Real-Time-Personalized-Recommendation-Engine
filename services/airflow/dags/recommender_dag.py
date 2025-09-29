from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


with DAG('recommender_train', start_date=datetime(2025,1,1), schedule_interval='@daily', catchup=False) as dag:
train = BashOperator(
task_id='train_model',
bash_command='python /opt/airflow/dags/../../services/model-training/train_model.py'
)


train
