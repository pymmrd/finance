# -*- coding:utf-8 -*-
from django.db import models

class Site(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(verify_exists=False)

    class Meta:
        db_table = 'site'
        verbose_name = u'站点'
        verbose_name_plural = u'站点'
    
    def __unicode__(self):
        return self.name

# Create your models here.
class NewsRule(models.Model):
    """
    新闻规则
    """
    site = models.ForeignKey(Site, verbose_name='收录站点')
    category = models.CharField(max_length=255, 
                                    blank=True,
                                    verbose_name=u'栏目分类')
    xpath_prefix = models.CharField(max_length=255, 
                                    blank=True,
                                    verbose_name=u'xpath前缀')
    title_xpath = models.CharField(max_length=255, 
                                verbose_name=u'标题抓取规则')
    url_xpath = models.CharField(max_length=255,
                                    verbose_name=u"抓取链接规则")
    url = models.URLField(verify_exists=False, 
                                verbose_name=u'抓取页面')
    date_fmt = models.CharField(max_length=50,
                                verbose_name=u'日期格式')
    date_xpath = models.CharField(max_length=255,
                                verbose_name=u'日期规则')
    created_date = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "newsrule"
        verbose_name = "新闻抓取规则"
        verbose_name_plural = u"新闻抓取规则"

class NewsItem(models.Model):
    site = models.ForeignKey(Site, verbose_name=u'来源')
    category = models.CharField(max_length=255, 
                                    blank=True,
                                    verbose_name=u'栏目分类')
    title = models.CharField(max_length=255,
                                verbose_name=u'新闻标题')
    url = models.URLField(verify_exists=False, 
                                verbose_name=u'新闻链接')
    pub_date = models.DateTimeField(blank=True, verbose_name=u'新闻发布时间')
    chksum = models.CharField(max_length=64, db_index=True)
    summary = models.TextField(blank=True, verbose_name=u'摘要')
    is_exported = models.BooleanField(default=False, verbose_name=u'是否导出')
    created_date = models.DateTimeField(auto_now=True,verbose_name=u'爬虫抓取时间')
    is_active = models.BooleanField(default=True, verbose_name=u'是否激活')

    class Meta:
        db_table = 'newsitem' 
        verbose_name = u'新闻'
        verbose_name_plural = u'新闻'
        ordering = ['-pub_date']
