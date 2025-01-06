from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.user.models import User
from ...models import Members
from .serializer import CompanyUpdateQuerySerializer, CompanyChangeOwnerQuerySerializer
from utils import api


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
			{
				'uuid': company.uuid,
				'name': company.name,
				'owner': company.owner.fio if company.owner else '',
				'members': [
					{
						'name': member.user.fio,
						'is_admin': member.is_admin
					}
					for member in company.company_members.all()
				]
			}
		)


class CompanyChangeOwnerViewV1(APIView):
	permission_classes = [IsAuthenticated, ]

	@transaction.atomic
	def post(self, request, uuid):
		query_serializer = CompanyChangeOwnerQuerySerializer(data=request.data)
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
			{
				'uuid': company.uuid,
				'name': company.name,
				'owner': company.owner.fio if company.owner else '',
				'members': [
					{
						'name': member.user.fio,
						'is_admin': member.is_admin
					}
					for member in company.company_members.all()
				]
			}
		)


class CompanyAddMembersViewV1(APIView):
	permission_classes = [IsAuthenticated, ]


class CompanyRemoveMembersViewV1(APIView):
	permission_classes = [IsAuthenticated, ]