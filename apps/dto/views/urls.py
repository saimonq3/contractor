from django.urls import path
from .list import list_dto_v1

urlpatterns = [
	path('list/v1/', list_dto_v1.as_view()),
]