from django.conf.urls.static import static
from . import settings
from django.contrib import admin
from django.urls import path, include
from apps.user import views as user_views
from apps.company import views as company_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include(user_views.urls)),
    path('api/pact/', include('apps.pact.urls')),
    path('api/company/', include(company_view.urls)),
    path('api/project/', include('apps.project.views.urls')),
    path('api/dto/', include('apps.dto.views.urls')),
    path('explorer/', include('explorer.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

