import scrapy
import csv

class TripadvisorReviewsSpider(scrapy.Spider):
    name = "tripadvisor_reviews"
    start_urls = [
        'https://www.tripadvisor.com/Restaurants-g60713-San_Francisco_California.html',
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.50 Safari/537.36',
    }

    def parse(self, response):
        for restaurant in response.css('.BMQDV, .FGwzt, .ukgoS'):
            yield response.follow(restaurant, self.parse_reviews)

    def parse_reviews(self, response):
        reviews_head = response.xpath('//div[@id="taplc_location_reviews_list_resp_rr_resp_0"]')
        
        reviews = reviews_head.xpath('//div[contains(@class, "listContainer")]')

        with open('tripadvisor_reviews.csv', 'a', newline='') as csvfile:
            fieldnames = ['reviewer_name', 'review_text', 'rating']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            ##file empty?
            if csvfile.tell() == 0:
                writer.writeheader()

            # Loop and append values
            for review in reviews:
                reviewer_name = review.xpath('.//div[contains(@class, "info_text")]//div/text()').get()
                print(reviewer_name)
                review_text = review.xpath('.//p[contains(@class, "partial_entry")]/text()').get()
                print(review_text)
                rating = review.xpath('.//span[contains(@class, "ui_bubble_rating bubble_")]/@class').re_first(r'\d+')
                print(rating)

                # Missing data? before append
                if reviewer_name and review_text and rating:
                    writer.writerow({
                        'reviewer_name': reviewer_name,
                        'review_text': review_text,
                        'rating': rating,
                    })
