import json
import scrapy
import re

from handler import save_rankings


class OptumSpider(scrapy.Spider):
    name = 'semrush'
    allowed_domains = ['semrush.com']
    start_urls = ['https://www.semrush.com/sensor/?db=US&category=']

    def parse(self, response):  # noqa
        script_tag = (re.sub(r'[\s+;]', '', response.xpath('//script/text()')[12].get()))
        print(script_tag)
        category_definitions = {}
        sensor_fields = response.css('div.sensor-filter-item')
        latest_ranks = []
        for index, field in enumerate(sensor_fields):
            category_definitions[index] = field.css('span:nth-child(2)::text').get()
            latest_ranks.append({
                "rank": float(field.css('span:nth-child(1)::text').get()),
                "category": index,
                "category_name": field.css('span:nth-child(2)::text').get(),
            })

        ranked_data = "{" + script_tag[script_tag.find('ranks') - 1:].strip()
        ranked_data = ranked_data[:ranked_data.find(']') + 2].strip() + "}"
        ranked_data = ranked_data[:10] + "\"US\"" + ranked_data[23:]

        json_object = json.loads(ranked_data)

        # file2write = open("thedata.json", 'w')
        # file2write.write(str(json_object))
        # file2write.close()

        save_rankings(json_object, category_definitions, latest_ranks)
