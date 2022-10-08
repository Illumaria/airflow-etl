ARG POSTGRES_BASE_IMAGE="postgres:13"
FROM ${POSTGRES_BASE_IMAGE}

ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres_db

COPY database_schema.sql /docker-entrypoint-initdb.d/database_schema.sql
