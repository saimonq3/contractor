from django.urls import path

from .list import company_list_v1
from .detail import company_detail_v1
from .create import company_create
from .update import company_update_name_v1, company_update_owner_v1

urlpatterns = [
	path('list/', company_list_v1.as_view()),
	path('detail/<uuid>/', company_detail_v1.as_view()),
	path('create/', company_create.as_view()),
	path('update_name/<uuid>/', company_update_name_v1.as_view()),
	path('update_owner/<uuid>/', company_update_owner_v1.as_view()),
]
