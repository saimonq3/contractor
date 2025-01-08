from django.urls import path

from .create import project_create_v1
from .list import project_list_v1
from .detail import project_detail_v1
from .update import project_add_member_v1, project_remove_member_v1, project_change_member_permission_v1, \
	project_change_owner_v1, project_change_company_v1, project_update_info_v1

urlpatterns = [
	path('create/<company_uuid>/v1/', project_create_v1.as_view()),
	path('list/v1/', project_list_v1.as_view()),
	path('detail/<uuid>/v1/', project_detail_v1.as_view()),
	path('add_member/<project_uuid>/v1/', project_add_member_v1.as_view()),
	path('remove_member/<project_uuid>/v1/', project_remove_member_v1.as_view()),
	path('member_permission/<project_uuid>/v1/', project_change_member_permission_v1.as_view()),
	path('change_owner/<project_uuid>/v1/', project_change_owner_v1.as_view()),
	path('change_company/<project_uuid>/v1/', project_change_company_v1.as_view()),
	path('update_info/<project_uuid>/v1/', project_update_info_v1.as_view()),


]
