# Run with
#
# scrapy runspider simple-scraper.py -t csv -o out-1.csv


# A very bare minimum spider
# Jonah Woods

from scrapy.spiders import Spider
import urllib

class SECSpider(Spider):
    name = 'SECSpider'
    #Stay with domains specified below
    allowed_domains = ['sec.gov/forms']
    start_urls = [ "https://www.sec.gov/forms" ]
    #Ensure we do not get throttled
    handle_httpstatus_list = [404, 403]
    custom_settings = { 'DOWNLOAD_DELAY': 0.5 }

    #Response below is the web page given by the server we reach out to
    #Here it is start_urls
    def parse(self, response):
        rows = response.xpath(".//td[@class='display-title-content views-field views-field-field-display-title']")
        items=[]
        for row in rows:
            file = {}
            file['url'] = 'https://www.sec.gov/' + row.xpath(".//a/@href").extract()[0]
            items.append(file)
            
        return items
    

    def download_file(download_url):
        web_file = urllib.urlopen(download_url)
        local_file = open(form_name + '.pdf', 'w')
        local_file.write(web_file.read())
        web_file.close()
        local_file.close()
        
        
        
        
        
        