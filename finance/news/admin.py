# -*- coding:utf-8 -*-

from django.contrib import admin
from news.models import Site, NewsRule, NewsItem

class SiteAdmin(admin.ModelAdmin):
	list_display = ('name', 'url')

class NewsRuleAdmin(admin.ModelAdmin):
	list_display = ('site', 'category', 'xpath_prefix','title_xpath', 'url_xpath', 'date_fmt', 'date_xpath',  'url')

class NewsItemAdmin(admin.ModelAdmin):
	list_display = ('site', 'title', 'url', 'pub_date', 'created_date')

admin.site.register(Site, SiteAdmin)
admin.site.register(NewsRule, NewsRuleAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
