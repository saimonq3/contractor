from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils import api
from utils.permissions import ReadOnlyCompanyPermission
from ...models import Company
from ...serializers import CompanyDetailSerializerV1


class CompanyDetailViewV1(APIView):
	permission_classes = [IsAuthenticated, ReadOnlyCompanyPermission, ]
	renderer_classes = [api.JsonRenderer, ]

	@swagger_auto_schema(
		operation_description='Инофрмация по компании',
		operation_summary='Информация по компании',
		responses={200: CompanyDetailSerializerV1()}
	)
	def get(self, request, uuid):
		try:
			company = Company.objects.get(uuid=uuid, deleted=False)
		except Company.DoesNotExist:
			return api.error_response(message='Компания не найдена', status=404)

		return api.response(
			CompanyDetailSerializerV1(company).data
		)
