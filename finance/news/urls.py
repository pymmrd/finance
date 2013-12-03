from django.conf.urls import patterns, include, url

urlpatterns = patterns('news.views',
    (r'^delete/$', 'delete_news'),
)
