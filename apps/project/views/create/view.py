from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.company.models import Members as CompanyMembers
from utils.models import normalize_base_url
from ...models import Project, Members as ProjectMembers
from .serializers import ProjectCreateV1RequestQuery
from utils import api


class ProjectCreateViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	@transaction.atomic
	def post(self, request, company_uuid):
		check_request_query = ProjectCreateV1RequestQuery(data=request.data)
		if not check_request_query.is_valid():
			return api.error_response(
				status=400,
				message=str(check_request_query.errors)
			)

		try:
			company_admin = CompanyMembers.objects.get(user=request.user, company__uuid=company_uuid)
		except CompanyMembers.DoesNotExist:
			return api.error_response(
				status=403,
				message='Пользавтель не является администратором компании'
			)

		company = company_admin.company

		project = Project.objects.create(
			name=request.data.get('name'),
			description=request.data.get('description'),
			owner=request.user,
			company=company,
			base_url=normalize_base_url(request.data.get('base_url'))
		)

		ProjectMembers.objects.create(
			project=project,
			user=request.user,
			is_admin=True
		)

		if request.data.get('add_company_members'):
			members = company.company_members.exclude(user=request.user)
			project_members = [member.user for member in members]

			ProjectMembers.objects.bulk_create(
				ProjectMembers(
					project=project,
					user=user
				) for user in project_members
			)

		return api.response(
			{
				'uuid': project.uuid,
				'name': project.name,
				'description': project.description,
				'owner': project.owner.fio,
				'company': {
					'name': company.name,
					'uuid': company.uuid
				},
				'count_members': project.project_members.count()
			}
		)