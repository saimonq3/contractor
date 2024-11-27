from django.db import models


class Members(models.Model):
	company = models.ForeignKey('company.Company', on_delete=models.PROTECT, default=None, blank=True, null=True,
								related_name='company_members')
	user = models.ForeignKey('user.User', on_delete=models.PROTECT, default=None, blank=True, null=True,
							 related_name='company_members')
	is_admin = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user}__{self.company}'

	class Meta:
		verbose_name = 'Сотрудник компании'
		verbose_name_plural = 'Сотрудники компании'
