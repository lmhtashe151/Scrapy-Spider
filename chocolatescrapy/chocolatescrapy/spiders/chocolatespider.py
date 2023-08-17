import scrapy
from chocolatescrapy.items import ChocolateProduct
from chocolatescrapy.itemloaders import ChocolateProductLoader
import re

from urllib.parse import urlencode

API_KEY = 'ef8e806e-4975-436c-8693-f4375d626bbb'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url 


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    # start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def start_requests(self):
        start_urls = 'https://www.chocolate.co.uk/collections/all'
        # return super().start_requests()
        yield scrapy.Request(url=get_proxy_url(start_urls),callback= self.parse)



    def parse(self, response):

        products = response.css('product-item')
        

        for product in products:
            # yield{
            #     'name': product.css('a.product-item-meta__title::text').get(),
            #     'price': product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>',''),
            #     'url': product.css('div.product-item-meta a').attrib['href']
                
            # }
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text'),
            # Extract the raw price text
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            yield chocolate.load_item()


        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            # yield scrapy.Request(url=next_page_url, callback=self.parse) 
            # proxy
            yield scrapy.Request(get_proxy_url(url=next_page_url), callback=self.parse) 
# scrapy crawl chocolatespider -o mydata.csv 
 

        pass
