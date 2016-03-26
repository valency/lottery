from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'alias/list$', views.list_alias),
    url(r'alias/add$', views.add_alias),
    url(r'alias/delete$', views.delete_alias),
    url(r'list/500$', views.list_lottery_500),
    url(r'list/hkjc$', views.list_hkjc),
    url(r'list/macau$', views.list_macau_slot)
]
