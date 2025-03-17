from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from ...models import Company, Members
from .view import CompanyDeleteViewV1
from apps.user.models import User


class CompanyDeleteTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		cls.user_1 = User.objects.create(username='test_1')
		cls.user_2 = User.objects.create(username='test_2')
		cls.company_1 = Company.objects.create(name='test_1', created_by=cls.user_1, owner=cls.user_1)
		cls.company_2 = Company.objects.create(name='test_2', created_by=cls.user_1, owner=cls.user_1)
		cls.member = Members.objects.create(company=cls.company_1, user=cls.user_1, is_admin=True)
		cls.member = Members.objects.create(company=cls.company_1, user=cls.user_2, is_admin=False)

		cls.member = Members.objects.create(company=cls.company_2, user=cls.user_1, is_admin=True)

	def setUp(self):
		self.factory = APIRequestFactory()

	def test_success_delete(self):
		request = self.factory.delete(
			'/'
		)
		request.session = {}
		request.user = self.user_1

		force_authenticate(request, self.user_1)

		response = CompanyDeleteViewV1().as_view()(request, company_uuid=str(self.company_1.uuid))

		self.assertEqual(200, response.status_code)
		response = response.data

		self.assertEqual(response['results'], 'ok')
		self.assertEqual(Company.objects.filter(deleted=False).count(), 1)
		self.assertEqual(Company.objects.filter(uuid=self.company_1.uuid, deleted=False).exists(), False)

	def test_fail_delete(self):
		request = self.factory.delete(
			'/'
		)
		request.session = {}
		request.user = self.user_2

		force_authenticate(request, self.user_2)

		response = CompanyDeleteViewV1().as_view()(request, company_uuid=str(self.company_1.uuid))

		self.assertEqual(403, response.status_code)

		self.assertEqual(Company.objects.count(), 2)
		self.assertEqual(Company.objects.filter(uuid=self.company_1.uuid).exists(), True)

	def test_fail_delete_by_not_member(self):
		request = self.factory.delete(
			'/'
		)
		request.session = {}
		request.user = self.user_2

		force_authenticate(request, self.user_2)

		response = CompanyDeleteViewV1().as_view()(request, company_uuid=str(self.company_2.uuid))

		self.assertEqual(403, response.status_code)

		self.assertEqual(Company.objects.count(), 2)
		self.assertEqual(Company.objects.filter(uuid=self.company_1.uuid).exists(), True)