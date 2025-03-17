import uuid

from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from utils.model_mixin import CreatedByModelMixin


class Field(TimeStampedModel, CreatedByModelMixin):
    TYPE = Choices(
        (1, 'int', 'Integer'),
        (2, 'str', 'String'),
        (3, 'list', 'List'),
        (4, 'dict', 'Dictionary'),
        (5, 'fk', 'ForeignKey'),
    )

    history = HistoricalRecords()

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')
    dto = models.ForeignKey('dto.DTO', on_delete=models.CASCADE, default=None, null=True, blank=True,
                            related_name='dto_fields')
    type = models.PositiveIntegerField(choices=TYPE, default=None, null=True, blank=True)
    value = models.TextField(default=None, blank=True, null=True)
    description = models.TextField(default=None, blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.dto}__{self.type}'

    class Meta:
        verbose_name = 'Поле ДТО'
        verbose_name_plural = 'Поля ДТО'
