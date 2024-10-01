## Структура проекта

- `main.py`: Основной файл, в котором выполняется обработка данных.
- `db_queries.py`: Файл с функциями для работы с базой данных.
- `utils.py`: Вспомогательные функции, включая чтение файлов.
- `.env`: Файл для хранения конфигурационных переменных, таких как пути к файлам и имя базы данных.
- `requirements.txt`: Список необходимых библиотек для работы проекта.


## Настройка

Создайте файл `.env` в корневой директории проекта и добавьте в него следующие переменные:

```plaintext
DB_NAME="test_task_taxcom"
FILES_DIR="C:/Path/To/Your/Test/Files/"  # Замените на путь к вашим тестовым файлам
```


## Установка

Для установки зависимостей выполните следующую команду:

```bash
pip install -r requirements.txt
```






## Тестовое задание SQL

## Запросы на создание таблиц с описанием полей

Таблицы с менеджерами:

```sql
CREATE TABLE managers (
    id SERIAL PRIMARY KEY,              -- Уникальный идентификатор менеджера
    first_name VARCHAR(255) NOT NULL,   -- Имя менеджера
    last_name VARCHAR(255) NOT NULL,    -- Фамилия менеджера
    middle_name VARCHAR(255),           -- Отчество менеджера (может быть NULL)
    birth_date DATE NOT NULL,           -- Дата рождения менеджера
    registration_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Дата регистрации менеджера
    role VARCHAR(50) NOT NULL,          -- Роль менеджера (например, администратор, менеджер)
    login VARCHAR(100) NOT NULL UNIQUE, -- Логин для авторизации
    password VARCHAR(255) NOT NULL,     -- Пароль для авторизации (Хранить в хэшированном виде)
    department_id INT,                  -- Внешний ключ на отдел (если потребуется)
    CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(id) -- Внешний ключ на отдел
);
```

Таблица с контрагентами:

```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,             -- Уникальный идентификатор контрагента
    name VARCHAR(255) NOT NULL,        -- Название компании
    surname VARCHAR(100),              -- Фамилия контрагента
    first_name VARCHAR(100),           -- Имя контрагента
    middle_name VARCHAR(100),          -- Отчество контрагента
    birth_date DATE,                   -- Дата рождения контрагента
    registration_date TIMESTAMP,       -- Дата регистрации контрагента
    role VARCHAR(50),                  -- Роль (например, клиент, партнер и т.д.)
    login VARCHAR(100) UNIQUE,         -- Логин контрагента
    password VARCHAR(255) NOT NULL,    -- Пароль контрагента
    passport_number VARCHAR(20),       -- Паспортные данные
    phone_number VARCHAR(20),          -- Номер телефона контрагента
    tax_id VARCHAR(20),                -- ИНН контрагента
    address TEXT                       -- Адрес контрагента
);
```

Таблица со счетами:

```sql
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,          -- Уникальный идентификатор счета
    invoice_number VARCHAR(50) NOT NULL,  -- Номер счета
    date TIMESTAMP NOT NULL,        -- Дата выставления счета
    manager_id INT NOT NULL,        -- Внешний ключ на таблицу менеджеров
    client_id INT NOT NULL,         -- Внешний ключ на таблицу контрагентов
    amount DECIMAL(15, 2),          -- Сумма счета
    status VARCHAR(50),             -- Статус счета (выставлен, оплачен, отменен и т.д.)
    details TEXT,                   -- Содержимое счета
    CONSTRAINT fk_manager FOREIGN KEY (manager_id) REFERENCES managers(id),
    CONSTRAINT fk_client FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

Таблица с расписанием нумераций счетов:

Данная таблица используется для получения актуального минимального номера счета с определенной даты.
Используется при создании нового счета для менеджера.

```sql
CREATE TABLE invoice_numbers (
    id SERIAL PRIMARY KEY,            -- Уникальный идентификатор записи
    manager_id INT NOT NULL,          -- Внешний ключ на таблицу менеджеров
    start_date TIMESTAMP NOT NULL,    -- Дата начала новой нумерации
    next_invoice_number INT NOT NULL, -- Следующий номер счета для менеджера с этой даты
    CONSTRAINT fk_manager_invoice_numbers FOREIGN KEY (manager_id) REFERENCES managers(id)
);
```




## Связи между таблицами

Связь между таблицами invoices (счета) и managers (менеджеры):
Тип связи: Один ко многим
Один менеджер может выставить множество счетов, но каждый счет может быть выставлен только одним менеджером.

Связь между таблицами invoices (счета) и clients (контрагенты):
Тип связи: Один ко многим
Один контрагент может быть получателем нескольких счетов, но каждый счет может быть выставлен только одному контрагенту.

Связь между таблицами invoice_numbers (нумерация счетов) и managers (менеджеры):
Тип связи: Один ко многим
Для одного менеджера может быть несколько записей о начале новой нумерации счетов, но каждая запись относится только к одному менеджеру.




## Индексы

Индексы на таблице invoices(Счета):

```sql
-- Данный индекс используется для поиска последних 20 счетов для менеджера по дате
CREATE INDEX idx_invoices_manager_date ON invoices(manager_id, date);

-- Данный индекс используется для поиска счета по номеру
CREATE INDEX idx_invoices_number ON invoices(invoice_number);

-- Данный индекс используется для поиска всех счетов по контрагенту
CREATE INDEX idx_invoices_client ON invoices(client_id);
```

Индексы на таблице invoice_numbers(Нумераций счетов):

```sql
-- Данный индекс используется для поиска текущего номера счета для менеджера с учетом начала новой нумерации.
CREATE INDEX idx_invoices_manager_date ON invoices(manager_id, date);
```




## SQL запросы

Получение последних 20 счетов, выставленных менеджером:
```sql
SELECT * 
FROM invoices 
WHERE manager_id = :manager_id 
    AND status = 'Выставлен'
ORDER BY date DESC 
LIMIT 20;
```

Получение ранее выставленных счетов:

При получениее за неделю: ``` AND i.date >= NOW() - INTERVAL '1 week' ```
При получениее за месяц: ``` AND i.date >= NOW() - INTERVAL '1 month' ```
При получениее за год: ``` AND i.date >= NOW() - INTERVAL '1 year' ```
```sql
SELECT i.*, c.name, c.surname, c.first_name, c.middle_name
FROM invoices i 
JOIN clients c ON c.id = i.client_id
WHERE i.manager_id = :manager_id 
    AND i.status = 'Выставлен'
    AND i.date >= NOW() - INTERVAL '1 week'
ORDER BY date DESC 
```

Получение всех счетов по контрагенту:
```sql
SELECT * 
FROM invoices 
WHERE client_id = :client_id
```

Получение счета по номеру:
Так как нумерация может обновляться нужно искать счета по номеру и дате/менеджеру
```sql
SELECT * 
FROM invoices 
WHERE invoice_number = :invoice_number 
    AND manager_id = :manager_id
    AND date = :date;
```

Получение всей информации по конкретному счету:
```sql
SELECT i.*, c.*, m.*
FROM invoices i
JOIN clients c ON c.id = i.client_id
JOIN managers m ON m.id = i.manager_id
WHERE i.id = :invoice_id
```
