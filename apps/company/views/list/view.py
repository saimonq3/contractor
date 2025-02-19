from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from utils import api
from rest_framework.views import APIView

from ...models import Members, Company
from ...serializers import CompanyListSerializerV1


class CompanyListViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	@swagger_auto_schema(
	operation_description = 'Получить список компаний в которых пользователь - сотрудник',
	operation_summary = 'Получить список компаний в которых пользователь - сотрудник',
		responses={200: CompanyListSerializerV1(many=True)}
	)
	def get(self, request):
		queryset = Members.objects.filter(user=request.user).values_list('company_id', flat=True)
		company = Company.objects.filter(id__in=queryset)
		return api.response(
			CompanyListSerializerV1(company, many=True).data
		)