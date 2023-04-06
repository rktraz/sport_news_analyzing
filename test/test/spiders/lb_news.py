import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'lb_news'
    allowed_domains = ['lb.ua']
    start_urls = ['https://lb.ua/sport?page=%s' % page for page in range(1, 4)]
    
    def parse(self, response):
        # Loop through the list of article previews and follow each link
        for preview in response.css(".item-news"):
            article_url = preview.css("a::attr(href)").get()
            yield response.follow(article_url, callback=self.parse_article)
    
    def parse_article(self, response):

        # Extract the article title, author, date, and text
        title = response.css("h1::text").get()
        author = response.css(".author-block span::text").get()
        date = response.css(".time::text").get()
        text = "\n".join(response.css(".MsoNormal *::text").getall())

        # Return the data as a dictionary
        yield {
            "title": title,
            "author": author,
            "date": date,
            "text": text
        }