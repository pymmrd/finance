# -*- coding:utf-8 -*-

#StdLib imports
import os
import operator
import itertools
from datetime import datetime

#Project imports
from news.models import Site, NewsRule, NewsItem

#Django Core imports
from django.contrib import admin
from django.http import HttpResponse

admin.site.disable_action('delete_selected')

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'check_url')

    def check_url(self, obj):
        return "<a href='%s' target='_blank'>%s</a>" % (obj.url, u'点击查看')
    check_url.allow_tags = True
    check_url.short_description = '网站'

class NewsRuleAdmin(admin.ModelAdmin):
    list_display = ('site', 'category', 'xpath_prefix','title_xpath', 'url_xpath', 'date_fmt', 'date_xpath',  'url')

def get_publish_filename(filename='publish.txt'):
    now = datetime.now()
    name, ext = os.path.splitext(filename)
    filename = '%s_%s_%s_%s%s' % ( name, now.year, now.month, now.day, ext)
    return filename

def make_published(modeladmin, request, queryset):
    values = ('site__id', 'title', 'url') 
    queryset.update(is_exported=True)
    atoms = list(queryset.values_list(*values).order_by('site__id'))
    category_atom = itertools.groupby(atoms, operator.itemgetter(0)) 
    filename = get_publish_filename()
    response = HttpResponse(mimetype='text/plain')                                   
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    for site_id, value in category_atom:
        site = Site.objects.get(pk=site_id)
        site_name = site.name.encode('utf-8')
        response.write('%s%s' % (site_name, os.linesep))
        for site_pk, title, url in value:
            response.write('%s\t\t\t%s%s' % (title.encode('utf-8'), url.encode('utf-8'), os.linesep))
    return response
make_published.short_description = u"标记选中需要导出的新闻"

class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('is_exported', 'check_title',  'category', 'pub_date', 'created_date',  'site', 'summary',  'check_news', 'delete_news' )
    actions = [make_published]

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', '/static')
        js = [ static_url+'admin/js/finance.js', ]
    
    def queryset(self, request):
        qs = super(self.__class__, self).queryset(request)
        queryset = qs.filter(is_active=True)
        return queryset

    def check_news(self, obj):
        return "<a href='%s' target='_blank'>%s</a>" % (obj.url, u'点击查看')
    check_news.allow_tags = True
    check_news.short_description = '新闻链接'

    def delete_news(self, obj):
        return "<button value='%s' class='delete' type='button'>%s</button>" % (obj.pk, u'删除') 
    delete_news.allow_tags = True
    delete_news.short_description = u'删除'
    
    def check_title(self, obj):
        return "<a href='%s' target='_blank'>%s</a>" % (obj.url, obj.title)
    check_title.allow_tags = True
    check_title.short_description = '标题'

admin.site.register(Site, SiteAdmin)
admin.site.register(NewsRule, NewsRuleAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
