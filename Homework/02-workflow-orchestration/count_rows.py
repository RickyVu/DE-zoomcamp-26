import requests
import pandas as pd
from io import BytesIO
import gzip

def download_and_count(year=2020, taxi_type='yellow'):
    base_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_type}/"
    total_rows = 0
    
    for month in range(1, 13):
        month_str = f"{month:02d}"
        filename = f"{taxi_type}_tripdata_{year}-{month_str}.csv.gz"
        url = base_url + filename
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Read and decompress the gzip file
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz_file:
                df = pd.read_csv(gz_file, nrows=0)
                
                gz_file.seek(0)
                row_count = sum(1 for line in gz_file) - 1  # Subtract header row
                total_rows += row_count
                print(f"  Rows in {filename}: {row_count:,}")
                
        except Exception as e:
            print(f"  Could not download {filename}: {e}")
    
    return total_rows

def download_and_count_single(month=1, year=2021, taxi_type='yellow'):
    base_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_type}/"
    total_rows = 0
    
    month_str = f"{month:02d}"
    filename = f"{taxi_type}_tripdata_{year}-{month_str}.csv.gz"
    url = base_url + filename
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Read and decompress the gzip file
        with gzip.GzipFile(fileobj=BytesIO(response.content)) as gz_file:
            df = pd.read_csv(gz_file, nrows=0)
            
            gz_file.seek(0)
            row_count = sum(1 for line in gz_file) - 1  # Subtract header row
            total_rows += row_count
            
    except Exception as e:
        print(f"  Could not download {filename}: {e}")
    
    return total_rows

# Count yellow taxi rows
yellow_total = download_and_count(2020, 'yellow')
print(f"\nTotal yellow taxi rows in 2020: {yellow_total:,}\n")

# Count green taxi rows
green_total = download_and_count(2020, 'green')
print(f"\nTotal green taxi rows in 2020: {green_total:,}")

yellow_march_21 = download_and_count_single(3, 2021, 'yellow')
print(f"\nTotal yellow taxi rows in March 2021: {yellow_march_21:,}")