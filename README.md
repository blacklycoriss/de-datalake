# de-datalake
S3 + Iceberg + Trino + PySpark + PostgreSQL + Greenplum + Clickhouse + Kafka

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