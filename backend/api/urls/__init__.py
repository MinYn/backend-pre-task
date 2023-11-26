from django.conf.urls import url, include

urlpatterns = [
    url(r'^v1/', include(('api.urls.v1', 'api_v1'), namespace='api_v1')),
]
