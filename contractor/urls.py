from django.contrib import admin
from django.urls import path, include
from apps.user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include(user_views.urls))
]
