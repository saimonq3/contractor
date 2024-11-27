from django.db import models


class Members(models.Model):
	project = models.ForeignKey('project.Project', on_delete=models.PROTECT, default=None, blank=True, null=True,
								related_name='project_members')
	user = models.ForeignKey('user.User', on_delete=models.PROTECT, default=None, blank=True, null=True,
							 related_name='project_members')
	is_admin = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user}__{self.project}'

	class Meta:
		verbose_name = 'Админ Проекта'
		verbose_name_plural = 'Админы проекта'
