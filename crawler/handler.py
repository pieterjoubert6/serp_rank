from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "paste_token"
org = "ranktank"
bucket = "serp_rank"

client = InfluxDBClient(url="http://localhost:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)


def save_rankings(latest_ranks):
    sequence = []
    time = datetime.utcnow()
    for item in latest_ranks:
        sequence.append(f'mem,host=host1 category={item["category"]} rank={item["rank"]}')
        point = Point("mem") \
            .tag("category_name", f'{item["category_name"]}') \
            .field("rank", float(item["rank"]))\
            .time(time, WritePrecision.NS)
        write_api.write(bucket, org, point)
