from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'query/$', views.query),
    url(r'crawl/$', views.crawl),
    url(r'search/$', views.search)
]
