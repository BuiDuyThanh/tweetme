

#---------------class-based view's url mapping------------

from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import (
		RetweetView, 
		TweetListView, 
		TweetDetailView, 
		TweetCreateView, 
		TweetUpdateView, 
		TweetDeleteView,
		)

urlpatterns = [
	url(r'^$', RedirectView.as_view(url="/")), # redirect from /tweet/ to /
	url(r'^search/$', TweetListView.as_view(), name='list'), # /tweet/
	url(r'^create/$', TweetCreateView.as_view(), name='create'), # /tweet/create/
	url(r'^(?P<pk>\d+)/$', TweetDetailView.as_view(), name='detail'), # /tweet/1/
	url(r'^(?P<pk>\d+)/retweet/$', RetweetView.as_view(), name='detail'), # /tweet/1/
	url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'), # /tweet/1/update/
	url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete'), # /tweet/1/delete/

]

#---------------function-based view's url mapping----------

#from django.conf.urls import url
#from .views import tweet_detail_view, tweet_list_view

#urlpatterns = [
#    url(r'^$', tweet_list_view, name='list'),
#    url(r'^(?P<pk>\d+)/$', tweet_detail_view, name="detail"),
#]
