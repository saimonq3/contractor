from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.project.models import Project
from apps.project.serializers import ProjectDetailSerializerV1
from utils import api


class ProjectDetailViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	@swagger_auto_schema(
		operation_description='Получить детализацию проекта',
		operation_summary='Получить детализацию проекта',
		responses={200: ProjectDetailSerializerV1()}
	)
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
