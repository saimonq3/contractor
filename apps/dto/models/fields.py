from django.db import models
from model_utils import Choices


class Field(models.Model):
    TYPE = Choices(
        (1, 'int', 'Integer'),
        (2, 'str', 'String'),
        (3, 'list', 'List'),
        (4, 'dict', 'Dictionary'),
        (5, 'fk', 'ForeignKey'),
    )

    dto = models.ForeignKey('dto.DTO', on_delete=models.CASCADE, default=None, null=True, blank=True,
                            related_name='dto_fields')
    type = models.PositiveIntegerField(choices=TYPE, default=None, null=True, blank=True)
    value = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.dto}__{self.type}'

    class Meta:
        verbose_name = 'Поле ДТО'
        verbose_name_plural = 'Поял ДТО'
