import re
import scrapy
import pprint
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from collections import defaultdict
from urllib.parse import urlparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class FormSpider(CrawlSpider):
    name = 'form_spider'
    pages_with_forms = []
    form_messages = {}

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
        self.base_netloc = domain

    def tree_factory(self):
        return defaultdict(self.tree_factory)

    def parse_item(self, response):
        self.logger.info('crawling %s', response.url)

        if (response.css('[data-uk-yooessentials-form]')):
            url_normalized = response.url.rstrip('/')
            message = self.get_cache_message(response)
            self.pages_with_forms.append((url_normalized, message))
            self.form_messages[url_normalized] = message
            self.add_to_tree(url_normalized)

    def get_cache_message(self, response):
        cache_comment = re.search(r'<!--(.*WP[- ]Optimize.*)-->', response.text, re.DOTALL)

        if cache_comment is not None:
            if "not served from cache" in cache_comment.group(1):
                return bcolors.OKGREEN + "Excluded from cache [WP Optimize]" + bcolors.ENDC
            else:
                return bcolors.FAIL + "Cached! [WP Optimize]" + bcolors.ENDC

        cache_comment = re.search(r'<!--(.*W3 Total Cache.*)-->', response.text, re.DOTALL)

        if cache_comment is not None:
            if "Requested URI is rejected" in cache_comment.group(1):
                return bcolors.OKGREEN + "Excluded from cache [W3 Total Cache]" + bcolors.ENDC
            else:
                return bcolors.FAIL + "Cached! [W3 Total Cache]" + bcolors.ENDC

        return bcolors.WARNING + "No cache marker found" + bcolors.ENDC

    def add_to_tree(self, url):
        parts = url.replace('https://', '').replace('http://', '').rstrip('/').split('/')
        d = self.tree
        for part in parts:
            d = d[part]

    def closed(self, reason):
        print('The following pages contain YOOEssentials forms:\n')
        for url, message in self.pages_with_forms:
            print(f'{url}  {message}')

        print('\nTree structure of the crawled forms:\n')
        print(self.format_tree(self.tree, prefix='', path=''))

    def format_tree(self, d, prefix, path):
        output = []
        
        for key in sorted(d.keys()):
            line = f'{prefix}{key}/'
            current_path = path + key + '/'
            full_url = self.construct_url(current_path).rstrip('/')

            if full_url in self.form_messages:
                line += f'  {self.form_messages[full_url]}'

            output.append(line)

            if d[key]:
                sub_prefix = prefix + '    '
                output.append(self.format_tree(d[key], sub_prefix, current_path))

        return '\n'.join(output)

    def construct_url(self, path):
        if path.startswith(self.base_netloc):
            return f'https://{path}'
        else:
            return f'https://{self.base_netloc}/{path}'
