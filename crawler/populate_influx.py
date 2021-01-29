from datetime import datetime
import json
import scrapy
import re

from ..conf import API_TOKEN, BUCKET, ORG

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


client = InfluxDBClient(url="http://localhost:8086", token=API_TOKEN)
write_api = client.write_api(write_options=SYNCHRONOUS)


def save_rankings(rank_data, category_definitions):
    sequence = []
    for item in rank_data['ranks']['US']:
        item['category_name'] = category_definitions[item.get('category', 0)]
        date_item = datetime.fromisoformat(item["date"])
        sequence.append({
            "measurement": item["category_name"],
            "time": datetime.utcfromtimestamp(date_item.timestamp()),
            "fields": {
                "rank": float(item["rank"])
            }
        })
    write_api.write(BUCKET, ORG, sequence)


class OptumSpider(scrapy.Spider):
    name = 'semrush'
    allowed_domains = ['semrush.com']
    start_urls = ['https://www.semrush.com/sensor/?db=US&category=']

    def parse(self, response):  # noqa
        script_tag = (re.sub(r'[\s+;]', '', response.xpath('//script/text()')[12].get()))
        category_definitions = {}
        sensor_fields = response.css('div.sensor-filter-item')
        latest_ranks = []
        for index, field in enumerate(sensor_fields):
            category_definitions[index] = field.css('span:nth-child(2)::text').get()
            latest_ranks.append({
                "rank": float(field.css('span:nth-child(1)::text').get()),
                "category_name": field.css('span:nth-child(2)::text').get(),
            })
        ranked_data = "{" + script_tag[script_tag.find('ranks') - 1:].strip()
        ranked_data = ranked_data[:ranked_data.find(']') + 2].strip() + "}"
        ranked_data = ranked_data[:10] + "\"US\"" + ranked_data[23:]

        json_object = json.loads(ranked_data)

        save_rankings(json_object, category_definitions)
