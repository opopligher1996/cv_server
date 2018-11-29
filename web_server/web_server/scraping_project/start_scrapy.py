# -*- coding: utf-8 -*-
import csv
from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings
from toscrape_css import ToScrapeCSSSpider
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings

def run_spider():
    p = Process(target=_crawl)
    p.start()
    p.join()

def _crawl():
    process_leveltwo = CrawlerProcess({
        'ELASTICSEARCH_URL': 'http://127.0.0.1:9200',
        'DEPTH_LIMIT': '5'
    })

    file_content =[]

    with open("project_website_list.csv","rb") as csvfile:
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
        print('start '+url)
        process_leveltwo.crawl(ToScrapeCSSSpider, "trail_two", level=2, start_urls=[url])
        process_leveltwo.start(stop_after_crawl=True)
        print('done '+url)

    return 0
