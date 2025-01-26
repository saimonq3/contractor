from django.contrib import admin
from apps.pact.models import Pact, QueryParams, Header


class QueryParamsInLine(admin.TabularInline):
	model = QueryParams
	extra = 0


class HeadersInLine(admin.TabularInline):
	model = Header
	extra = 0


@admin.register(Pact)
class PactAdmin(admin.ModelAdmin):
	inlines = [
		QueryParamsInLine,
		HeadersInLine
	]
	list_display = [
		'uuid',
		'method',
	]
	fields = [
		'uuid',
		'dto',
		'method',
		'base_url',
		'body'
	]

	readonly_fields = ['uuid', 'id']