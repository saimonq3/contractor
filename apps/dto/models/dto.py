from django.db import models


class DTO(models.Model):
	name = models.CharField(max_length=128)
	project = models.ForeignKey('project.Project', on_delete=models.PROTECT, default=None, null=True, blank=True,
								related_name='dto')
	description = models.TextField(verbose_name='Описание', default=None, null=True, blank=True)
	arhived = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.name}__{self.project}'

	class Meta:
		verbose_name = 'ДТО'
		verbose_name_plural = 'ДТО'

	def delete(self, using=None, keep_parents=False):
		self.athived = True
		return self.save()
