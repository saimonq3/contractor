from django.urls import path

from .create import company_create_v1
from .detail import company_detail_v1
from .list import company_list_v1
from .delete import delete_company_v1
from .update import company_update_name_v1, company_update_owner_v1, company_add_member_v1, company_remove_member_v1, \
	company_member_change_permission_v1

urlpatterns = [
	path('list/v1/', company_list_v1.as_view()),
	path('detail/<company_uuid>/v1/', company_detail_v1.as_view()),
	path('create/v1/', company_create_v1.as_view()),
	path('update_name/<company_uuid>/v1/', company_update_name_v1.as_view()),
	path('update_owner/<company_uuid>/v1/', company_update_owner_v1.as_view()),
	path('add_member/<company_uuid>/v1/', company_add_member_v1.as_view()),
	path('remove_member/<company_uuid>/v1/', company_remove_member_v1.as_view()),
	path('remove/<company_uuid>/v1/', delete_company_v1.as_view()),
	path('change_member_permission/<company_uuid>/v1/', company_member_change_permission_v1.as_view()),
]
