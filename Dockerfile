FROM apache/airflow:2.11.0

USER root

# Установка вспомогательных утилит через apt (wget, curl)
RUN apt-get update && \
    apt-get install -y wget curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка Java 11 (Temurin) из официального релиза
RUN wget -q https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.24%2B8/OpenJDK11U-jdk_x64_linux_hotspot_11.0.24_8.tar.gz && \
    tar -xzf OpenJDK11U-jdk_x64_linux_hotspot_11.0.24_8.tar.gz -C /opt/ && \
    mv /opt/jdk-11.0.24+8 /opt/java11 && \
    rm OpenJDK11U-jdk_x64_linux_hotspot_11.0.24_8.tar.gz

# Скачивание Spark 3.5.1 (совместимость с Bitnami)
RUN wget -q https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz && \
    tar -xzf spark-3.5.1-bin-hadoop3.tgz -C /opt/ && \
    mv /opt/spark-3.5.1-bin-hadoop3 /opt/spark && \
    rm spark-3.5.1-bin-hadoop3.tgz

# Установка Python-пакетов
RUN python -m pip install --no-cache-dir \
    apache-airflow-providers-trino==6.6.0 \
    apache-airflow-providers-apache-spark==4.11.0 \
    pyspark==3.5.1 \
    apache-airflow-providers-docker==3.10.0

# Переменные окружения
ENV JAVA_HOME=/opt/java11
ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${JAVA_HOME}/bin:${PATH}"

USER airflow