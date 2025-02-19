from rest_framework.permissions import IsAuthenticated
from utils import api
from rest_framework.views import APIView

from ...models import Members, Company
from ...serializers import CompanyDetailSerializerV1


class CompanyListViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def get(self, request):
		queryset = Members.objects.filter(user=request.user).values_list('company_id', flat=True)
		company = Company.objects.filter(id__in=queryset)
		return api.response(
			CompanyDetailSerializerV1(company, many=True).data
		)