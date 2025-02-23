from rest_framework.test import APITestCase, APIRequestFactory


class CompanyCreateTest(APITestCase):

	def setUp(self):
		self.factory = APIRequestFactory()