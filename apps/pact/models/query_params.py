from django.db import models
from model_utils.models import TimeStampedModel

from utils.model_mixin import CreatedByModelMixin


class QueryParams(TimeStampedModel, CreatedByModelMixin):

	pact = models.ForeignKey('pact.Pact', on_delete=models.CASCADE,  related_name='query_params')
	key = models.CharField(max_length=128, blank=True, null=True, default=None)
	value = models.CharField(max_length=256, blank=True, null=True, default=None)

	def __str__(self):
		return f'"{self.key}": "{self.value}"'

	class Meta:
		verbose_name = 'Параметр запроса'
		verbose_name_plural = 'Параметры запроса'
		unique_together = ['key', 'value', 'pact']