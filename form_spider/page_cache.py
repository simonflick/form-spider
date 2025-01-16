import re
from .bcolors import bcolors

def get_cache_message(response):
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