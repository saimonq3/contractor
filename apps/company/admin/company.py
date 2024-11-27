from django.contrib import admin

from apps.company.models import Company, Members


class MemberInLine(admin.TabularInline):
	model = Members
	extra = 0


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	inlines = [MemberInLine]
	list_display = [
		'name',
		'owner',
		'arhived'
	]
	fields = [
		'name',
		'owner',
		'arhived'
	]
