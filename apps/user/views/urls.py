from django.urls import path
from .register import register_v1
from .login import login_v1
from .get import find_users_v1
from .update import update_user_v1
from .profile import user_profile_v1


urlpatterns = [
	path('register/', register_v1.as_view()),
	path('login/', login_v1.as_view()),
	path('find/', find_users_v1.as_view()),
	path('update/<str:uuid>/', update_user_v1.as_view()),
	path('profile/', user_profile_v1.as_view())
]