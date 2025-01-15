#!/usr/bin/env bash

cd $(dirname $0) # switch to dir of this file
scrapy crawl form_spider -a url=$1
