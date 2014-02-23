from django.conf.urls import patterns, include, url

urlpatterns = patterns('stopviolence.views',
    url('^(?P<theme>[a-zA-Z]+)/ask', 'index',),
    url('^(?P<theme>[a-zA-Z]+)', 'result',),
)
