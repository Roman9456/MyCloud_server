import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Проверяем правильность загруженных переменных
print(f"Django DB User: {os.getenv('DJANGO_DB_USER')}")
print(f"Django DB Password: {os.getenv('DJANGO_DB_PASSWORD')}")
print(f"Django DB Host: {os.getenv('DJANGO_DB_HOST')}")
print(f"Django DB Name: {os.getenv('DJANGO_DB_NAME')}")

# Подключаемся к PostgreSQL
def create_database():
    try:
        conn = psycopg2.connect(
            dbname='postgres', 
            user=os.getenv('DJANGO_DB_USER'),
            password=os.getenv('DJANGO_DB_PASSWORD'),
            host=os.getenv('DJANGO_DB_HOST')
        )
        conn.autocommit = True  # Включаем автокоммит, чтобы команды типа CREATE DATABASE работали
        cursor = conn.cursor()

        # Проверка на существование базы данных
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (os.getenv('DJANGO_DB_NAME'),))
        exists = cursor.fetchone()

        if not exists:
            # Если базы данных нет, создаем
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(os.getenv('DJANGO_DB_NAME'))))
            print(f"Database {os.getenv('DJANGO_DB_NAME')} created successfully.")
        else:
            print(f"Database {os.getenv('DJANGO_DB_NAME')} already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

# Запуск функции
if __name__ == '__main__':
    create_database()
