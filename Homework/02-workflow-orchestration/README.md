For the homework, we'll be working with the green taxi dataset located here:

https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download

To get a wget-able link, use this prefix (note that the link itself gives 404):

https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/

## Question 1
Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e. the output file yellow_tripdata_2020-12.csv of the extract task)?

### Solution
```bash
wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-12.csv.gz | gunzip > yellow_tripdata_2020-12.csv && ls -lh yellow_tripdata_2020-12.csv
```
```bash
-rw-r--r-- 1 root root 129M Feb  2 08:21 yellow_tripdata_2020-12.csv
```

---

## Question 2
What is the rendered value of the variable file when the inputs taxi is set to green, year is set to 2020, and month is set to 04 during execution?
{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv

### Solution
green_tripdata_2020-04.csv

---

## Question 3, 4
How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

How many rows are there for the Green Taxi data for all CSV files in the year 2020?

```bash
python count_rows.py
```

```
Total yellow taxi rows in 2020: 24,648,499
Total green taxi rows in 2020: 1,734,051
```

---

## Question 5
How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

```sql
SELECT COUNT(*) 
FROM yellow_tripdata 
WHERE filename = 'yellow_tripdata_2021-03.csv';
```

```
count
1925152
```

---

## Question 6
How would you configure the timezone to New York in a Schedule trigger?

### Solution
Check the documentation of Kestra, it mentions timezone parameter following TZ identifier.

So check this wikipedia table column 2:
https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

Answer is `Add a timezone property set to America/New_York in the Schedule trigger configuration`