import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        for book in response.css("article.product_pod h3 a::attr(href)"):
            yield response.follow(book.get(), callback=self.parse_book)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "price": response.css("p.price_color::text").get(),
            "amount_in_stock": response.css("p.instock.availability::text").re_first(r"\d+"),
            "rating": response.css("p.star-rating::attr(class)").re_first(r"star-rating (\w+)"),
            "category": response.css("ul.breadcrumb li:nth-child(3) a::text").get(),
            "description": response.css("article.product_page p::text").get(),
            "upc": response.xpath("//th[text()='UPC']/following-sibling::td/text()").get(),
        }
