from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from ..models import Directory


@admin.register(Directory)
class DirectoryAdmin(TreeAdmin):
	list_display = [
		'uuid',
		'name',
		'created_by'
	]

	ordering = ['name']

	search_fields = ['name']

	form = movenodeform_factory(Directory)