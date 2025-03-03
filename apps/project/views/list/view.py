from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ...models import Members, Project
from utils import api
from ...serializers import ProjectDetailSerializerV1


class ProjectListViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	@swagger_auto_schema(
		operation_description='Получить список проектов в которых учавствует пользователь',
		operation_summary='Получить список проектов в которых учавствует пользователь',
		responses={200: ProjectDetailSerializerV1(many=True)}
	)
	def get(self, request):
		company_uuid = request.query_params.get('company_uuid')
		projects_ids = (
			Members.objects.filter(user=request.user, project__company__uuid=company_uuid)
			.distinct('project')
			.values_list('project_id', flat=True)
		)
		projects = Project.objects.filter(id__in=projects_ids, company__deleted=False)

		return api.response(
			ProjectDetailSerializerV1(projects, many=True).data
		)
