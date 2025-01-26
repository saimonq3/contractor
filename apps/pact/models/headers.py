from django.db import models


class Header(models.Model):
	pact = models.ForeignKey('pact.Pact', on_delete=models.CASCADE, related_name='headers')
	key = models.CharField(max_length=64)
	value = models.CharField(max_length=1024)

	def __str__(self):
		return f'"{self.key}": "{self.value}"'

	class Meta:
		verbose_name = 'Заголовок'
		verbose_name_plural = 'Заголовки'
