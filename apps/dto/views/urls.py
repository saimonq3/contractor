from django.urls import path
from .list import list_dto_v1
from .detail import dto_detail_v1

urlpatterns = [
	path('list/v1/', list_dto_v1.as_view()),
	path('detail/<project_uuid>/<dto_uuid>/v1/', dto_detail_v1.as_view()),
]