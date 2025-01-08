from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ...models import Members
from utils import api


class ProjectListViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def get(self, request):
		company_uuid = request.query_params.get('company')
		projects_member = (
			Members.objects.filter(user=request.user, project__company__uuid=company_uuid)
			.distinct('project')
			.select_related('project', 'project__company', 'user')
		)

		return api.response(
			[
				{
					'uuid': member.project.uuid,
					'name': member.project.name,
					'description': member.project.description,
					'is_admin': member.is_admin,
					'company': {
						'uuid': member.project.company.uuid,
						'name': member.project.company.name
					},
					'count_members': member.project.project_members.count()
				}
				for member in projects_member
			]
		)
