# Airflow ETL with Postgres DB connection

## Prerequisites

* Python >= 3.10
* pip >= 22.2.2
* docker
* [docker-compose](https://docs.docker.com/compose/install/) >= 2.10.2

## Installation

```bash
git clone https://github.com/Illumaria/airflow-etl.git
cd airflow-etl
```

## Usage

1. Get `API_KEY` and `API_SECRET` for https://live-score-api.com/.
2. Either set them as environment variables:

```bash
export API_KEY=<your_api_key>
export API_SECRET=<your_api_secret>
```

or put them in a `.env` file.

3. Depending on the method selected in the previous step, run one of the following commands.

```bash
docker-compose up --build
```
or

```bash
docker-compose --env-file <path_to_.env_file> up --build
```

In those cases when docker only runs with `sudo`, don't forget that `sudo` has its own environment variables, so you need to add the following to the commands above:

```bash
sudo -E docker-compose ...
```
4. Once all the services are up and running, go to [`https://localhost:8080`](https://localhost:8080) (use `airflow` for both username and password), then to `Admin` -> `Connections` -> `Add a new record`, and specify the following values to establish connection with the external Postgres DB:
    * Connection id: `postgres_db`
    * Type: `Postgres`
    * Schema: `postgres_db`
    * Host: `postgres-db`
    * Port: `5432`
    * User: `postgres`
    * Password: `postgres`
