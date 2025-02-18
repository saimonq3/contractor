from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.user.models import User
from utils import api
from .serializer import CompanyUpdateQuerySerializer, CompanyMemberV1Serializer, CompanyChangeMemberV1Serializer
from ...models import Members
from ...serializers import CompanyDetailSerializerV1


class CompanyUpdateNameViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	@transaction.atomic
	def post(self, request, uuid):
		query_serializer = CompanyUpdateQuerySerializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)

		try:
			company_admin = Members.objects.get(company__uuid=uuid, user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Компания не найдена или у вас нет прав на ее изменение'
			)

		company = company_admin.company
		company.name = request.data.get('name')
		company.save()

		return api.response(
			CompanyDetailSerializerV1(company).data
		)


class CompanyChangeOwnerViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	@transaction.atomic
	def post(self, request, uuid):
		query_serializer = CompanyMemberV1Serializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)

		try:
			company_admin = Members.objects.get(company__uuid=uuid, user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Компания не найдена или у вас нет прав на ее изменение'
			)

		company = company_admin.company
		try:
			new_owner = User.objects.get(uuid=request.data.get('user'))
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

		return api.response(
			CompanyDetailSerializerV1(company).data
		)


class CompanyAddMembersViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request, uuid):
		query_serializer = CompanyChangeMemberV1Serializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)

		try:
			company_admin = Members.objects.get(company__uuid=uuid, user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Компания не найдена или у вас нет прав на ее изменение'
			)

		try:
			user = User.objects.get(uuid=request.data.get('uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)

		company = company_admin.company

		Members.objects.create(
			company=company,
			user=user,
			is_admin=request.data.get('is_admin')
		)

		return api.response(
			CompanyDetailSerializerV1(company).data
		)


class CompanyRemoveMembersViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	def post(self, request, uuid):
		query_serializer = CompanyChangeMemberV1Serializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)

		try:
			company_admin = Members.objects.get(company__uuid=uuid, user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Компания не найдена или у вас нет прав на ее изменение'
			)

		try:
			user = User.objects.get(uuid=request.data.get('uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)

		if user == company_admin.user:
			return api.error_response(
				status=404,
				message='Польователь не может удалить сам себя'
			)

		company = company_admin.company

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
	permission_classes = [IsAuthenticated, ]

	def post(self, request, uuid):
		query_serializer = CompanyChangeMemberV1Serializer(data=request.data)
		if not query_serializer.is_valid():
			return api.error_response(
				status=400,
				message=str(query_serializer.errors)
			)

		try:
			company_admin = Members.objects.get(company__uuid=uuid, user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Компания не найдена или у вас нет прав на ее изменение'
			)

		try:
			user = User.objects.get(uuid=request.data.get('uuid'))
		except User.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не найден'
			)

		company = company_admin.company

		try:
			member = Members.objects.get(user=user, company=company)
			member.is_admin = request.data.get('is_admin')
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Пользователь не является сотрудником компании'
			)

		return api.response(
			CompanyDetailSerializerV1(company).data
		)