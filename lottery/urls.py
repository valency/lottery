from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^alias/', include('lottery_alias.urls')),
    url(r'^market/', include('lottery_market.urls')),
    url(r'^market/asian/', include('lottery_market_asian.urls'))
]
