-- 0 

-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `causal-bison-448415-h1.zoomcamp.hw_yellow_trip_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_hw3_2025_aur_3913992/yellow_tripdata_2024-*.parquet']
);

-- Creatin a table
CREATE OR REPLACE TABLE causal-bison-448415-h1.zoomcamp.hw_table_yellow_2024
AS(
  SELECT * FROM `causal-bison-448415-h1.zoomcamp.hw_yellow_trip_2024`
)

-- Helper
SELECT * FROM `causal-bison-448415-h1.zoomcamp.hw_yellow_trip_2024` LIMIT 1;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE causal-bison-448415-h1.zoomcamp.hw_yellow_trip_2024_partitioned
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM causal-bison-448415-h1.zoomcamp.hw_yellow_trip_2024
;

-- Q1
SELECT COUNT(1)
FROM causal-bison-448415-h1.zoomcamp.hw_yellow_trip_2024_partitioned;

-- Q2
SELECT COUNT(DISTINCT(PULocationID)) FROM causal-bison-448415-h1.zoomcamp.hw_yellow_trip_2024;
SELECT COUNT(DISTINCT(PULocationID)) FROM causal-bison-448415-h1.zoomcamp.hw_table_yellow_2024;

-- Q3 Theorical
-- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

-- Q4
SELECT COUNT(1)
FROM causal-bison-448415-h1.zoomcamp.hw_yellow_trip_2024_partitioned
WHERE fare_amount = 0;

-- Q5
-- Partition by tpep_dropoff_datetime and Cluster on VendorID
CREATE OR REPLACE TABLE causal-bison-448415-h1.zoomcamp.partitioned_trip_yellow_2024
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS(
  SELECT * FROM `causal-bison-448415-h1.zoomcamp.hw_table_yellow_2024`
);

-- Q6 

-- 26.84 MB
SELECT DISTINCT(VendorID)
FROM causal-bison-448415-h1.zoomcamp.partitioned_trip_yellow_2024
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15'
;

-- 310.24 MB
SELECT DISTINCT(VendorID)
FROM causal-bison-448415-h1.zoomcamp.hw_table_yellow_2024
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15'
;

-- Q7 GCP Bucket

-- Q8 False