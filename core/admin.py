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



class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_cart', 'status')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_product', 'id_cart', 'quantity')

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'finalized')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'bar_code')








admin.site.register(Purchase, PurchaseAdmin)



admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Validator)

