from django.urls import path
from .register import register_v1
from .login import login_v1
from .get import find_users_v1


urlpatterns = [
	path('register/', register_v1.as_view()),
	path('login/', login_v1.as_view()),
	path('find/', find_users_v1.as_view()),
]