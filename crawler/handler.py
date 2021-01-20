from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "paste_token"
org = "ranktank"
bucket = "serp_rank"

client = InfluxDBClient(url="http://localhost:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)


def save_rankings(rank_data, category_definitions, latest_ranks):
    file2write = open("metrics", 'w')
    sequence = []
    time = datetime.utcnow()
    for item in latest_ranks:
        print(item)
        print(f'mem,host=semrush category_name="{item["category_name"]}" rank={item["rank"]}')
        file2write.write(
            f'serp_rank{{category="{item["category"]}",category_name="{item["category_name"]}"}} {item["rank"]} \n'
        )
        sequence.append(f'mem,host=host1 category={item["category"]} rank={item["rank"]}')
        point = Point("mem") \
            .tag("category_name", f'{item["category_name"]}') \
            .field("rank", float(item["rank"]))\
            .time(time, WritePrecision.NS)
        write_api.write(bucket, org, point)
    file2write.close()
