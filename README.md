# de-datalake
S3 + Iceberg + Trino + PySpark + PostgreSQL + Greenplum + Clickhouse + Kafka

## Создание виртуального окружения

```bash
python3.12 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install poetry && \
poetry lock && \
poetry install
```

### Добавление новых зависимостей в окружение

```bash
poetry lock && \
poetry install
```

### Добавление зависимости в pyproject.toml

```bash
poetry add <package_name>=<version>
```

## Разворачивание инфраструктуры

```bash
docker-compose up -d
```