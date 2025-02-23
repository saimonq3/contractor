from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils import api
from .serializers import ProfileSerializer


class UserProfile(APIView):
	permission_classes = [IsAuthenticated, ]


	def get(self, request):
		user = request.user
		serializer = ProfileSerializer(user)

		return api.response(serializer.data)

