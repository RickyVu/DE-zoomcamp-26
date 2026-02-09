# Module 3 Homework: Data Warehousing & BigQuery

In this homework we'll practice working with BigQuery and Google Cloud Storage.

When submitting your homework, you will also need to include
a link to your GitHub repository or other public code-hosting
site.

This repository should contain the code for solving the homework.

When your solution has SQL or shell commands and not code
(e.g. python files) file format, include them directly in
the README file of your repository.

## Data

For this homework we will be using the Yellow Taxi Trip Records for January 2024 - June 2024 (not the entire year of data).

Parquet Files are available from the New York City Taxi Data found here:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

## Loading the data

You can use the following scripts to load the data into your GCS bucket:

- Python script: [load_yellow_taxi_data.py](./load_yellow_taxi_data.py)

You will need to generate a Service Account with GCS Admin privileges or be authenticated with the Google SDK, and update the bucket name in the script.

If you are using orchestration tools such as Kestra, Mage, Airflow, or Prefect, do not load the data into BigQuery using the orchestrator.

Make sure that all 6 files show in your GCS bucket before beginning.

Note: You will need to use the PARQUET option when creating an external table.


## BigQuery Setup

Create an external table using the Yellow Taxi Trip Records. 

Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table). 

Create external table pointing to GCS bucket
```
CREATE OR REPLACE EXTERNAL TABLE `nyc_taxi_data.external_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://<GCS_BUCKET_NAME>/yellow_tripdata_2024-*.parquet']
);
```

Create regular table from external table
```
CREATE OR REPLACE TABLE `nyc_taxi_data.yellow_tripdata_2024` AS
SELECT * FROM `nyc_taxi_data.external_yellow_tripdata_2024`;
```

---

## Question 1. Counting records

What is count of records for the 2024 Yellow Taxi Data?

### Solution
```sql
SELECT COUNT(*) as total_records
FROM `<GOOGLE_CLOUD_PROJECT>.nyc_taxi_data.yellow_tripdata_2024`;
```
```
20332093
```

---

## Question 2. Data read estimation

Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
 
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

### Solution
```
SELECT COUNT(DISTINCT PULocationID) as distinct_pulocations_external
FROM `<GOOGLE_CLOUD_PROJECT>.nyc_taxi_data.external_yellow_tripdata_2024`;
```
```
This query will process 0 B when run.
```

```
SELECT COUNT(DISTINCT PULocationID) as distinct_pulocations_regular
FROM `<GOOGLE_CLOUD_PROJECT>.nyc_taxi_data.yellow_tripdata_2024`;
```
```
This query will process 155.12 MB when run.
```
in job information:
```
Bytes processed
155.12 MB
Bytes billed
156 MB
```

---

## Question 3. Understanding columnar storage

Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table.

Why are the estimated number of Bytes different?

### Solution
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires 
reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

---

## Question 4. Counting zero fare trips

How many records have a fare_amount of 0?

### Solution
```
SELECT COUNT(*)
FROM `<GOOGLE_CLOUD_PROJECT>.nyc_taxi_data.yellow_tripdata_2024`
WHERE fare_amount=0;
```
```
8333
```
---

## Question 5. Partitioning and clustering

What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

### Solution
- Partition by tpep_dropoff_datetime and Cluster on VendorID

---

Question 6. Partition benefits

Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime
2024-03-01 and 2024-03-15 (inclusive)


Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? 


Choose the answer which most closely matches.
### Solution
Create the optimized table
```
CREATE OR REPLACE TABLE `<GOOGLE_CLOUD_PROJECT>.nyc_taxi_data.yellow_tripdata_2024_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `<GOOGLE_CLOUD_PROJECT>.nyc_taxi_data.yellow_tripdata_2024`;
```

unoptimized query
```
SELECT DISTINCT VendorID
FROM `<GOOGLE_CLOUD_PROJECT>.nyc_taxi_data.yellow_tripdata_2024`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
ORDER BY VendorID;
```
```
Bytes processed
310.24 MB
Bytes billed
311 MB
```

optimized query
```
SELECT DISTINCT VendorID
FROM `<GOOGLE_CLOUD_PROJECT>.nyc_taxi_data.yellow_tripdata_2024_optimized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
ORDER BY VendorID;
```

```
Bytes processed
26.84 MB
Bytes billed
27 MB
```
Answer: `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`

---

## Question 7. External table storage

Where is the data stored in the External Table you created?

### Solution
- GCP Bucket

---

## Question 8. Clustering best practices

It is best practice in Big Query to always cluster your data:

### Solution
- False

---

## Question 9. Understanding table scans

No Points: Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

### Solution
```
SELECT COUNT(*) as total_records
FROM `<GOOGLE_CLOUD_PROJECT>.nyc_taxi_data.yellow_tripdata_2024`;
```
```
This query will process 0 B when run.
If it detect COUNT(*), it can automatically retrieve this information from stored metadata.
```