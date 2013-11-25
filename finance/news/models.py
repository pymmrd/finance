# -*- coding:utf-8 -*-
from django.db import models

class CrawlSite(models.Model):
	name = models.CharField(max_length=255)
	url = models.URLField(verify_exists=False)

# Create your models here.
class NewsRule(models.Model):
	"""
	新闻规则
	"""
	site = models.ForeignKey(Site, verbose_name='收录站点')
	category = models.CharField(max_length=255, 
									blank=True,
									verbose_name=u'栏目分类')
	title_rule = models.CharField(max_length=255, 
								verbose_name=u'标题抓取规则')
	url_rule = models.CharField(max_length=255,
									verbose_name=u"抓取链接规则")
	url = models.CharField(verify_exists=False, 
								verbose_name=u'新闻链接')
	created_date = models.DateTimeField(auto_now=True)


	class Meta:
		db_table = "newsrule"
		verbose_name = "新闻抓取规则"
		verbose_name_plural = u"新闻抓取规则"

class NewsItem(models.Model):
	site = models.ForeginKey(Site, verbose_name=u'来源')
	title = models.CharField(max_length=255,
								verbose_name=u'新闻标题')
	url = models.CharField(verify_exists=False, 
								verbose_name=u'新闻链接')
	pub_date = models.DateTimeField(blank=True, verbose_name=u'新闻发布时间')

	class Meta:
		db_talbe = 'newsitem' 
		verbose_name = u'新闻'
		verbose_name_plural = u'新闻'
