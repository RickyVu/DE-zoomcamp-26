## Question 1. Understanding Docker images
Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

What's the version of pip in the image?

### Solution
Check this: https://hub.docker.com/_/python

```bash
docker pull python:3.13
docker run -it python:3.13 /bin/bash
```

Run in docker container:
```bash
root@f350eba61f8f:/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

---

## Question 2. Understanding Docker networking and docker-compose
### Solution
[Check here](./Q2/README.md)

## Question 3. Counting short trips
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

### Solution
```sql
SELECT COUNT(*) as trips_under_1_mile
FROM 
    green_taxi_trips
WHERE 
    lpep_pickup_datetime >= '2025-11-01' 
    AND lpep_pickup_datetime < '2025-12-01'
    AND trip_distance <= 1.0;
```

```
"trips_under_1_mile"
8007
```

---

## Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

### Solution

```sql
SELECT DATE(lpep_pickup_datetime) as pickup_day, MAX(trip_distance) as longest_trip_that_day
FROM green_taxi_trips 
WHERE trip_distance < 100 
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY longest_trip_that_day DESC 
LIMIT 1;
```

```
"pickup_day" "longest_trip_that_day"
"2025-11-14" 88.03
```

---

## Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

### Solution
```sql
SELECT zones."Zone" as pickup_zone,SUM(trips.total_amount) as total_amount_sum
FROM 
    green_taxi_trips trips
INNER JOIN 
    taxi_zone_lookup zones
    ON trips."PULocationID" = zones."LocationID"
WHERE 
    DATE(trips.lpep_pickup_datetime) = '2025-11-18'
GROUP BY 
    zones."Zone"
ORDER BY 
    total_amount_sum DESC
LIMIT 1;
```

```
"pickup_zone"	"total_amount_sum"
"East Harlem North"	9281.920000000004
```

---

## Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's tip , not trip. We need the name of the zone, not the ID.

### Solution

```sql
SELECT 
    do_zone."Zone" as dropoff_zone,
	max(tip_amount) as max_tip
FROM 
    green_taxi_trips trips
LEFT JOIN 
    taxi_zone_lookup pu_zone ON trips."PULocationID" = pu_zone."LocationID"
LEFT JOIN 
    taxi_zone_lookup do_zone ON trips."DOLocationID" = do_zone."LocationID"
WHERE pu_zone."Zone" = 'East Harlem North'
GROUP BY do_zone."Zone"
ORDER BY max_tip DESC
LIMIT 1

```

```
"dropoff_zone"	"max_tip"
"Yorkville West"	81.89
```

---

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.

[Check Here](./terraform_test/)

### Solution
```bash
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init
```

I first made a terraform.tfvars with this in it:
```
project           = "<PROJECT_ID>"
```

```bash
# Check changes to new infra plan
terraform plan
# Alternatively do: terraform plan -var="project=<PROJECT_ID"

# Create new infra
terraform apply
```

```bash
# Delete infra after work, to avoid costs on any running services
terraform destroy
```

---

## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform

### Solution
`terraform init, terraform apply -auto-approve, terraform destroy`