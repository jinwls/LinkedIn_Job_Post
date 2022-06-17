import scrapy
import time
import json
from job.items import JobItem
from scrapy.http import Request
from scrapy.loader import ItemLoader


class LinkedinScrape(scrapy.Spider):
    name = 'linkedin'
    def start_requests(self):
        urls = [f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keyword}&location=%EB%AF%B8%EA%B5%AD&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start={page}' for page in range(25,1000,25) for keyword in ['data%20specialist','data%20analyst','data%20scientist','data%20engineer']]
        for url in urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        print(response)
        for link in response.css('div.base-card a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_lists)
            time.sleep(0.5)


    def parse_lists(self, response):
        l = ItemLoader(item = JobItem(), selector = response)

        l.add_css('title', 'h1 ::text')
        l.add_css('job', 'h1 ::text')
        l.add_css('company', 'a.topcard__org-name-link ::text')
        l.add_css('city','span.topcard__flavor--bullet ::text')
        l.add_css('state','span.topcard__flavor--bullet ::text')
        l.add_css('level', 'li.description__job-criteria-item span ::text')
        l.add_css('type', 'li.description__job-criteria-item span ::text')
        l.add_css('function', 'li.description__job-criteria-item span ::text')
        l.add_css('industry', 'li.description__job-criteria-item span ::text')
        l.add_css('detail', 'div.show-more-less-html__markup ::text')

        script = response.css('script::text')[1].extract()
        data = json.loads(script)
        date = data['datePosted'][:10]
        l.add_value('date', date)

        yield l.load_item()



class JobKoreaScrape(scrapy.Spider):
    name = 'jobkorea'
    start_urls = ['https://www.jobkorea.co.kr/Search/?stext=데이터%20분석&tabType=recruit&Page_No=1']

    def parse(self, response):
        for link in response.css('li.list-post a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_lists)
    
    def parse_lists(self, response):
        coName=response.css('span.coName::text').get().replace('\r\n','').replace(' ','')
