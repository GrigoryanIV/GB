import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem_2

class SujobSpider(scrapy.Spider):
    name = 'sujob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vakansii/biznes-analitik.html']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@rel = 'next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        vacansy_links = response.xpath("//div[@class='_2J-3z _3B5DQ']/div/div/span/a/@href").getall()
        for link in vacansy_links:
            yield response.follow(link, callback=self.parse_vacansy)

    def parse_vacansy(self, response: HtmlResponse):
        vacanci_name = response.css ('h1::text').get()
        vacanci_salary = response.xpath("//span[@class='_2eYAG _1nqY_ _249GZ _1dIgi']//text()").getall()
        vacanci_url = response.url
        yield ParserJobItem_2(
            name=vacanci_name,
            salary=vacanci_salary,
            _id=vacanci_url
        )