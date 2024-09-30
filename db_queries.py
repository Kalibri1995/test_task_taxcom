import sqlite3


def create_table(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS taxcom_test (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        column_int INTEGER,
        column_str TEXT
    )''')

    conn.commit()
    conn.close()


def insert_taxcom_test(db_name, data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Вставка данных в таблицу
    for row in data:
        int_value = row[0]
        # Сохраняем каждый текстовый элемент вместе с его соответствующим int значением
        for text in row[1:]:
            cursor.execute("INSERT INTO taxcom_test (column_int, column_str) VALUES (?, ?)", (int_value, text))

    conn.commit()
    conn.close()
