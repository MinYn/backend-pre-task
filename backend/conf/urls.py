from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url('', include('api.urls')),
]