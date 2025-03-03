from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.user.models import User
from utils import api
from utils.permissions import ChangeCompanyPermission
from .serializer import CompanyUpdateQuerySerializer, CompanyMemberV1Serializer, CompanyChangeMemberV1Serializer
from ...models import Members, Company
from ...serializers import CompanyDetailSerializerV1


class CompanyUpdateNameViewV1(APIView):
	permission_classes = [IsAuthenticated, ChangeCompanyPermission]
	renderer_classes = [api.JsonRenderer, ]

	@transaction.atomic
	@swagger_auto_schema(
		request_body=CompanyUpdateQuerySerializer,
		operation_description='Изменить название компании',
		operation_summary='Изменить название компании'
	)
	def post(self, request, uuid):
		query_serializer = CompanyUpdateQuerySerializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)
		try:
			company = Company.objects.get(uuid=uuid, deleted=False)
		except Company.DoesNotExist:
			return api.error_response(status=404, message='Компания не найдена')
		company.name = request.data.get('name')
		company.save()

		return api.response(
			CompanyDetailSerializerV1(company).data
		)


class CompanyChangeOwnerViewV1(APIView):
	permission_classes = [IsAuthenticated, ChangeCompanyPermission, ]
	renderer_classes = [api.JsonRenderer, ]

	@transaction.atomic
	@swagger_auto_schema(
		request_body=CompanyMemberV1Serializer,
		operation_description='Изменить владельца компании',
		operation_summary='Изменить владельца компании'
	)
	def post(self, request, uuid):
		query_serializer = CompanyMemberV1Serializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)
		try:
			company = Company.objects.get(uuid=uuid, deleted=False)
		except Company.DoesNotExist:
			return api.error_response(status=404, message='Компания не найдена')
		try:
			new_owner = User.objects.get(uuid=request.data.get('user_uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)

		try:
			new_owner.company_members.get(company=company)
		except Members.DoesNotExist:
			return api.error_response(
				status=400,
				message=f'Пользователь {new_owner.fio} не является сотрудником компании'
			)
		company.owner = new_owner
		company.save()

		# TODO Передлать на сервис. Написать отдельный сервис для смены привелегий пользвоателя в компании
		new_owner_set_is_admin = Members.objects.get(company=company, user=new_owner)
		new_owner_set_is_admin.is_admin = True
		new_owner_set_is_admin.save()

		return api.response(
			CompanyDetailSerializerV1(company).data
		)


class CompanyAddMembersViewV1(APIView):
	permission_classes = [IsAuthenticated, ChangeCompanyPermission, ]
	renderer_classes = [api.JsonRenderer, ]

	@transaction.atomic
	@swagger_auto_schema(
		request_body=CompanyChangeMemberV1Serializer,
		operation_description='Добавить пользователя в компанию',
		operation_summary='Добавить пользователя в компанию'
	)
	def post(self, request, uuid):
		query_serializer = CompanyChangeMemberV1Serializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)

		try:
			user = User.objects.get(uuid=request.data.get('user_uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)

		try:
			company = Company.objects.get(uuid=uuid, deleted=False)
		except Company.DoesNotExist:
			return api.error_response(status=404, message='Компания не найдена')

		Members.objects.create(
			company=company,
			user=user,
			is_admin=request.data.get('is_admin')
		)

		return api.response(
			CompanyDetailSerializerV1(company).data
		)


class CompanyRemoveMembersViewV1(APIView):
	permission_classes = [IsAuthenticated, ChangeCompanyPermission, ]
	renderer_classes = [api.JsonRenderer, ]

	@transaction.atomic
	@swagger_auto_schema(
		request_body=CompanyChangeMemberV1Serializer,
		operation_description='Убрать пользователя из компании',
		operation_summary='Убрать пользователя из компании'
	)
	def post(self, request, uuid):
		query_serializer = CompanyChangeMemberV1Serializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)

		try:
			user = User.objects.get(uuid=request.data.get('user_uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)

		try:
			company = Company.objects.get(uuid=uuid, deleted=False)
		except Company.DoesNotExist:
			return api.error_response(status=404, message='Компания не найдена')

		if user == Members.objects.get(user=request.user, company=company).user:
			return api.error_response(
				status=404,
				message='Польователь не может удалить сам себя'
			)

		try:
			Members.objects.get(user=user, company=company).delete()
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не является сотрудником компании'
			)

		return api.response(
			CompanyDetailSerializerV1(company).data
		)


class CompanyChangeMemberPermissionViewV1(APIView):
	permission_classes = [IsAuthenticated, ChangeCompanyPermission, ]
	renderer_classes = [api.JsonRenderer, ]

	@transaction.atomic
	@swagger_auto_schema(
		request_body=CompanyChangeMemberV1Serializer,
		operation_description='Изменить права пользователя в компании',
		operation_summary='Изменить права пользователя в компании'
	)
	def post(self, request, uuid):
		query_serializer = CompanyChangeMemberV1Serializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)

		try:
			user = User.objects.get(uuid=request.data.get('user_uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)

		try:
			company = Company.objects.get(uuid=uuid, deleted=False)
		except Company.DoesNotExist:
			return api.error_response(status=404, message='Компания не найдена')

		try:
			member = Members.objects.get(user=user, company=company)
			member.is_admin = request.data.get('is_admin')
			member.save()
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не является сотрудником компании'
			)

		return api.response(
			CompanyDetailSerializerV1(company).data
		)
