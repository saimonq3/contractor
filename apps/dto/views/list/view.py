from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated

from utils import api
from utils.permissions import ReadOnlyProjectPermission
from ...models import DTO
from .serializers import DTOSerializerV1


class DTOCursorPagination(CursorPagination):
	page_size = 20
	ordering = 'id'

class ListDTOV1View(ListAPIView):
	permission_classes = [IsAuthenticated, ReadOnlyProjectPermission, ]
	queryset = DTO.objects.all()
	serializer_class = DTOSerializerV1
	pagination_class = DTOCursorPagination
	renderer_classes = [api.JsonRenderer, ]

	@swagger_auto_schema(
		manual_parameters=[
			openapi.Parameter(
				'name',
				in_=openapi.IN_QUERY,
				type=openapi.TYPE_STRING,
				description='Имя ДТО',
				required=False,
			),
			openapi.Parameter(
				'project_uuid',
				in_=openapi.IN_QUERY,
				type=openapi.TYPE_STRING,
				description='UUID проекта',
				required=True,
			),
		]
	)
	def get(self, request, *args, **kwargs):
		request_project_uuid = self.request.query_params.get('project_uuid')
		if not request_project_uuid:
			return api.error_response(status=400, message='project_uuid обязательный параметр запроса')
		return super().get(request, *args, **kwargs)

	def get_queryset(self):
		request_project_uuid = self.request.query_params.get('project_uuid')
		dtos = DTO.objects.filter(project__uuid=request_project_uuid).select_related('project')

		if name := self.request.query_params.get('name'):
			dtos = dtos.filter(name=name)

		return dtos

