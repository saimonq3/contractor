from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ...models import Members, Company
from utils import api


class CompanyDeleteViewV1(APIView):
	#TODO Возможно сделать так чтобы компания и ее сотрудники не удалялись. Пока что так
	permission_classes = [IsAuthenticated, ]

	@transaction.atomic
	def delete(self, request, uuid):
		try:
			Members.objects.get(company__uuid=uuid, user=request.user, is_admin=True)
		except Members.DoesNotExist:
			return api.error_response(
				status=404,
				message='Компания не найдена или у вас нет прав на ее изменение'
			)

		Members.objects.filter(company__uuid=uuid).delete()
		Company.objects.get(uuid=uuid).delete()

		return api.response('ok')
