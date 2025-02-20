import uuid

from django.db import models
from django.db.models.query import QuerySet
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords
from treebeard.mp_tree import MP_Node

from utils.model_mixin import CreatedByModelMixin


class DirectoryQuerySet(models.QuerySet):
	def with_descendants(self, *args, **kwargs):
		"""
		Получить категорию вместе с потомками.
		"""
		root_category = self.get(*args, **kwargs)
		return self.model.get_tree(parent=root_category)

	def filter_with_descendants(self, *args, **kwargs) -> QuerySet:
		root_categories = self.filter(*args, **kwargs)

		if not root_categories:
			return self.none()

		query = models.Q()
		for category in root_categories:
			if category.is_leaf():
				query |= models.Q(pk=category.pk)
			else:
				query |= models.Q(name__startswith=category.name, depth__gte=category.depth)

		return self.filter(query).distinct().order_by('name')

class Directory(MP_Node, TimeStampedModel, CreatedByModelMixin):
	history = HistoricalRecords()
	objects = DirectoryQuerySet.as_manager()

	uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='Идентификатор')
	name = models.CharField(max_length=128, verbose_name='Каталог')
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)

	node_order_by = ['name']

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Каталог'
		verbose_name_plural = 'Каталоги'