from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.core.exceptions import PermissionDenied

class UserCreationCustomForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'currency', 'balance')

class UserChangeCustomForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'currency', 'balance', 'is_active', 'is_staff', 'is_superuser')

class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationCustomForm
    form = UserChangeCustomForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'currency', 'balance')
    list_filter = ('currency', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'currency', 'balance', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'currency', 'balance')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    def get_readonly_fields(self, request, instance=None):
        readonly = []
        if instance:
            readonly = ['username', 'email']
            if not request.user.is_superuser:
                readonly.append('balance')
        return readonly

    def has_permission_to_change(self, request, instance=None):
        if instance and 'balance' in request.POST and not request.user.is_superuser:
            raise PermissionDenied("Only superusers can modify the balance.")
        return super().has_change_permission(request, instance)

    def save_instance(self, request, instance, form, is_changed):
        if is_changed and 'balance' in form.changed_data and not request.user.is_superuser:
            raise PermissionDenied("Only superusers can modify the balance.")
        super().save_model(request, instance, form, is_changed)

admin.site.register(User, CustomUserAdmin)
