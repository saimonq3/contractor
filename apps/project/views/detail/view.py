from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.project.models import Members, Project
from utils import api


class ProjectDetailViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def get(self, request, uuid):
		try:
			project = Project.objects.get(uuid=uuid)
		except Project.DoesNotExist:
			return api.error_response(
				status=404,
				message='Проект не найден'
			)
		project_members = (
			Members.objects
			.filter(project=project)
			.order_by('-is_admin', 'user__first_name', 'user__last_name')
			.select_related('user')
		)

		return api.response(
			{
				'uuid': project.uuid,
				'name': project.name,
				'description': project.description,
				'owner': project.owner.fio,
				'company': project.company.name,
				'base_url': project.base_url,
				'members': [
					{
						'user': member.user.fio,
						'is_admin': member.is_admin
					}
					for member in project_members
				]
			}
		)
