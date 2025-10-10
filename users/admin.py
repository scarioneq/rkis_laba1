from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, UserUpdateForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = UserUpdateForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'avatar']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'avatar'),
        }),
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Avatar', {'fields': ('avatar',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)