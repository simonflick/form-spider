#!/usr/bin/env bash

cd $(dirname $0) # switch to dir of this file
scrapy crawl form_spider_sitemap -a url=$1 -a display=$2
