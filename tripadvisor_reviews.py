import scrapy


class TripadvisorReviewsSpider(scrapy.Spider):
    name = "tripadvisor_reviews"
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["https://tripadvisor.com"]

    def parse(self, response):
        pass
