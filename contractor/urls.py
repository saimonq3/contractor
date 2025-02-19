from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import settings
from django.contrib import admin
from django.urls import path, include
from apps.user import views as user_views
from apps.company import views as company_view

schema_view = get_schema_view(
	openapi.Info(
		title="API",
		default_version='v1',
		description="API contractor",
		contact=openapi.Contact(url="https://t.me/Saimonq3", name='Семен Иванов'),
		license=openapi.License(name=""),
	),
	public=True,
	permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('docs/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/account/', include(user_views.urls)),
    path('api/pact/', include('apps.pact.urls')),
    path('api/company/', include(company_view.urls)),
    path('api/project/', include('apps.project.views.urls')),
    path('api/dto/', include('apps.dto.views.urls')),
    path('explorer/', include('explorer.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

