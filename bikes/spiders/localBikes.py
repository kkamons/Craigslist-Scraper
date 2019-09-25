# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class BikesSpider(scrapy.Spider):
    name = 'localBikes'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://stlouis.craigslist.org/search/bia?',
    'https://pittsburgh.craigslist.org/search/bia?','https://cincinnati.craigslist.org/search/bia?',
    'https://columbiamo.craigslist.org/search/bia?','https://cleveland.craigslist.org/search/bia?',
    'https://indianapolis.craigslist.org/search/bia?','https://kirksville.craigslist.org/search/bia?',
    'https://loz.craigslist.org/search/bia?','https://semo.craigslist.org/search/bia?']
    def parse(self, response):
        # titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        bikeTitles = response.xpath('//p[@class="result-info"]')
        for entry in bikeTitles:
            title=entry.xpath('a/text()').extract_first()
            # ("") forces to string
            area=entry.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            # force to string
            cost=entry.xpath('span[@class="result-meta"]/span[@class="result-price"]/text()').extract_first("")[1:]
            relURL=entry.xpath('a/@href').extract_first()
            absURL=response.urljoin(relURL)
            yield Request(absURL,callback=self.parse_page, meta={'Title':title, 'Area':area, 'Cost':cost, 'Link':absURL})
            # yield{'Title':title, 'Area':area, 'Cost':cost, 'Link':absURL}

        relNextURL=entry.xpath('//a[@class="button next"]/@href').extract_first()
        absNextURL=response.urljoin(relNextURL)
        yield Request(absNextURL, callback=self.parse)

    def parse_page(self, response):
        url=response.meta.get('Link')
        title=response.meta.get('Title')
        area=response.meta.get('Area')
        cost=response.meta.get('Cost')
        
        # the discription will not display in excel... something to do with formatting
        # this will display in notepad though, so if read into a pandas df then maybe can search through it. here anyways
        description="".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())

        # tag name and data are list types
        tagName=response.xpath('//p[@class="attrgroup"]/span/text()').extract()
        tagData=response.xpath('//p[@class="attrgroup"]/span/b/text()').extract()
        tagDataStr =''.join(item for item in tagData).lower()
        if(('58' in tagDataStr or '56' in tagDataStr) and ('road' in tagDataStr or 'cyclocross' in tagDataStr or 'gravel' in tagDataStr or 'cyclocross' in description.lower() or 'cx' in description.lower() or 'cx' in tagDataStr or 'gravel' in description.lower() or 'road' in description.lower())):
            yield{"Title": title, "Cost":cost, "Area":area,"Link":url, "TabName":tagName,"TagData":tagData}
