from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated

from ...models import DTO, Members
from .serializers import DTOSerializerV1


class DTOCursorPagination(CursorPagination):
	page_size = 20
	ordering = 'id'

class ListDTOV1View(ListAPIView):
	permission_classes = [IsAuthenticated, ]
	queryset = DTO.objects.all()
	serializer_class = DTOSerializerV1
	pagination_class = DTOCursorPagination

	def get_queryset(self):
		request_name = self.request.query_params.get('name')
		request_project_uuid = self.request.query_params.get('project_uuid')

		user_dto_ids = Members.objects.filter(user=self.request.user).values_list('dto_id')

		query = Q(id__in=user_dto_ids)
		if request_project_uuid:
			query.add(Q(project__uuid=request_project_uuid), Q.AND)
		if request_name:
			query.add(Q(name__icontains=request_name), Q.AND)

		return DTO.objects.filter(query).select_related('project')

