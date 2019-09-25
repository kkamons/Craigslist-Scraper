# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class BikesSpider(scrapy.Spider):
    name = 'craigslist'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://denver.craigslist.org/search/bia?','https://minneapolis.craigslist.org/search/bia?',
    'https://stlouis.craigslist.org/search/bia?','https://kansascity.craigslist.org/search/bia?',
    'https://wichita.craigslist.org/search/bia?','https://omaha.craigslist.org/search/bia?',
    'https://desmoines.craigslist.org/search/bia?','https://iowacity.craigslist.org/search/bia?',
    'https://milwaukee.craigslist.org/search/bia?','https://oklahomacity.craigslist.org/search/bia?',
    'https://pittsburgh.craigslist.org/search/bia?','https://cincinnati.craigslist.org/search/bia?',
    'https://columbus.craigslist.org/search/bia?','https://cleveland.craigslist.org/search/bia?',
    'https://detroit.craigslist.org/search/bia?','https://indianapolis.craigslist.org/search/bia?',
    'https://losangeles.craigslist.org/search/bia?','https://newyork.craigslist.org/search/bia?',
    'https://memphis.craigslist.org/search/bia?','https://nashville.craigslist.org/search/bia?',
    'https://bham.craigslist.org/search/bia?','https://atlanta.craigslist.org/search/bia?',
    'https://louisville.craigslist.org/search/bia?','https://neworleans.craigslist.org/search/bia?',
    'https://charlotte.craigslist.org/search/bia?','https://washingtondc.craigslist.org/search/bia?',
    'https://boston.craigslist.org/search/bia?']

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

        # tagDict={}
        # for i in range(len(tagName)):
        #     tagDict[tagName[i]]=tagData[i]
        if(('jamis' in tagDataStr) or ('road' in tagDataStr.lower()) or ('jamis' in description.lower()) or ('58' in description.lower())):
            yield{"Title": title, "Cost":cost, "Area":area,"Link":url, "TabName":tagName,"TagData":tagData}

        # yield{"Title": title, "Cost":cost, "Area":area,"Link":url, "TabName":tagName,"TagData":tagData}
