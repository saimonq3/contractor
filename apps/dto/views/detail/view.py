from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils import api
from utils.permissions import ReadOnlyProjectPermission


class DTODetailViewV1(APIView):
	permission_classes = [IsAuthenticated, ReadOnlyProjectPermission, ]
	renderer_classes = [api.JsonRenderer, ]

	def get(self, request, uuid):
		return api.response('ok')