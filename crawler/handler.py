from datetime import datetime

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from conf import API_TOKEN, BUCKET, ORG, REGION_URLS

client = InfluxDBClient(url="http://localhost:8086", token=API_TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)


def save_rankings(latest_ranks, current_url):
    REGION_URLS
    sequence = []
    region = None
    device = None
    for item in REGION_URLS:
        if item['url'] == current_url:
            region = item['region']
            device = item['device']
            break
    time = datetime.utcnow()
    for item in latest_ranks:
        sequence.append({
            "measurement": region,
            "time": time,
            "tags": {
                "category_name": item["category_name"],
                "device": device
            },
            "fields": {
                "value": float(item["rank"])
            }
        })
    write_api.write(BUCKET, ORG, sequence)
