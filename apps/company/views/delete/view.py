from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.project.models import Project
from utils.permissions import ChangeCompanyPermission
from ...models import Members, Company
from utils import api


class CompanyDeleteViewV1(APIView):
	#TODO Возможно сделать так чтобы компания и ее сотрудники не удалялись, а убирались в архив. Пока что так
	permission_classes = [IsAuthenticated, ChangeCompanyPermission]
	renderer_classes = [api.JsonRenderer, ]

	@transaction.atomic
	def delete(self, request, uuid):
		try:
			company = Company.objects.get(uuid=uuid)
		except Company.DoesNotExist:
			return api.error_response(status=404, message='Компания не найдена')
		company.deleted = True
		company.save()

		return api.response('ok')
