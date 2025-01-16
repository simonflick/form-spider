import scrapy
import pprint
from collections import defaultdict
from urllib.parse import urlparse
from scrapy.spiders import SitemapSpider
from ..url_tree import URLTree
from ..page_cache import get_cache_message

class FormSpiderSitemap(SitemapSpider):
    name = 'form_spider_sitemap'
    pages_with_forms = []
    form_messages = {}

    def __init__(self, url=None, display=None, *args, **kwargs):
        super(FormSpiderSitemap, self).__init__(*args, **kwargs)
        
        if not url:
            raise ValueError('Please provide a URL to crawl')

        domain = urlparse(url).netloc

        if not domain:
            raise ValueError('Could not extract domain from URL')

        self.allowed_domains = [domain]
        self.base_netloc = domain
        self.sitemap_urls = [f'{url.rstrip("/")}/robots.txt']
        self.output_display = display
        self.tree = URLTree()

    def parse(self, response):
        self.logger.info('crawling %s', response.url)

        if (response.css('[data-uk-yooessentials-form]')):
            url_normalized = response.url.rstrip('/')
            message = get_cache_message(response)
            self.pages_with_forms.append((url_normalized, message))
            self.form_messages[url_normalized] = message
            self.tree.add(url_normalized)

    def closed(self, reason):
        print('The following pages contain YOOEssentials forms:\n')
        
        match self.output_display:
            case 'combined':
                for url, message in self.pages_with_forms:
                    print(f'{url}  {message}')
                print('\nTree structure of the crawled forms:\n')
                print(self.tree.format(self.form_messages, self.base_netloc))
            case 'tree':
                print(self.tree.format(self.form_messages, self.base_netloc))
            case _:
                for url, message in self.pages_with_forms:
                    print(f'{url}  {message}')
            
