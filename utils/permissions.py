from rest_framework.permissions import BasePermission

from apps.project.models import Members as ProjectMembers
from apps.company.models import Members as CompanyMembers

def pars_data(data):
	result = {}
	for key, value in data.items():
		if key.endswith('uuid'):
			result[key] = value
	return result


def find_uuid(request):
	"""
	Поиск uuid`а в реквесте
	Он может быть как в теле запроса, так и квери параметре, так и в урле
	"""
	request_kwargs = pars_data(request.parser_context['kwargs'])
	query_params = pars_data(request.query_params)
	data = pars_data(request.data)
	return request_kwargs|query_params|data


class ReadOnlyCompanyPermission(BasePermission):
	def has_permission(self, request, view):
		uuid = find_uuid(request)
		try:
			CompanyMembers.objects.get(company__uuid=uuid.get('company_uuid'), user=request.user)
			return True
		except CompanyMembers.DoesNotExist:
			return False


class ChangeCompanyPermission(BasePermission):
	def has_permission(self, request, view):
		uuid = find_uuid(request)
		try:
			CompanyMembers.objects.get(company__uuid=uuid.get('company_uuid'), user=request.user, is_admin=True)
			return True
		except CompanyMembers.DoesNotExist:
			return False


class ReadOnlyProjectPermission(BasePermission):
	def has_permission(self, request, view):
		uuid = find_uuid(request)
		try:
			ProjectMembers.objects.get(project__uuid=uuid.get('project_uuid'), user=request.user)
			return True
		except ProjectMembers.DoesNotExist:
			return False


class ChangeProjectPermission(BasePermission):
	def has_permission(self, request, view):
		uuid = find_uuid(request)
		try:
			ProjectMembers.objects.get(project__uuid=uuid.get('project_uuid'), user=request.user, is_admin=True)
			return True
		except ProjectMembers.DoesNotExist:
			return False