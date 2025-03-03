import uuid

from django.db import models
from model_utils.models import TimeStampedModel

from utils.model_mixin import CreatedByModelMixin


class Company(TimeStampedModel, CreatedByModelMixin):
	"""
	Модель описывает компании
	"""

	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')
	name = models.CharField(max_length=128)
	owner = models.ForeignKey('user.User', on_delete=models.PROTECT, default=None, null=True, blank=True,
							  related_name='company_owner')
	deleted = models.BooleanField(default=False, verbose_name='Удалена')


	def __str__(self):
		return f'{self.name}'

	class Meta:
		verbose_name = 'Комания'
		verbose_name_plural = 'Компании'
		unique_together = ['name', 'owner']
