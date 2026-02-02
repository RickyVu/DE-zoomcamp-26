

5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

```sql
SELECT COUNT(*) 
FROM yellow_tripdata 
WHERE filename = 'yellow_tripdata_2021-03.csv';
```

```
count
1925152
```