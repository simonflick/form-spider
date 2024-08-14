# Form Spider

All pages with forms need to be excluded from page caching. This spider crawls a website and returns all pages that contain a form with `method="POST"`.

## Dependencies

1. install Python 3.*
2. [install Scrapy](https://docs.scrapy.org/en/latest/intro/install.html)

## Running the spider

```sh
scrapy crawl form_spider -a url=https://www.example.com/
```

On Windows, the Anaconda Shell needs to be used.