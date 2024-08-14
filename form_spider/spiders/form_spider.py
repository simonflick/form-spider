import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from collections import defaultdict
from urllib.parse import urlparse

class FormSpider(CrawlSpider):
    name = 'form_spider'
    pages_with_forms = []

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, url=None, *args, **kwargs):
        super(FormSpider, self).__init__(*args, **kwargs)
        
        if not url:
            raise ValueError('Please provide a URL to crawl')

        domain = urlparse(url).netloc

        if not domain:
            raise ValueError('Could not extract domain from URL')

        self.start_urls = [url]
        self.allowed_domains = [domain]
        self.tree = defaultdict(self.tree_factory)

    def tree_factory(self):
        return defaultdict(self.tree_factory)

    def parse_item(self, response):
        self.logger.info('crawling %s', response.url)

        if response.css('form[method="post"]') or response.css('form[method="POST"]'):
            self.add_to_tree(response.url)
            self.pages_with_forms.append(response.url)

    def add_to_tree(self, url):
        parts = url.replace('https://', '').replace('http://', '').rstrip('/').split('/')
        d = self.tree
        for part in parts:
            d = d[part]

    def closed(self, reason):
        print('The following pages contain forms with POST method:\n')
        print('\n'.join(self.pages_with_forms))
        print('\nTree structure of the crawled URLs:\n')
        print(self.format_tree(self.tree, '', ''))

    def format_tree(self, d, prefix, path):
        output = []
        for key in sorted(d.keys()):
            # If this key is the only child and its name is the last part, don't add it separately
            if len(d[key]) == 0 and len(d) == 1:
                output.append(f'{prefix}{key}/')
            else:
                line = f'{prefix}{key}/'
                output.append(line)
                if d[key]:
                    sub_prefix = ' ' * (len(line) - len(key) - 1) + '    '
                    output.append(self.format_tree(d[key], sub_prefix, path + key + '/'))
        return '\n'.join(output)
