from django.db import models


class QueryParams(models.Model):

	pact = models.ForeignKey('pact.Pact', on_delete=models.CASCADE,  related_name='query_params')
	key = models.CharField(max_length=128, blank=True, null=True, default=None)
	value = models.CharField(max_length=256, blank=True, null=True, default=None)

	def __str__(self):
		return f'"{self.key}": "{self.value}"'

	class Meta:
		verbose_name = 'Параметр запроса'
		verbose_name_plural = 'Параметры запроса'