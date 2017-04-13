

#---------------class-based view's url mapping------------

from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import (
					LikeToggleAPIView,
					RetweetAPIView,
					TweetCreateAPIView,
					TweetListAPIView,
					TweetDetailAPIView,
					)

urlpatterns = [
#	url(r'^$', RedirectView.as_view(url="/")), # redirect from /tweet/ to /
	url(r'^$', TweetListAPIView.as_view(), name='list'), # /api/tweet/
	url(r'^create/$', TweetCreateAPIView.as_view(), name='create'), # /api/tweet/create/
	url(r'^(?P<pk>\d+)/$', TweetDetailAPIView.as_view(), name='detail'), # /api/tweet/id/
	url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'), # /api/tweet/id/like/
	url(r'^(?P<pk>\d+)/retweet/$', RetweetAPIView.as_view(), name='retweet'), # /api/tweet/id/retweet/
#	url(r'^(?P<pk>\d+)/$', TweetDetailView.as_view(), name='detail'), # /tweet/1/
#	url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'), # /tweet/1/update/
#	url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete'), # /tweet/1/delete/

]

#---------------function-based view's url mapping----------

#from django.conf.urls import url
#from .views import tweet_detail_view, tweet_list_view

#urlpatterns = [
#    url(r'^$', tweet_list_view, name='list'),
#    url(r'^(?P<pk>\d+)/$', tweet_detail_view, name="detail"),
#]
