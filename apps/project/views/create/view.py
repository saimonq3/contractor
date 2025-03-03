from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.company.models import Members as CompanyMembers
from utils import api
from utils.models import normalize_base_url
from .serializers import ProjectCreateV1RequestQuery
from ...models import Project, Members as ProjectMembers
from ...serializers import ProjectDetailSerializerV1


class ProjectCreateViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	@transaction.atomic
	@swagger_auto_schema(
		request_body=ProjectCreateV1RequestQuery,
		operation_description='Создать проект',
		operation_summary='Создать проект',
		responses={200: ProjectDetailSerializerV1()}
	)
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
			base_url=normalize_base_url(request.data.get('base_url')),
			created_by=request.user
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
			ProjectDetailSerializerV1(project).data
		)
