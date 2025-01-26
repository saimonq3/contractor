import uuid

from django.db import models
from model_utils import Choices
from simple_history.models import HistoricalRecords


class Pact(models.Model):
	METHOD_CHOICES = Choices(
		(1, 'get', 'GET'),
		(2, 'post', 'POST'),
		(3, 'put', 'PUT'),
		(4, 'patch', 'PATCH'),
		(5, 'delete', 'DELETE'),
		(6, 'options', 'OPTIONS'),
		(7, 'head', 'HEAD'),
	)

	history = HistoricalRecords()

	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')

	dto = models.ForeignKey('dto.DTO', on_delete=models.PROTECT, default=None, blank=True, null=True,
	                        verbose_name='DTO', related_name='pact')
	method = models.PositiveIntegerField(choices=METHOD_CHOICES, default=1, verbose_name='Метод запроса')
	base_url = models.CharField(max_length=1024, default=None, blank=True, null=True,
	                            verbose_name='Базовый URL запроса')
	body = models.TextField(default=None, blank=True, null=True, verbose_name='Тело запроса')

	@property
	def get_query_params(self):
		return self.query_params.all()

	@property
	def get_headers(self):
		return self.headers.all()

	def __str__(self):
		return f'{self.METHOD_CHOICES[self.method]}__{self.dto}'

	class Meta:
		verbose_name = 'Контракт'
		verbose_name_plural = 'Контракты'
