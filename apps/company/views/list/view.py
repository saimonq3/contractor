from rest_framework.permissions import IsAuthenticated
from utils import api
from rest_framework.views import APIView

from ...models import Members
from .serializer import CompanyListSerializerV1


class CompanyListViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def get(self, request):
		queryset = Members.objects.filter(user=request.user).select_related('company')
		serializer = CompanyListSerializerV1(queryset, many=True)
		return api.response(serializer.data)