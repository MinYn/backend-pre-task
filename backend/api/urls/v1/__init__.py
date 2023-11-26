from django.urls import path
from django.conf.urls import url, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter

from api.contacts.views.contacts import ContactsViewSet, LabelViewSet

version = 'v1'

schema_url_patterns = [
    path(f'{version}/', include(f'api.urls.{version}')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="연락처 API",
        default_version=f'{version}',
        description="연락처 API 입니다.",
        contact=openapi.Contact(email="ysmysm3@naver.com"),
        license=openapi.License(name="윤석민"),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)/$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name=f'schema-swagger-ui{version}'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name=f'schema-redoc-{version}'),
]

router = SimpleRouter()

router.register(r'contacts', ContactsViewSet, basename='contacts')
router.register(r'label', LabelViewSet, basename='label')

urlpatterns += router.urls