from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils import api
from utils.permissions import ChangeProjectPermission
from ...models import Project


class DeleteProjectV1(APIView):
	permission_classes = [IsAuthenticated, ChangeProjectPermission]

	def delete(self, request, uuid):
		try:
			Project.objects.get(uuid=uuid).delete()
		except Project.DoesNotExist:
			return api.error_response(status=404, message='Проект не найден')
		return api.response('ok')

