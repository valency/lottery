from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'query/$', views.market),
    url(r'list/five/$', views.five),
    url(r'list/hkjc/$', views.hkjc),
    url(r'list/betfair/$', views.betfair)
]
