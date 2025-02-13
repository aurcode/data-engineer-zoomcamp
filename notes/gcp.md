### Login
```
gcloud auth activate-service-account --key-file=<key.json>
gcloud config set project "<project-name>"
```

### gsutil (Bucket from GCP)

- Multi-region - Dual region - Single region
- Classes: Standard (often) - Nearline (month) - Coldline (3 months) - Archive (year)
- Access control: **Public access** and **uniform / Fine-grained** (specified)
- Retention policy

Create a bucket
```
gsutil mb gs://<bucket-name>
```

See my buckets
```
gsutil ls
```

See my files
```
gsutil ls gs://<bucket-name>
```

Copy
```
gsutil cp gsutil cp ./<file> gs://<bucket-name>
gsutil cp gs://<bucket-name>/<file> . 
```

Active history for files
```
gsutil versioning set on gs://<bucket-name>
```

Delete file
```
gsutil rm gs://<bucket-name>/<file>
```

### Cloud Bigtable - NoSQL serverless

create BigTable instance
```
cbt createinstance quick-start-instance "quick-start-instance" quickstart-instance-c1 us-east1-c 1 SSD
```

Set for bash 
```
echo project = `gcloud config get-value project` > ~/.cbtrc
echo instance = quick-start-instance >> ~/.cbtrc
```

create table
```
create table my-table
cbt ls
```

Create column family
```
cbt createfamily my-table my-family
cbt ls my-table
```

```

```

### BigQuery (BQ) - SQL serverless

- https://cloud.google.com/sdk/gcloud/reference/alpha/bq/datasets
- https://cloud.google.com/bigquery/docs/locations
```
  gcloud alpha bq datasets config export
  gcloud alpha bq datasets create
  gcloud alpha bq datasets delete
  gcloud alpha bq datasets describe
  gcloud alpha bq datasets list
  gcloud alpha bq datasets update
  gcloud alpha bq jobs cancel
  gcloud alpha bq jobs config export
  gcloud alpha bq jobs describe
  gcloud alpha bq jobs list
```