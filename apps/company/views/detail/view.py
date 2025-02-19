from rest_framework.permissions import IsAuthenticated
from utils import api
from rest_framework.views import APIView

from ...serializers import CompanyDetailSerializerV1
from ...models import Company


class CompanyDetailViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def get(self, request, uuid):
		try:
			company = Company.objects.get(uuid=uuid)
		except Company.DoesNotExist:
			return api.error_response(message='Компания не найдена', status=404)

		return api.response(
			CompanyDetailSerializerV1(company).data
		)