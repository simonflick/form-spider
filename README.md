# Form Spider

If a page contains forms with user specific tokens, it needs to be excluded from page caching. This spider crawls a website for such forms.

## Limitations

Only detects YOOEssentials Forms and page caching using W3 Total Cache or WP Optimize.

## Dependencies

1. install Python 3.*
2. [install Scrapy](https://docs.scrapy.org/en/latest/intro/install.html)

## Running the spider

```sh
scrapy crawl form_spider -a url=https://www.example.com/
scrapy crawl form_spider -a url=https://www.example.com/ -a display=tree # displays results as tree
scrapy crawl form_spider -a url=https://www.example.com/ -a display=combined # displays results as list and tree
```

On Windows, the Anaconda Shell needs to be used.

## Register globally (Linux only)

1. Move repo to e.g. ~/Applications/form-spider
2. Add `export PATH="$HOME/Applications/form-spider"` to `~/.bashrc`
3. Execute using `form-spider.sh https://www.example.com/ tree`
