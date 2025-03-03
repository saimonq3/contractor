from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.company.models import Company, Members
from apps.user.models import User
from .view import CompanyUpdateNameViewV1, CompanyChangeOwnerViewV1, CompanyAddMembersViewV1, \
	CompanyRemoveMembersViewV1, CompanyChangeMemberPermissionViewV1


class CompanyUpdateTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_1 = User.objects.create(username='test1', first_name='test_1', last_name='test_1')
		cls.user_2 = User.objects.create(username='test2', first_name='test_2', last_name='test_2')
		cls.user_3 = User.objects.create(username='test3', first_name='test_3', last_name='test_3')
		cls.company = Company.objects.create(
			name='name',
			owner=cls.user_1,
			created_by=cls.user_1
		)

		cls.member_1 = Members.objects.create(
			user=cls.user_1,
			is_admin=True,
			company=cls.company
		)
		cls.member_2 = Members.objects.create(
			user=cls.user_2,
			is_admin=False,
			company=cls.company
		)

	def setUp(self):
		self.factory = APIRequestFactory()

	def test_change_company_name(self):
		# Проверяем от имени администратора
		request_admin_user = self.factory.post(
			'/',
			data={'name': 'New name'},
			format='json'
		)
		request_admin_user.session = {}
		request_admin_user.user = self.user_1

		force_authenticate(request_admin_user, self.user_1)

		response_1 = CompanyUpdateNameViewV1().as_view()(request_admin_user, self.company.uuid)

		self.assertEqual(200, response_1.status_code)
		response = response_1.data

		self.company.refresh_from_db()

		# Проверяем что имя поменялось корректно
		self.assertEqual(self.company.name, 'New name')

		# Смотрим чтобы не создалось новой компании
		self.assertEqual(Company.objects.count(), 1)

		# Смотрим что вьюха вернула правильные данные
		self.assertEqual(response['result']['uuid'], str(self.company.uuid))
		self.assertEqual(response['result']['name'], self.company.name)
		self.assertEqual(response['result']['owner']['fio'], self.user_1.fio)
		self.assertEqual(
			response['result']['members'],
			[
				{'user': {'fio': self.user_1.fio}, 'is_admin': True},
				{'user': {'fio': self.user_2.fio}, 'is_admin': False},
			]
		)

	def test_change_owner(self):
		request = self.factory.post(
			'/',
			data={'user_uuid': str(self.user_2.uuid)},
			format='json'
		)
		request.session = {}
		request.user = self.user_1

		force_authenticate(request, self.user_1)

		response = CompanyChangeOwnerViewV1().as_view()(request, self.company.uuid)

		self.assertEqual(200, response.status_code)
		response = response.data

		self.company.refresh_from_db()
		self.member_1.refresh_from_db()
		self.member_2.refresh_from_db()

		self.assertEqual(self.company.owner, self.user_2)
		self.assertEqual(self.member_1.is_admin, True)

		self.assertEqual(self.member_2.is_admin, True)

		# Смотрим что вьюха вернула правильные данные
		self.assertEqual(response['result']['uuid'], str(self.company.uuid))
		self.assertEqual(response['result']['name'], self.company.name)
		self.assertEqual(response['result']['owner']['fio'], self.user_2.fio)
		self.assertEqual(
			response['result']['members'],
			[
				{'user': {'fio': self.user_1.fio}, 'is_admin': True},
				{'user': {'fio': self.user_2.fio}, 'is_admin': True},
			]
		)

	def test_add_member(self):
		request = self.factory.post(
			'/',
			data={'user_uuid': self.user_3.uuid, 'is_admin': False},
			format='json'
		)
		request.session = {}
		request.user = self.user_1

		force_authenticate(request, self.user_1)

		response = CompanyAddMembersViewV1().as_view()(request, self.company.uuid)

		self.assertEqual(200, response.status_code)
		response = response.data

		self.user_3.refresh_from_db()
		member = Members.objects.get(user=self.user_3)

		self.assertEqual(member.is_admin, False)
		self.assertEqual(Members.objects.count(), 3)

		# Смотрим что вьюха вернула правильные данные
		self.assertEqual(response['result']['uuid'], str(self.company.uuid))
		self.assertEqual(response['result']['name'], self.company.name)
		self.assertEqual(response['result']['owner']['fio'], self.user_1.fio)
		self.assertEqual(
			response['result']['members'],
			[
				{'user': {'fio': self.user_1.fio}, 'is_admin': True},
				{'user': {'fio': self.user_2.fio}, 'is_admin': False},
				{'user': {'fio': self.user_3.fio}, 'is_admin': False},
			]
		)

	def test_remove_member(self):
		request = self.factory.post(
			'/',
			data={'user_uuid': self.user_2.uuid},
			format='json'
		)
		request.session = {}
		request.user = self.user_1

		force_authenticate(request, self.user_1)

		response = CompanyRemoveMembersViewV1().as_view()(request, self.company.uuid)

		self.assertEqual(200, response.status_code)
		response = response.data

		self.assertEqual(self.company.company_members.count(), 1)
		self.assertEqual(self.company.company_members.filter(user=self.user_2).exists(), False)

		# Смотрим что вьюха вернула правильные данные
		self.assertEqual(response['result']['uuid'], str(self.company.uuid))
		self.assertEqual(response['result']['name'], self.company.name)
		self.assertEqual(response['result']['owner']['fio'], self.user_1.fio)
		self.assertEqual(
			response['result']['members'],
			[
				{'user': {'fio': self.user_1.fio}, 'is_admin': True},
			]
		)

	def test_change_permission(self):
		request = self.factory.post(
			'/',
			data={'user_uuid': self.user_2.uuid, 'is_admin': True},
			format='json'
		)
		request.session = {}
		request.user = self.user_1

		force_authenticate(request, self.user_1)

		response = CompanyChangeMemberPermissionViewV1().as_view()(request, self.company.uuid)

		self.assertEqual(200, response.status_code)
		response = response.data

		self.member_2.refresh_from_db()

		self.assertEqual(self.member_2.is_admin, True)

		# Смотрим что вьюха вернула правильные данные
		self.assertEqual(response['result']['uuid'], str(self.company.uuid))
		self.assertEqual(response['result']['name'], self.company.name)
		self.assertEqual(response['result']['owner']['fio'], self.user_1.fio)
		self.assertEqual(
			response['result']['members'],
			[
				{'user': {'fio': self.user_1.fio}, 'is_admin': True},
				{'user': {'fio': self.user_2.fio}, 'is_admin': True},
			]
		)
