from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.company.models import Company, Members
from apps.user.models import User
from .view import CompanyListViewV1


class CompanyListTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_1 = User.objects.create(username='test1')
		cls.user_2 = User.objects.create(username='test2')
		cls.company_1 = Company.objects.create(
			name='test_company_1',
			owner=cls.user_1,
			created_by=cls.user_1
		)
		cls.company_2 = Company.objects.create(
			name='test_company_2',
			owner=cls.user_2,
			created_by=cls.user_2
		)
		cls.company_3 = Company.objects.create(
			name='test_company_3',
			owner=cls.user_2,
			created_by=cls.user_2
		)
		cls.members = Members.objects.create(
			user=cls.user_1,
			is_admin=True,
			company=cls.company_1
		)
		cls.members = Members.objects.create(
			user=cls.user_1,
			is_admin=True,
			company=cls.company_2
		)
		cls.members = Members.objects.create(
			user=cls.user_2,
			is_admin=True,
			company=cls.company_3
		)

	def setUp(self):
		self.factory = APIRequestFactory()

	def test_company_list(self):
		request = self.factory.get('/')
		request.session = {}
		request.user = self.user_1

		force_authenticate(request, self.user_1)

		response = CompanyListViewV1().as_view()(request)

		self.assertEqual(200, response.status_code)
		response = response.data

		self.assertEqual(len(response['results']), 2)
		self.assertEqual(response['results'][1]['name'], self.company_1.name)
		self.assertEqual(response['results'][0]['name'], self.company_2.name)
		self.assertEqual(response['results'][1]['owner']['fio'], self.user_1.fio)
		self.assertEqual(response['results'][0]['owner']['fio'], self.user_2.fio)
