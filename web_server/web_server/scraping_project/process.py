import scrapy
from scrapy.crawler import CrawlerProcess
from toscrape_css import ToScrapeCSSSpider

process_levelone = CrawlerProcess({
    'ELASTICSEARCH_URL': 'http://127.0.0.1:9200',
    'DEPTH_LIMIT': '2'
})

process_leveltwo = CrawlerProcess({
    'ELASTICSEARCH_URL': 'http://127.0.0.1:9200',
    'DEPTH_LIMIT': '0'
})

process_leveltwo.crawl(ToScrapeCSSSpider, "trailone", level=2, start_urls=['https://www.data-voyager.com'])
process_leveltwo.start()
