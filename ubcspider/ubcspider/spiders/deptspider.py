
# -*- coding: utf-8 -*-
import scrapy
from ubcspider.loaders import *
from ubcspider.items import *
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor



class UBCspider(scrapy.Spider):
    name = 'ubcspider'

    start_urls = [
        'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=1&dept=CPSC'
    ]
    rules = [
        Rule(LinkExtractor(allow='.*'), follow=True, callback="parse_course")
    ]

    def parse(self, response):
        for href in response.xpath('body/div/div/table//a/@href'):
            yield response.follow(href, self.parse_course)

    def parse_course(self, response):
        cl = CourseLoader(item=Course(), response=response)
        cl.add_xpath('name', '//h4', re='(\w{4}\s\w{3,4}\s.+)')
        cl.add_xpath('prereqs', 'body/div/div/p[3]')

        c = cl.load_item()
        yield c

