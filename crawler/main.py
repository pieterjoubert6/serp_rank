import scrapy
from handler import save_rankings
from conf import REGEON_URLS


class OptumSpider(scrapy.Spider):
    name = 'semrush'
    allowed_domains = ['semrush.com']
    start_urls = [
        x['url'] for x in REGEON_URLS
    ]

    def parse(self, response):  # noqa
        sensor_fields = response.css('div.sensor-filter-item')
        latest_ranks = []
        for index, field in enumerate(sensor_fields):
            latest_ranks.append({
                "rank": float(field.css('span:nth-child(1)::text').get()),
                "category_name": field.css('span:nth-child(2)::text').get(),
            })
        save_rankings(latest_ranks, response.request.url)
