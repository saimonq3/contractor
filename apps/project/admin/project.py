from django.contrib import admin

from apps.project.models import Project, Members
from utils.admin_mixin import CreatedByModelAdminMixin


class MembersInLine(admin.TabularInline):
	model = Members
	extra = 0


@admin.register(Project)
class ProjectAdmin(CreatedByModelAdminMixin):
	list_display = [
		'uuid',
		'name',
		'company',
		'description',
		'owner',
		'id',
		'created_by'
	]
	fields = [
		'uuid',
		'name',
		'company',
		'description',
		'owner',
		'base_url',
		'id',
		'created_by'
	]
	readonly_fields = [
		'uuid',
		'id',
		'created_by'
	]
	inlines = [MembersInLine, ]
