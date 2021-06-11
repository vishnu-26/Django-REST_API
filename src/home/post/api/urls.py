from django.conf.urls import url

from .views import BlogPostRudView,BlogPostAPIView
urlpatterns=[
    url(r'^$',BlogPostAPIView.as_view(),name='post-listcreate'),
    url(r'^(?P<pk>\d+)/$',BlogPostRudView.as_view(),name='post-rud')
#    url(r'^all/',BlogPostListView.as_view(),name='post-list')
]
