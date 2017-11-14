from django.contrib import admin
from .models import User, Product, Purchase, Item, Validator, Cart
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminForm


class UserAdmin(BaseUserAdmin):
	add_form = UserAdminCreationForm
	add_fieldsets = (
		(None, {'fields': ('username', 'email', 'cpf', 'password1', 'password2')}
			)
		)
	form = UserAdminForm	
	fieldsets = (
					(None, {'fields': ('username', 'email')}),
		('Informaçoes',{'fields': ('last_login', 'cpf')}),
		('Permissoes',{'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')})
		)
	list_display = ['id', 'username', 'cpf', 'email', 'is_active', 'is_staff', 'date_joined']
	search_fields = ['username', 'id']


#PARA MOSTRAR NO PAINEL DE ADMIN
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Validator)
