import scrapy
import pprint
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from ..url_tree import URLTree
from ..page_cache import get_cache_message

class FormSpider(CrawlSpider):
    name = 'form_spider'
    pages_with_forms = []
    form_messages = {}

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, url=None, display=None, *args, **kwargs):
        super(FormSpider, self).__init__(*args, **kwargs)
        
        if not url:
            raise ValueError('Please provide a URL to crawl')

        domain = urlparse(url).netloc

        if not domain:
            raise ValueError('Could not extract domain from URL')

        self.start_urls = [url]
        self.allowed_domains = [domain]
        self.base_netloc = domain
        self.output_display = display
        self.tree = URLTree()

    def parse_item(self, response):
        self.logger.info('crawling %s', response.url)

        if (response.css('[data-uk-yooessentials-form]')):
            url_normalized = response.url.rstrip('/')
            message = get_cache_message(response)
            self.pages_with_forms.append((url_normalized, message))
            self.form_messages[url_normalized] = message
            self.tree.add(url_normalized)

    def closed(self, reason):
        if len(self.pages_with_forms) > 0:
            print('The following pages contain YOOEssentials forms:\n')
        else:
            print('No forms were found.\n')
        
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
            