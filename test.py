import scrapy
import json
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
import urllib.parse as urlparse

class AppstorecrawlerItem(scrapy.Item):
    # fields here
    # name = Field()
    Link = scrapy.Field()
    Item_name = scrapy.Field()
    Updated = scrapy.Field()
    Author = scrapy.Field()
    Filesize = scrapy.Field()
    Version = scrapy.Field()
    Compatibility = scrapy.Field()
    Content_rating = scrapy.Field()
    Author_link = scrapy.Field()
    Genre = scrapy.Field()
    Price = scrapy.Field()
    Rating_value = scrapy.Field()
    Rating_count = scrapy.Field()
    Description = scrapy.Field()
    Language = scrapy.Field()
    Artwork = scrapy.Field()

class MySpider(CrawlSpider):
  name = "final"
  start_urls = ["https://itunes.apple.com/cn/app/%E5%96%9C%E9%A9%AC%E6%8B%89%E9%9B%85fm-%E5%90%AC%E4%B9%A6%E7%A4%BE%E5%8C%BA-%E7%94%B5%E5%8F%B0%E6%9C%89%E5%A3%B0%E5%B0%8F%E8%AF%B4%E7%9B%B8%E5%A3%B0%E8%AF%84%E4%B9%A6/id876336838?mt=8"]
  def abs_url(url, response):
      """Return absolute link"""
      base = response.xpath('//head/base/@href').extract()
      if base:
        base = base[0]
      else:
        base = response.url
      return urlparse.urljoin(base, url)
    
  def parse(self,response):
      hxs = Selector(response)
      titles = hxs.xpath('/html')
      items = []
      for titles in titles :
        item = AppstorecrawlerItem()
        item["Link"] = str(titles.xpath('//*[@rel="canonical"]/@href').extract())
        item["Item_name"] = str(titles.xpath('//h1[@itemprop="name"]/text()').extract())
        item["Updated"] = str(titles.xpath('//*[@itemprop="datePublished"]/text()').extract())
        item["Author"] = str(titles.xpath('//span[@itemprop="name"]/text()').extract())
        item["Filesize"] = str(titles.xpath('//ul[@class="list"]/li[5]/text()').extract())
        item["Version"] = str(titles.xpath('//*[@itemprop="softwareVersion"]/text()').extract())
        item["Compatibility"] = str(titles.xpath('//*[@itemprop="operatingSystem"]/text()').extract())
        item["Content_rating"] = str(titles.xpath('//*[@class="app-rating"]/a/text()').extract())
        item["Author_link"] = str(titles.xpath('//*[@class="app-links"]/a[1]/@href').extract())
        item["Genre"] = str(titles.xpath('//*[@itemprop="applicationCategory"]/text()').extract())
        item["Price"] = str(titles.xpath('//*[@itemprop="price"]/text()').extract())
        item["Rating_value"] = str(titles.xpath('//*[@itemprop="ratingValue"]/text()').extract())
        item["Rating_count"] = str(titles.xpath('//*[@itemprop="reviewCount"]/text()').extract())
        item["Description"] = str(response.xpath('//*[@itemprop="description"]/text()').extract())
        item["Language"] = str(response.xpath('//*[@class="language"]/text()').extract())
        item["Artwork"] = str(titles.xpath('//*[@id="left-stack"]/div[1]/a[1]/div/img/@src').extract())
        items.append(item)
      filename = 'appstore'
      with open (filename, 'w', encoding = 'utf-8') as fo:
          for item in items:
              print(dict(item))
              fo.write(json.dumps(dict(item),ensure_ascii=False))
      return items

      

