from django.db import models


class Company(models.Model):
	name = models.CharField(max_length=128)
	owner = models.ForeignKey('user.User', on_delete=models.PROTECT, default=None, null=True, blank=True,
							  related_name='company_owner')
	arhived = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.name}__{self.owner}'

	class Meta:
		verbose_name = 'Комания'
		verbose_name_plural = 'Компании'

	def delete(self, using=None, keep_parents=False):
		self.athived = True
		return self.save()
