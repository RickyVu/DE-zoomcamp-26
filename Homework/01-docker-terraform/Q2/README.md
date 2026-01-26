## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```



## Prepare the Data

Download the green taxi trips data for November 2025:

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
```

You will also need the dataset with zones:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

### Solution
Save the provided docker compose code into docker-compose.yml
```bash
docker compose up -d
```
Use browser to access: http://localhost:8080/

Login to pgadmin, then connect to database according to docker compose file

hostname:port combination is `postgres:5432`

Data Ingestion
1. Write ingest_data.py
2. Setup a pyproject.toml with required libraries
3. Setup a Dockerfile with python, uv, and copies pyproject.toml. Set entrypoint to ingest_data.py

```bash
docker build -t taxi_ingest:v002 .

docker run -it --rm --network=q2_default taxi_ingest:v002 ingest-all --pg-user=postgres --pg-pass=postgres --pg-host=postgres --pg-port=5432 --pg-db=ny_taxi
```