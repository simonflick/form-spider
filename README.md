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

## Register globally (Linux only)

1. Move repo to e.g. ~/Applications/form-spider
2. Add `export PATH="$HOME/Applications/form-spider"` to `~/.bashrc`
3. Execute using `form-spider.sh https://www.example.com/`
