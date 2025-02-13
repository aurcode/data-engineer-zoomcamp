## Login
```
gcloud auth activate-service-account --key-file=<key.json>
gcloud config set project "<project-name>"
gcloud services list --enabled
```

## Storaged in GCP

| Product           | Simple Description                                     | Good For                                                                  | Bad For                                                                         | Examples and Scale                                       |
|--------------------|--------------------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------------|---------------------------------------------------------|
| Cloud Firestore    | Scalable storage for structured servers.               | Google App Engine applications                                            | Relational or analytical data.                                                  | User profiles or product catalogs. TB                   |
| Cloud Bigtable     | Large volume, low latency database.                    | "Flat" data, heavy read/write, or analytical data.                         | Transactional or highly structured data.                                       | Ad data, financial data, or IoT data. PB               |
| Google Cloud Storage | Binary/object storage (files).                          | Large unstructured data or data accessed infrequently.                     | Structured data, creating fast applications.                                      | Images, disk backups, and file transmissions. PB          |
| Cloud Spanner      | Global, consistent, and innovative RDBMS.               | Serving large amounts of data and consistent data worldwide.             | Small applications and analytical data.                                         | Ad publishing, global inventory, global applications. PB  |
| Cloud SQL          | Easy-to-understand RDBMS based on virtual machines.    | Web frameworks and existing applications.                                 | Scaling, analysis, heavy writes.                                                | User credentials, transactions. TB                    |
| BigQuery | Fully-managed, serverless data warehouse. | Business intelligence, data analytics, and large datasets. | Real-time transactions, frequently updated data, very small datasets. | Analyzing website traffic, customer behavior, and market trends. PB |

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
cbt set my-table my-row-key my-family:my-column=my-cell
```

read table
```
cbt read my-table
```

### Cloud SQL & Cloud Spanner

- CSQL: Serverless service close to MySQL, PostgreSQL and SQL Server
- CSpanner: Around world (Global but more expensive)

Create a instance for Spanner
```
gcloud spanner instances create example-db --config=regional-us-central1 --nodes=1
```

Create a db inside the instance
```
gcloud spanner databases create example-db-db --instance=example-db
```

Create schema | Write ddl
```
gcloud spanner databases ddl update example-db-db
        --instance=example-db
        --ddl='CREATE TABLE Singers ( 
				SingerId INT64 NOT NULL, 
				FirstName STRING(1024), 
				LastName STRING(1024), 
				SingerInfo BYTES(MAX) 
				) PRIMARY KEY (SingerId)'
```

Insert Data
```
gcloud spanner rows insert 
        --database=example-db-db
        --instance=example-db
        --table=Singers
        --data=
                SingerId=1,
                FirstName=Marc,
                LastName=Richards
```

Update Data
```
gcloud spanner rows update
        --table=Singers
        --database=example-db-db
        --instance=example-db
        --data=SingerId=1,SingerName=Will
```

Delete Data
```
gcloud spanner rows delete 
        --table=Singers
        --database=example-db-db
        --instance=example-db
        --keys=1
```

Read data
```
gcloud spanner databases execute-sql example-db-db
    --instance=example-db
    --sql='SELECT * FROM Singers'
```

### Cloud Firestore
- Serverless NoSQL Database based in documents
- btw can work without network

```
gcloud firestore databases create --region=<region-name>	
```

### alpha BQ (alpha BigQuery)

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

```
gcloud alpha bq datasets list --project=<project-name> --all

gcloud alpha bq datasets create <bq-dataset-name>
        --description="<description>"
        --overwrite
        --project=<project-name>

gcloud alpha bq datasets describe <bq-dataset-name> --project=<project-name>
```

### BigQuery (BQ) - SQL serverless

Information BQ
```
bq ls

bq ls <dataset-name>

bq show <project-name>:<dataset-name>
```

Create dataset
```
bq mk --location=<region-name> --dataset <project-name>:<dataset-name>
```

Create table inside dataset
```
bq mk -t <project-name>:<dataset-name>.<table-name> <id:integer,name:string>
```

```
bq query --project_id=<project-name> --use_legacy_sql=false 'SELECT table_catalog, table_schema, table_name, table_type, is_insertable_into, creation_time, ddl from <table-name>.INFORMATION_SCHEMA.TABLES;'

bq query --project_id=<project-name> --use_legacy_sql=false 'SELECT * from <x>;'
```
Show innformation pretty way
```
bq show --format=pretty <project-name>:<dataset-name>.<table-name>

