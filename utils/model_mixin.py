"""
Тут описываются различные миксины для моделей
"""

from django.db import models


class CreatedByModelMixin(models.Model):
    """
    Миксин для добавления поля created_by(Создатель), для того чтобы не прописывать это поля во всех моделях каждый раз
    """
    created_by = models.ForeignKey('user.User', related_name='+', on_delete=models.PROTECT, verbose_name='Создатель')

    class Meta:
        abstract = True