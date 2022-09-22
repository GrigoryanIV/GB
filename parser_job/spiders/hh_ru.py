import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/vacancies/data-analyst'
                 ]

    def parse(self, response:HtmlResponse):

        next_page = response.xpath("//a[@data-qa = 'pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        vacansy_links = response.xpath("//div[@class='serp-item']//a[@data-qa='serp-item__title']/@href").getall()
        for link in vacansy_links :
             yield response.follow(link, callback=self.parse_vacansy)

    def parse_vacansy(self, response:HtmlResponse):
        vacanci_name = response.css ('h1::text').get()
        vacanci_salary = response.xpath ("//div[@data-qa = 'vacancy-salary']//text()").getall()
        vacanci_url = response.url
        yield ParserJobItem (
            name = vacanci_name,  
            salary = vacanci_salary,
            _id = vacanci_url
        )
    
                                    