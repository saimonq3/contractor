from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from utils import api
from .serializer import CompanyCreateV1RequestQuery, CompanyCreateSerializerV1
from ...models import Company, Members


class CompanyCreateViewV1(GenericAPIView):
	permission_classes = [IsAuthenticated, ]
	renderer_classes = [api.JsonRenderer]
	serializer_class = CompanyCreateV1RequestQuery

	@transaction.atomic
	@swagger_auto_schema(
		request_body=CompanyCreateV1RequestQuery,
		operation_description='Создать команию',
		operation_summary='Создать компанию',
		responses={200: CompanyCreateSerializerV1()}
	)
	def post(self, request):
		check_request_query = self.serializer_class(data=request.data)
		if not check_request_query.is_valid():
			return api.error_response(
				status=400,
				message=str(check_request_query.errors)
			)

		# В случае если пользователь пытается создать компанию которая уже есть, то вернем ее без ошибок
		company, added = Company.objects.get_or_create(
			name=request.data.get('name'),
			owner=request.user,
			created_by=request.user
		)

		# Сразу назначаем пользователя сотрудником и даем ему админа
		if added:
			Members.objects.create(
				company=company,
				user=request.user,
				is_admin=True
			)

		serializer = CompanyCreateSerializerV1(company)
		return api.response(
			serializer.data
		)