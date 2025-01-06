import uuid

from django.db import models


class Company(models.Model):
	"""
	Модель описывает компании
	"""

	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')
	name = models.CharField(max_length=128)
	owner = models.ForeignKey('user.User', on_delete=models.PROTECT, default=None, null=True, blank=True,
							  related_name='company_owner')
	arhived = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.name}__{self.owner}'

	class Meta:
		verbose_name = 'Комания'
		verbose_name_plural = 'Компании'
		unique_together = ['name', 'owner']
