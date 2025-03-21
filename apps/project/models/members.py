import uuid

from django.db import models
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class Members(TimeStampedModel):
	history = HistoricalRecords()

	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')
	project = models.ForeignKey('project.Project', on_delete=models.PROTECT, default=None, blank=True, null=True,
								related_name='project_members')
	user = models.ForeignKey('user.User', on_delete=models.PROTECT, default=None, blank=True, null=True,
							 related_name='project_members')
	is_admin = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user}__{self.project}'

	class Meta:
		verbose_name = 'Участник Проекта'
		verbose_name_plural = 'Участники проекта'
