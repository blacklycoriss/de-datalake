### Инструменты:
#### 1. S3
#### 2. Apache Iceberg
#### 3. Trino
#### 4. Apache Spark (PySpark)
#### 5. PostgreSQL
#### 6. Greenplum
#### 7. Clickhouse
#### 8. Apache Kafka

# НАСТРОЙКИ ПРОЕКТА ПЕРЕД РАБОТОЙ


## ШАГИ ПО РАЗВЕРТЫВАНИЮ ОКРУЖЕНИЯ

### 1. Установка WSL2 (Windows Subsystem for Linux 2)

Инструкция по установке:
https://habr.com/ru/articles/956330/

**Примечание: при установке используй VPN**

### 2. Установка Docker Desktop для Windows

Инструкция по установке:
https://docs.docker.com/desktop/setup/install/windows-install/

### 3. Установка VS Code и Git

Ссылка для скачивания VS Code:
https://code.visualstudio.com/download?_exp_download=d53503e735

После открытия VS Code создай папку в любом удобном месте и через "Open Folder" или File -> Open Folder выбери созданную папку для твоего проекта.

Ссылка для скачивания Git (тебе нужен Standalone Installer):
https://git-scm.com/install/windows

После установки Git зарегистрируйся на GitHub:
https://github.com/

После регистрации на GitHub создай токен и сохрани в надежное место - он тебе пригодится в будущем.
Ссылка на гайд: 
https://netology-code.github.io/guides/github-access-token/

### 4. Клонирование текущего репозитория

Выполни следующую команду в терминале VS Code (Ctrl + `):
```bash
git clone https://github.com/blacklycoriss/de-datalake
```
### 5. Установка Python

Ссылка на установку (используй Python 3.12+):
https://www.python.org/ftp/python/pymanager/python-manager-26.3.msix

### 6. Создание виртуального окружения

Выполни в терминале либо последовательно (без ```&& \``` в конце строк), либо разом следующие инструкции:

```bash
python3 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install poetry && \
poetry lock && \
poetry install
```

### 7. Добавление новых зависимостей в окружение

Выполни в терминале либо последовательно (без ```&& \``` в конце строк), либо разом следующие инструкции:

```bash
poetry lock && \
poetry install
```

### 8. Добавление зависимости в pyproject.toml

```bash
poetry add <package_name>=<version>
```

### 9. Разворачивание инфраструктуры

Перед выполнением убедись, что Docker Desktop у тебя запущен, иначе появится ошибка.
```bash
docker-compose up -d
```

## ПОДКЛЮЧЕНИЕ К СЕРВИСАМ

### 1. Скачать Dbeaver

Ссылка на скачивание:
https://dbeaver.io/download/

### 2. Создать подключение

После открытия Dbeaver:

#### 1. Нажать на иконку "New Connection" (под вкладкой "File")

#### 2. Выбрать нужный сервис (PostgreSQL, Clickhouse и тд)

Для каждого сервиса подключение настраивается отдельно

#### 3. Прописать нужные данные (адрес, порт, название БД/схемы, логин и пароль (при наличии))

Все данные для подключения ты можешь посмотреть в файле docker-compose.yaml в конфигурациях сервисов

#### 4. Нажать на "Test Connection"

При необходимости установи всё, что предлагает Dbeaver

## ПОДКЛЮЧЕНИЕ К DWH

Чтобы подключиться к DWH, необходимо создать несколько подключений в Dbeaver'е:

#### 1. Подключение к Airflow БД
#### 2. Подключение к OLTP БД
#### 3. Подключение к Clickhouse БД

# Описание проекта

## Архитектура каталогов

В полной имплементации проекта существуют следующие папки:

### 1. airflow - директория Apache Airflow
#### 1.1. config - пользовательские конфиг файлы
#### 1.2. dags - DAG'и для исполнения
#### 1.3. logs - хранение логов выполнения задач (Task Instances) и логов самого веб-сервера/воркеров
##### 1.3.1. logs/scheduler/ — логи планировщика
##### 1.3.2. logs/webserver/ — логи веб-интерфейса
##### 1.3.3. logs/dag_id={dag_id}/task_id={task_id}/{execution_date}.log — конкретные логи выполнения каждого таска
#### 1.4. plugins - кастомные расширения, которые не входят в базовый дистрибутив Airflow


### 2. Каталоги с данными сервисов
#### Данные каталоги находятся в .gitignore, поэтому отсутствуют в репозитории, создаются при разворачивании контейнеров.
##### 2.1. clickhouse-data - данные Clickhouse
##### 2.2. data - данные S3
##### 2.3. greenplum-data - данные Greenplum
##### 2.4. kafka-data - данные Apache Kafka
##### 2.5. postgres-oltp-data - данные PostgreSQL (OLTP)


### 3. Каталоги Trino (trino/etc)
#### 3.1. catalog - данные о подключениях к сервисам
##### 3.1.1. clickhouse.properties - подключение к Clickhouse
##### 3.1.2. greenplum.properties - подключение к Greenplum
##### 3.1.3. iceberg.properties - подключение к Apache Iceberg
##### 3.1.4. kafka.properties - подключение к Apache Kafka
##### 3.1.5. oltp.properties - подключение к PostgreSQL (OLTP)
#### 3.2. config.properties - конфиг файл сервера Trino
#### 3.3. jvm.config - настройка JVM, в которой работает Trino
#### 3.4. node.properties - настройки для текущего узла в кластере (здесь кластера нет, но файл все равно нужен)

### 4. Каталог utils - здесь хранятся кастомные утилиты для работы с сервисами (пока что только для S3)