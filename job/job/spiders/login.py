# import scrapy

# class LinkedinScrape(scrapy.Spider):
#     name = 'linkedin'
#     start_urls = ['https://kr.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data&location=%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD&geoId=105149562&trk=public_jobs_jobs-search-bar_search-submit&start=25']

#     def parse(self, response):
#         for link in response.css('div.base-card a::attr(href)'):
#             yield response.follow(link.get(), callback=self.parse_lists)

#     def parse_lists(self, response):
#         yield {
#             'description': response.css('div.jobs-box__html-content::text').strip()
#         }



# class LinkedinScrape(scrapy.Spider):
#     name = 'linkedin'
#     start_urls = ['https://www.linkedin.com/uas/login']

#     def parse(self, response):
#         token = response.css('form#otp-generation input::attr(value)').extract_first()
#         return FormRequest.from_response(response, formdata={
#             'csrfToken' : token,
#             'session_key' : '',
#             'session_password' : ''
#         }, callback = self.start_scraping)
    
#     def start_scraping(self, response):
#         item = response.css('div ::text').get()
#         print(item)
