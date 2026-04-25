# Простой DataLake: Trino + S3 Minio + Spark + Iceberg
[Исходное видео](https://www.youtube.com/watch?v=-fAwvsbSZh0 "Туториал по Data Lake") \
[Оригинальный репозиторий](https://github.com/k0rsakov/pet_project_trino_data_lake)


## Сервисы
### minio & minio-setup
Сервисы локального S3 - minio.

### postgres-iceberg
База данных PostgreSQL для Iceberg.

### rest
WEB-UI Iceberg.

### trino
Сервис trino.

### spark-iceberg
Сервис Spark-Iceberg.

### postgres-dwh
База данных для хранения бизнес-информации.

## О проекте
### Поднятие инфраструктуры
Для запуска инфраструктуры:
```bash
docker compose up -d
```
Для перезапуска инфраструктуры, если что-то пошло не так:
```bash
docker-compose down && docker-compose build && docker-compose up -d 
```
Для перезапуска trino чтобы добавить новые коннекты или изменить существующие:
```bash
docker-compose up -d --force-recreate trino
```

### Подключение к Minio
Параметры подключения стандартные:
* `login`: `minioadmin`
* `password`: `minioadmin`

### Подключение к Trino
Проверка работоспобности Trino:
```bash
docker exec -it trino trino --server localhost:8080 --user test 
```