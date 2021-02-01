from datetime import datetime
import json
import scrapy
import re

from conf import API_TOKEN, BUCKET, ORG

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


client = InfluxDBClient(url="http://localhost:8086", token=API_TOKEN)
write_api = client.write_api(write_options=SYNCHRONOUS)


def save_rankings(rank_data, category_definitions, current_url):
    sequence = []
    regions_urls = [
        {'region': 'United States', 'url': 'https://www.semrush.com/sensor/?db=US&category=', 'device': "Desktop"},
        {'region': 'United Kingdom', 'url': 'https://www.semrush.com/sensor/?db=UK&category=', 'device': "Desktop"},
        {'region': 'Germany', 'url': 'https://www.semrush.com/sensor/?db=DE&category=', 'device': "Desktop"},
        {'region': 'Italy', 'url': 'https://www.semrush.com/sensor/?db=IT&category=', 'device': "Desktop"},
        {'region': 'Spain', 'url': 'https://www.semrush.com/sensor/?db=ES&category=', 'device': "Desktop"},
        {'region': 'France', 'url': 'https://www.semrush.com/sensor/?db=FR&category=', 'device': "Desktop"},
        {'region': 'Australia', 'url': 'https://www.semrush.com/sensor/?db=AU&category=', 'device': "Desktop"},
        {'region': 'United States', 'url': 'https://www.semrush.com/sensor/?db=MOBILE-US&category=',
         'device': "Mobile"},
        {'region': 'United Kingdom', 'url': 'https://www.semrush.com/sensor/?db=MOBILE-UK&category=',
         'device': "Mobile"},
        {'region': 'Germany', 'url': 'https://www.semrush.com/sensor/?db=MOBILE-DE&category=', 'device': "Mobile"},
        {'region': 'Italy', 'url': 'https://www.semrush.com/sensor/?db=MOBILE-IT&category=', 'device': "Mobile"},
        {'region': 'Spain', 'url': 'https://www.semrush.com/sensor/?db=MOBILE-ES&category=', 'device': "Mobile"},
        {'region': 'France', 'url': 'https://www.semrush.com/sensor/?db=MOBILE-FR&category=', 'device': "Mobile"},
        {'region': 'Australia', 'url': 'https://www.semrush.com/sensor/?db=MOBILE-AU&category=', 'device': "Mobile"},
    ]
    region = None
    device = None
    for item in regions_urls:
        if item['url'] == current_url:
            region = item['region']
            device = item['device']
            break
    if None in [region, device]:
        return
    for item in rank_data['ranks']['US']:
        item['category_name'] = category_definitions[item.get('category', 0)]
        date_item = datetime.fromisoformat(item["date"])
        sequence.append({
            "measurement": region,
            "time": datetime.utcfromtimestamp(date_item.timestamp()),
            "tags": {
                "category_name": item["category_name"],
                "device": device
            },
            "fields": {
                "value": float(item["rank"])
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

        save_rankings(json_object, category_definitions, response.request.url)
