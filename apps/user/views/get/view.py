from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils import api
from .schema import UserListSchema
from ...models import User


class FindUserV1(APIView):
	permission_classes = [IsAuthenticated, ]

	@swagger_auto_schema(**UserListSchema)
	def get(self, request):
		request_query = request.query_params.get('query')
		query = Q(email=request_query)
		query.add(Q(username__icontains=request_query), Q.OR)
		users = User.objects.filter(query)

		return api.response(
			[
				{
					'uuid': user.uuid,
					'username': user.username,
					# 'avatar': user.avatar
				} for user in users
			]
		)
