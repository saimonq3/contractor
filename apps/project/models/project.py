from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(verbose_name='Описание', default=None, null=True, blank=True)
    owner = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='project_owner')
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT, related_name='projects')
    arhived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}__{self.company}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def delete(self, using=None, keep_parents=False):
        self.athived = True
        return self.save()
