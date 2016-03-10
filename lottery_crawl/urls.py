from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'list/500$', views.list_lottery_500),
    url(r'list/macau', views.list_macau_slot)
]
