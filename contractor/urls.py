from django.contrib import admin
from django.urls import path, include
from apps.user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include(user_views.urls)),
    path('api/pact/', include('apps.pact.urls')),
    path('api/company/', include('apps.company.urls')),
    path('api/project/', include('apps.project.urls')),
    path('api/dto/', include('apps.dto.urls')),

]
