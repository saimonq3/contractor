from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils import api
from utils.permissions import ReadOnlyProjectPermission
from .serializers import DTODetailSerializer
from ...models import DTO


class DTODetailViewV1(APIView):
	permission_classes = [IsAuthenticated, ReadOnlyProjectPermission]

	def get(self, request, project_uuid, dto_uuid):
		try:
			dto = DTO.objects.get(project__uuid=project_uuid, uuid=dto_uuid)
		except DTO.DoesNotExist:
			return api.error_response(status=404, message='ДТО не найдено')

		serializer = DTODetailSerializer(dto)

		return api.response(serializer.data)