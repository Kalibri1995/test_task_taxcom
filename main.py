import json
import os

from dotenv import load_dotenv

from db_queries import create_table, insert_taxcom_test
from utils import read_file


load_dotenv()

FILES_DIR = os.getenv("FILES_DIR")
DB_NAME = os.getenv("DB_NAME")


# Основная функция для выполнения всего процесса
def main():
    file_path1 = os.path.join(FILES_DIR, "Тестовый файл1.txt")
    file_path2 = os.path.join(FILES_DIR, "Тестовый файл2.txt")

    # Чтение данных из файлов
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)

    # Объединение данных и сортировка данных
    sorted_data = sorted(data1 + data2, key=lambda x: x[1].lower() if len(x) > 1 else '')

    # Сохранение в JSON
    with open("sorted_data.json", 'w', encoding='utf-8') as json_file:
        json.dump(sorted_data, json_file, ensure_ascii=False, indent=4)

    # Сохранение в базу данных
    create_table(DB_NAME)
    insert_taxcom_test(DB_NAME, sorted_data)


# Запуск программы
if __name__ == "__main__":
    main()
