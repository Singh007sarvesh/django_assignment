
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


class AccountAdmin(UserAdmin):
	ordering = ('email',)
	list_display = ('email', 'last_login', 'is_admin', 'is_staff')
	search_fields = ('email',)
	readonly_fields = ('last_login',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)