# -*- coding: utf-8 -*-
import scrapy, csv
from scrapy.crawler import CrawlerProcess
from toscrape_css import ToScrapeCSSSpider

process_levelone = CrawlerProcess({
    'ELASTICSEARCH_URL': 'http://127.0.0.1:9200',
    'DEPTH_LIMIT': '2'
})

process_leveltwo = CrawlerProcess({
    'ELASTICSEARCH_URL': 'http://127.0.0.1:9200',
    'DEPTH_LIMIT': '5'
})

file_content =[]

with open("sample.csv","rb") as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',', quotechar='\"')
	for row in reader:
		jdata = {}
		jdata["website"] = row["website"]
		jdata["page_view"] = row["page_view"]
		jdata["page_visit"] = row["page_visit"]
		file_content.append(jdata)
	csvfile.close()

for item in file_content:
	url = item["website"]
	process_leveltwo.crawl(ToScrapeCSSSpider, "trail_two", level=2, start_urls=[url])
	process_leveltwo.start(stop_after_crawl=False)
