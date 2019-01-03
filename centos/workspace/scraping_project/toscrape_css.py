# -*- coding: utf-8 -*-
import scrapy
import requests, json
import time
from datetime import datetime
from scrapy import Request
from elasticsearch import Elasticsearch, helpers
from urlparse import urlparse
from pprint import pprint


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    
    def __init__(self, project_name, level, start_urls):
        if start_urls is not None:
            self.start_urls = start_urls
            self.allowed_domains = [ urlparse(s).netloc for s in self.start_urls]
        self.project_name = project_name
        self.level = level

    def start_requests(self):
        self.actions = []
        if self.settings['ELASTICSEARCH_URL'] is not None:
            self.elasticsearch_url = self.settings['ELASTICSEARCH_URL']
        else:
            self.elasticsearch_url = 'http://127.0.0.1:9200'
        
        for url in self.start_urls:
            item = {'start_url': url}
            request = Request(url, dont_filter=True)
            # set the meta['item'] to use the item in the next call back
            request.meta['item'] = item
            yield request

    def parse(self, response):
        es = self.create_Elasticsearch(self.elasticsearch_url)
        url = urlparse(response.request.url)
        index_date = datetime.now().strftime('%Y.%m.%d')
        
        params = ';{}'.format(url.params) if url.params != '' else ''
        query = '?{}'.format(url.query) if url.query != '' else ''
        fragment = '#{}'.format(url.fragment) if url.fragment != '' else ''
        path = '{path}{params}{query}{fragment}'.format(path=url.path, params=params, 
            query=query, fragment=fragment)
        
        title = response.css('title').extract_first().replace('<title>','').replace('</title>','');
        doc = {
            'domain_name': url.netloc,
            'route': response.request.url,
            'content': response.xpath('//body').extract(),
            'title': title,
            'level': self.level,
            'url': path,
            'project_name': self.project_name,
            'timestamp': datetime.now()
        }
        yield doc
        self.actions.append({
            "_index": "cpr-" + self.project_name + "-" + index_date,
            "_type": "_doc",
            "_source": doc
        })
        for href in response.css("a::attr(href)").extract():
            yield scrapy.Request(response.urljoin(href))

    def closed(self, reason):
        es = self.create_Elasticsearch(self.elasticsearch_url)
        self.send_json(es, self.actions)

    def send_json(self, es, actions):
        return helpers.bulk(es, actions, stats_only=True, chunk_size=500000)

    def create_Elasticsearch(self, host, user=None, password=None):
        if user is None or password is None:
            return Elasticsearch(host, timeout=100)
        else:
            return Elasticsearch(host, http_auth=(user,password), timeout=100)
