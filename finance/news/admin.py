# -*- coding:utf-8 -*-

from django.contrib import admin
from news.models import Site, NewsRule, NewsItem

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'check_url')

    def check_url(self, obj):
        return "<a href='%s' target='_blank'>%s</a>" % (obj.url, u'点击查看')
    check_url.allow_tags = True
    check_url.short_description = '网站'

class NewsRuleAdmin(admin.ModelAdmin):
    list_display = ('site', 'category', 'xpath_prefix','title_xpath', 'url_xpath', 'date_fmt', 'date_xpath',  'url')

def make_published(modeladmin, request, queryset):
    queryset.update(is_exported=True)
make_published.short_description = u"标记选中需要导出的新闻"

class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('id','is_exported', 'check_title',  'category', 'pub_date', 'created_date',  'site', 'summary',  'check_news', )
    actions = [make_published]

    def check_news(self, obj):
        return "<a href='%s' target='_blank'>%s</a>" % (obj.url, u'点击查看')
    check_news.allow_tags = True
    check_news.short_description = '新闻链接'
    
    def check_title(self, obj):
        return "<a href='%s' target='_blank'>%s</a>" % (obj.url, obj.title)
    check_title.allow_tags = True
    check_title.short_description = '标题'

admin.site.register(Site, SiteAdmin)
admin.site.register(NewsRule, NewsRuleAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
