from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'list/$', views.list_alias),
    url(r'add/$', views.add_alias),
    url(r'delete/$', views.delete_alias)
]
