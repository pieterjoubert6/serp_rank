from datetime import datetime

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from ..conf import API_TOKEN, BUCKET, ORG

client = InfluxDBClient(url="http://localhost:8086", token=API_TOKEN, org=ORG)
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
    write_api.write(BUCKET, ORG, sequence)
