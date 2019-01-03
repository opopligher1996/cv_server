# -*- coding: utf-8 -*-
import csv
import tldextract
from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings
from toscrape_css import ToScrapeCSSSpider
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings

def run_spider(level):

    file_content =[]

    with open("web_server/scraping_project/project_website_list.csv","rb") as csvfile:
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
        p = Process(target = test , args = (url,level))
        p.start()
        p.join()
        print('done '+url)

    return 0

def test(url,level):
    print('level = '+level)
    if level=='1':
        process_levelone = CrawlerProcess({
            'ELASTICSEARCH_URL': 'http://127.0.0.1:9200',
            'DEPTH_LIMIT': '2'
        })
        allowed_domains = tldextract.extract(url).domain
        if tldextract.extract(url).suffix!='':
            allowed_domains = allowed_domains + '.' + tldextract.extract(url).suffix
        process_levelone.crawl(ToScrapeCSSSpider, "trail_two", level=1, start_urls=[url], allowed_domains=[allowed_domains])
        process_levelone.start(stop_after_crawl=True)
    else:
        process_leveltwo = CrawlerProcess({
            'ELASTICSEARCH_URL': 'http://127.0.0.1:9200',
            'DEPTH_LIMIT': '6'
        })
        allowed_domains = tldextract.extract(url).domain
        if tldextract.extract(url).suffix!='':
            allowed_domains = allowed_domains + '.' + tldextract.extract(url).suffix
        process_leveltwo.crawl(ToScrapeCSSSpider, "trail_two", level=2, start_urls=[url], allowed_domains=[allowed_domains])
        process_leveltwo.start(stop_after_crawl=True)