bq show --format=prettyjson <project-name>:<dataset-name>.<table-name>

bq show --format=prettyjson <project-name>:<dataset-name>
```

Delete table
```
!bq rm <project-name>:<dataset-name>.<table-name>

bq rm -r
```

<details>
<summary>Extra Commands for BQ</summary>

- https://cloud.google.com/bigquery/docs/tables#sql
- https://cloud.google.com/bigquery/docs/reference/bq-cli-reference#bq_mk
- https://cloud.google.com/bigquery/docs/information-schema-tables
- https://cloud.google.com/bigquery/docs/listing-datasets

1. **Show datasets in a project**:
```bash
bq ls
```

2. **Show tables in a dataset**:
```bash
bq ls dataset_id
```

3. **Show schema of a table**:
```bash
bq show project_id:dataset_id.table_id
```

4. **Load data into a table**:
```bash
bq load --source_format=FORMAT dataset_id.table_id path_to_source
```

5. **Export data from a table**:
```bash
bq extract dataset_id.table_id gs://path_to_destination
```

6. **Run a query**:
```bash
bq query --use_legacy_sql=false 'SELECT * FROM dataset_id.table_id'
```

7. **Show query results in the console**:
```bash
bq query --n=5 'SELECT * FROM dataset_id.table_id'
```

8. **Copy a table**:
```bash
bq cp project_id:dataset_id.table_id project_id:dataset_id.new_table_id
```

9. **Delete a table**:
```bash
bq rm project_id:dataset_id.table_id
```

10. **Delete a dataset**:
```bash
bq rm -r dataset_id
```


</details>


## Compute Enine

### VPC Network

**Red in VPC:**

|Kind||||
|---|---|---|---|
| Default | Presente en cada proyecto | Una subred por región | Reglas de firewall por defecto |
| Auto Mode | Red por defecto | Una subred por región | Subred /20 expandible a /16 |
| Custom Mode | No se crean subredes por defecto | Control total del rango de IPs | Subred expandible a cualquier tamaño RFC 1918 |


**Capacidades importantes de las VPC**
| Global | Expandible | Access Privado | Compatible |
|---|---|---|---|
| Conectividad multi-región privada | Adaptable a las necesidades | Cloud Storage y otras APIs | Administración de red centralizada |
| Utiliza la red global de Google | Crece sin problemas | IPs públicas y acceso a Internet opcionales | VPN compartida. IAM granular |

Create network
```
gcloud compute networks create <name>
    --subnet-mode=<mode> 
    --bgp-routing-mode=<type> 
    --mtu=<number-mtu>
```

Create subnetwork
```
gcloud compute networks subnets create <name-subnet>
    --network=<name-vpc> 
    --range=<ip-range> 
    --region=<region-name>
```

```
gcloud compute firewall-rules create <rule-name> --network <network-name> --allow tcp:<port>

gcloud compute firewall-rules delete <rule-name> --network <network-name>

gcloud compute firewall-rules list
```

- Rules Network by Default are all trafit to internet is allow, but all trafit from internet is deny

- Cloud nat for create fake public ip for our machines

### Virtual machine

- Preemptible VMs onna be up only 24 hours but is cheaper, perfect for haboop or similars

| **Instance Type** | **Optimization Focus**     | **Description**                         |
|-------------------|----------------------------|-----------------------------------------|
| **Efficient E2**  | Cost optimization          | Prioritizes cost savings               |
| **Balanced N2, N2D** | Balanced performance       | Focused on performance and TCO (Total Cost of Ownership) |
| **TAU T2D**       | Scalability optimization   | Optimized for high scalability and performance |
| **C2**            | Compute optimization       | Best CPU performance                   |
| **M1, M2**        | Memory optimization        | Higher memory capacity                 |
| **A2**            | Acceleration optimization  | Optimized for high-performance GPUs    |

```
gcloud compute ssh <instance-name>  --zone <zona> --tunnel-through-iap
gcloud compute scp 
```
- 35.235.240.0/20

```
gcloud compute scp <path> <instance-name>:<path> --zone=<zone>
```

### idk

```gcloud builds submit --tag gcr.io/project_id/webapp:0.0.1```

## Kubernetes (K8s) in GCP

```
gcloud beta container --project <project-name> clusters get-credentials '<cluster-name>' --zone=<zone>
```