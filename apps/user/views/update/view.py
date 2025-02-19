from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from utils import api
from ...models import User
from .serializer import UpdateSerializer


class UpdateProfile(UpdateAPIView):
	permission_classes = [IsAuthenticated, ]
	serializer_class = UpdateSerializer
	queryset = User.objects.all()
	lookup_field = 'uuid'

	def put(self, request, *args, **kwargs):
		if self.get_object() != request.user:
			return api.error_response(code=403, status=403)
		return super().put(request, *args, **kwargs)