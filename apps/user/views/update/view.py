from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.user.views.update.serializer import UpdateSerializer


class UpdateProfile(UpdateAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = UpdateSerializer

	def put(self, request, *args, **kwargs):
		return super().put(request, *args, **kwargs)