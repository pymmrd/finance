# -*- coding:utf-8 -*-

#StdLib imports
import os
import sys
import time
import random
import urllib2
import urlparse
import traceback
from datetime import datetime

#Third-party imports
from lxml import html

pathjoin = os.path.join
abspath = os.path.abspath
dirname = os.path.dirname

CURRENT_PATH = abspath(dirname(__file__))
PROJECT_PATH = abspath(dirname(CURRENT_PATH))

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'finance.settings'
#Django Core imports
from django.utils.hashcompat import md5_constructor as md5

from news.models import NewsRule, Site, NewsItem 

def get_content(url):
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17"
    ]

    content = ''
    headers = {'User-Agent':random.choice(user_agents)}
    req = urllib2.Request(url=url, headers=headers)
    try:
        content = urllib2.urlopen(req).read()
    except urllib2.HTTPError, e:
        if e.code == 503 : 
            time.sleep(30)
            content = tryAgain(req, 0)
    except :
        time.sleep(30)
        content = tryAgain(req, 0)
    return content

def tryAgain(url, retries=0):
    content = ''
    if retries < 4:
        try:
            time.sleep(30)
            content = urllib2.urlopen(req).read()
        except :
            retries += 1
            content = tryAgain(url, retries)
    return content

def get_chksum(title, url, pub_date):
    return md5("%s%s%s" % (title, url, pub_date)).hexdigest()

def check_news_exists_or_not(chksum):
    exists = False
    try:
        NewsItem.objects.get(chksum=chksum)
    except NewsItem.DoesNotExist:
        pass
    else:
        exists = True
    return exists

def gen_news(title, category, site, url, chksum, pub_date):
    ni = NewsItem()
    ni.site = site
    ni.title = title
    ni.url = url
    ni.pub_date = pub_date
    ni.category = category
    ni.chksum = chksum 
    ni.save()

def conact_url(url, link):
    if not url.startswith('http'):
        #parse_domain = urlparse.urlparse(link)
        #domain = parse_domain.netloc
        #scheme = parse_domain.scheme
        #uri = '%s://%s' % (scheme, domain)
        url = urlparse.urljoin(link, url)
    return url
        

def spider():
    crawlers = NewsRule.objects.all() 
    count = 0
    for crawl in crawlers:
        link = crawl.url
        content = get_content(link)
        dom = html.fromstring(content)
        items = dom.xpath(crawl.xpath_prefix)
        for item in items:
            try:
                url = item.xpath(crawl.url_xpath)[0]
                url = url.encode('utf-8')
                url = conact_url(url, link)
                title = item.xpath(crawl.title_xpath)[0]
                title = title.encode('utf-8')
                pub_date = item.xpath(crawl.date_xpath)[0].strip()
                pub_date = pub_date.encode('utf-8')
                chksum = get_chksum(title, url, pub_date)
                exists = check_news_exists_or_not(chksum)
                if not exists:
                    pub_date = datetime.strptime(pub_date, crawl.date_fmt)
                    gen_news(title, crawl.category, crawl.site, url, chksum, pub_date)
                else:
                    break
            except Exception, e:
                print 'error link', link
                print e
                traceback.print_exc()

if __name__ == "__main__":
    spider()
