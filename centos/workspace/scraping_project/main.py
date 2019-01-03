# -*- coding: utf-8 -*-
import scrapy, csv
from scrapy.crawler import CrawlerProcess
from toscrape_css import ToScrapeCSSSpider
from twisted.internet import reactor
from billiard import Process
from argparse import ArgumentParser

parser = ArgumentParser()
file_content =[]


parser.add_argument("-p", help="parse project name in this arguement",  default="random_project")
parser.add_argument("-l", help="parse crawling level in this arguement",  default=5)
parser.add_argument("-f", help="parse your input filepath here",  default="samplefile.csv")
args = parser.parse_args()

def test(url,level):
	process_levelone = CrawlerProcess({
	    'ELASTICSEARCH_URL': 'http://127.0.0.1:9200',
	    'DEPTH_LIMIT': '2'
	})
	process_leveltwo = CrawlerProcess({
	    'ELASTICSEARCH_URL': 'http://127.0.0.1:9200',
	    'DEPTH_LIMIT': '5'
	})
	if level is 2:
		process_levelone.crawl(ToScrapeCSSSpider, args.p, level=2, start_urls=[url])
		process_levelone.start(stop_after_crawl=True)
	elif level is 5:
		process_leveltwo.crawl(ToScrapeCSSSpider, args.p, level=5, start_urls=[url])
		process_leveltwo.start(stop_after_crawl=True)

with open(args.f,"rb") as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		jdata = {}
		jdata["website"] = row["website"]
		file_content.append(jdata)
		print jdata

	csvfile.close()

for item in file_content:
	url = item['website']
	print('start '+ url)
	p = Process(target = test , args = (url,args.l))
	p.start()
	p.join()
	print('done '+url)


