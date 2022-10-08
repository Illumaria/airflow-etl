ARG AIRFLOW_BASE_IMAGE="apache/airflow:2.4.1-python3.10"
FROM ${AIRFLOW_BASE_IMAGE}

USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
