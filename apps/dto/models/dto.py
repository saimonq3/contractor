import uuid

from django.db import models
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from utils.model_mixin import CreatedByModelMixin


class DTO(TimeStampedModel, CreatedByModelMixin):
	history = HistoricalRecords()

	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')
	name = models.CharField(max_length=128)
	project = models.ForeignKey('project.Project', on_delete=models.PROTECT, default=None, null=True, blank=True,
								related_name='dto')
	description = models.TextField(verbose_name='Описание', default=None, null=True, blank=True)
	base_url = models.CharField(max_length=256, default=None, blank=True, null=True, verbose_name='Базовый URL DTO')

	def __str__(self):
		return f'{self.name}__{self.project}'

	class Meta:
		verbose_name = 'ДТО'
		verbose_name_plural = 'ДТО'
		unique_together = ['project', 'name']
