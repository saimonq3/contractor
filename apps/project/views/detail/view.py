from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.project.models import Members, Project
from apps.project.serializers import ProjectDetailSerializerV1
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

		return api.response(
			ProjectDetailSerializerV1(project).data
		)
