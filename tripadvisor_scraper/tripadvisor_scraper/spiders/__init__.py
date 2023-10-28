import scrapy

class TripadvisorReviewsSpider(scrapy.Spider):
    name = "tripadvisor_reviews"
    start_urls = [
        'https://www.tripadvisor.com/Restaurants-g60713-San_Francisco_California.html',
    ]

    def parse(self, response):
        # Extract review data (e.g., reviewer name, text, rating)
        review_items = response.xpath('//div[@data-test-target="reviews-tab"]')

        for item in review_items:
            yield {
                'reviewer_name': item.xpath('.//div[contains(@class, "info_text")]/a/text()').get(),
                'review_text': item.xpath('.//q/span/text()').get(),
                'rating': item.xpath('.//span[contains(@class, "ui_bubble_rating")]/@class').re_first(r'\d+'),
            }
