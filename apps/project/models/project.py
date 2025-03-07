import uuid

from django.db import models
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from utils.model_mixin import CreatedByModelMixin


class Project(TimeStampedModel, CreatedByModelMixin):
    history = HistoricalRecords()

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')
    name = models.CharField(max_length=128)
    description = models.TextField(verbose_name='Описание', default=None, null=True, blank=True)
    owner = models.ForeignKey('user.User', on_delete=models.PROTECT, related_name='project_owner')
    company = models.ForeignKey('company.Company', on_delete=models.PROTECT, related_name='projects')
    base_url = models.CharField(max_length=128, default=None, blank=True, null=True, verbose_name='Базовый URL проекта')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
