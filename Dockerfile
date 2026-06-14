FROM apache/airflow:2.11.0

USER root

# Создаём директорию для apt (исправление ошибки сборки)
RUN mkdir -p /var/lib/apt/lists/partial && \
    apt-get update && \
    apt-get install -y wget openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Скачиваем и распаковываем Spark 3.5.5
RUN wget -q https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz && \
    tar -xzf spark-3.5.5-bin-hadoop3.tgz -C /opt/ && \
    mv /opt/spark-3.5.5-bin-hadoop3 /opt/spark && \
    rm spark-3.5.5-bin-hadoop3.tgz

# Устанавливаем Python-пакеты (обход ограничений Airflow)
RUN python -m pip install --no-cache-dir \
    apache-airflow-providers-trino==6.6.0 \
    apache-airflow-providers-apache-spark==4.11.0 \
    pyspark==3.5.5 \
    apache-airflow-providers-docker==3.10.0

# Переменные окружения
ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${SPARK_HOME}/bin:${PATH}"

USER airflow