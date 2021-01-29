from datetime import datetime

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

token = "shH3Slbz4CVJo6er5rkFs0ykM-_36NwwM2bM9poNKmb76boWmGOr2IGP_yUibLDUR6OQGxnz6vD0DRHox59WYg=="
org = "RankTank"
bucket = "serp_rank"

client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)


def save_rankings(latest_ranks):
    sequence = []
    time = datetime.utcnow()
    for item in latest_ranks:
        sequence.append({
            "measurement": item["category_name"],
            "time": time,
            "fields": {
                "rank": float(item["rank"])
            }
        })
    write_api.write(bucket, org, sequence)
