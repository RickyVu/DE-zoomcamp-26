
1
```
stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned

When running dbt run --select int_trips_unioned, dbt builds:

First, all upstream dependencies (stg_green_tripdata and stg_yellow_tripdata)

Then, the selected model itself (int_trips_unioned)

This is because dbt needs to ensure that all dependencies are built before building the selected model. The --select flag with a model name includes that model and all its parents (upstream dependencies), but not its children (downstream dependencies).
```

2
```
dbt will fail the test, returning a non-zero exit code

The accepted_values test is a generic test that validates that all values in the payment_type column are from the specified list [1, 2, 3, 4, 5]. When a new value (6) appears in the source data, the test will fail because it finds a value that's not in the accepted list. This will result in a non-zero exit code, which is typically used to indicate test failure in CI/CD pipelines and build processes.
```

3
```
python -c "
import duckdb
conn = duckdb.connect('taxi_rides_ny.duckdb')
count = conn.execute('SELECT COUNT(*) FROM prod.fct_monthly_zone_revenue').fetchone()[0]
print(f'Count in fct_monthly_zone_revenue: {count}')
conn.close()
"
```

```
Count in fct_monthly_zone_revenue: 12184
```

4
```
python -c "
import duckdb
conn = duckdb.connect('taxi_rides_ny.duckdb')

# Query for green taxi zones with highest total revenue in 2020
query = '''
SELECT 
    pickup_zone,
    SUM(revenue_monthly_total_amount) as total_revenue
FROM prod.fct_monthly_zone_revenue
WHERE service_type = 'Green'
    AND revenue_month >= '2020-01-01'
    AND revenue_month < '2021-01-01'
    AND pickup_zone IS NOT NULL
GROUP BY pickup_zone
ORDER BY total_revenue DESC
LIMIT 5;
'''

results = conn.execute(query).fetchall()
print('Top 5 pickup zones for Green taxis in 2020:')
for i, (zone, revenue) in enumerate(results, 1):
    print(f'{i}. {zone} - ${revenue:,.2f}')

conn.close()
"
```
```
Top 5 pickup zones for Green taxis in 2020:
1. East Harlem North - 
2. East Harlem South - 
3. Central Harlem - 
4. Washington Heights South - 
5. Morningside Heights -
```

5
```
python -c "
import duckdb
conn = duckdb.connect('taxi_rides_ny.duckdb')

# Query for Green taxi trips in October 2019
query = '''
SELECT 
    SUM(total_monthly_trips) as total_trips
FROM prod.fct_monthly_zone_revenue
WHERE service_type = 'Green'
    AND revenue_month = '2019-10-01'
    AND pickup_zone IS NOT NULL
GROUP BY service_type;
'''

result = conn.execute(query).fetchone()
total_trips = result[0] if result[0] else 0
print(f'Total Green taxi trips in October 2019: {total_trips:,}')

conn.close()
"
```
```
Total Green taxi trips in October 2019: 384,624
```



## 6
Create `load_fhv_data.py`

Run `move_to_prod.py`

Create staging model `models/staging/stg_fhv_tripdata.sql`
```
{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
    where dispatching_base_num is not null
)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as tripid,
    dispatching_base_num,
    Affiliated_base_number as affiliated_base_number,
    
    -- timestamps
    pickup_datetime,
    dropOff_datetime as dropoff_datetime,
    
    -- locations
    PUlocationID as pickup_location_id,
    DOlocationID as dropoff_location_id,
    
    -- SR_Flag
    SR_Flag as sr_flag
    
from source
where extract(year from pickup_datetime) = 2019
```

Add FHV to the existing `models/staging/sources.yml`
```
      - name: fhv_tripdata
        description: Raw FHV (For-Hire Vehicle) trip records for 2019
        loaded_at_field: pickup_datetime
        columns:
          - name: dispatching_base_num
            description: Unique identifier for the base dispatching the vehicle
          - name: pickup_datetime
            description: Date and time when the trip started
          - name: dropOff_datetime
            description: Date and time when the trip ended
          - name: PUlocationID
            description: TLC Taxi Zone where the trip started
          - name: DOlocationID
            description: TLC Taxi Zone where the trip ended
          - name: SR_Flag
            description: Shared Ride Flag
          - name: Affiliated_base_number
            description: Base number affiliated with the dispatch
```

Run dbt model
```
dbt run --select stg_fhv_tripdata --target prod
```

Query
```
python -c "
import duckdb
conn = duckdb.connect('taxi_rides_ny.duckdb')
count = conn.execute('SELECT COUNT(*) FROM prod.stg_fhv_tripdata').fetchone()[0]
print(f'\\nRecords in stg_fhv_tripdata: {count:,}')
conn.close()
"
```

```
Records in stg_fhv_tripdata: 43,244,693
```
