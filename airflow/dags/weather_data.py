import os
import requests
import json
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


# Функция для загрузки данных о погоде
def download_data():
    # Получаем API ключ из переменной окружения
    api_key = os.getenv('OPENWEATHER_API_KEY')
    city = 'London'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)  # Выполняем запрос к API
    #data = response.json()  # Преобразуем ответ в формат JSON

    # Сохраняем данные в локальный файл
    with open('/tmp/weather_data.json', 'w') as file:
        json.dump(response.content, file)


# Функция для обработки данных
def process_data():
    with open('/tmp/weather_data.json') as file:
        data = json.load(file)  # Загружаем данные из файла
    # Преобразуем температуру из Кельвинов в Цельсии
    temp_kelvin = data['main']['temp']
    temp_celsius = temp_kelvin - 273.15
    df = pd.DataFrame({'temperature': [temp_celsius]})
    df.to_csv('/tmp/processed_weather_data.csv', index=False)  # Сохраняем обработанные данные в CSV


# Функция для сохранения данных в формат Parquet
def save_data():
    df = pd.read_csv('/tmp/processed_weather_data.csv')  # Загружаем обработанные данные из CSV
    df.to_parquet('/tmp/weather.parquet')  # Сохраняем данные в формат Parquet


# Аргументы по умолчанию для задач
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 5),
    'retries': 1,
}

# Создание DAG
dag = DAG(
    'weather_data_pipeline_dag',
    default_args=default_args,
    description='DAG для обработки данных о погоде',
    schedule_interval='@daily',  # DAG будет запускаться ежедневно
)

# Определение задач
download_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag,
)

save_task = PythonOperator(
    task_id='save_data',
    python_callable=save_data,
    dag=dag,
)

# Определение порядка выполнения задач
download_task >> process_task >> save_task