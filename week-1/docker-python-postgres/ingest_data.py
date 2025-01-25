from time import time
import argparse
import urllib.request
from sqlalchemy import create_engine
import pandas as pd

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    print('Start to download')
    urllib.request.urlretrieve(url, csv_name)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv('yellow_tripdata_2021-01.csv.gz', iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()
            print('inserted another chunk, took %.3f second' % (t_end-t_start))
        except StopIteration:
            print('Finished ingesting data into the postgres database')
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user
    # passwordd
    # host
    # port
    # database nae
    # table
    # url of the csv

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()
    main(args)


"""
SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pick_up_loc",
	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "dropoff_loc"
FROM
	yellow_taxi_trips t,
	zones zpu,
	zones zdo
WHERE 
	t."PULocationID" = zpu."LocationID" AND
	t."DOLocationID" = zdo."LocationID"
LIMIT 100;


SELECT
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	COUNT(1)
FROM
	yellow_taxi_trips t
GROUP BY 
	CAST(tpep_dropoff_datetime AS DATE)
ORDER BY 
	"day" ASC;

SELECT
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	"DOLocationID",
	COUNT(1) as "count",
	MAX(total_amount),
	MAX(passenger_count)
FROM
	yellow_taxi_trips t
GROUP BY 
	1,2
ORDER BY 
	"day" ASC,
	"DOLocationID" ASC;

python ingest_data.py
--user=root
--password=root
--host=localhost
--port=5432
--db=ny_taxi
--table_name=yellow_taxi_trips
--url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz

"""