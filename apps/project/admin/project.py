from django.contrib import admin

from apps.project.models import Project, Members


class MembersInLine(admin.TabularInline):
	model = Members
	extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = [
		'uuid',
		'name',
		'company',
		'description',
		'owner',
		'id'
	]
	fields = [
		'uuid',
		'name',
		'company',
		'description',
		'owner',
		'base_url',
		'id'
	]
	readonly_fields = [
		'uuid',
		'id'
	]
	inlines = [MembersInLine, ]
