from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUserModel, PasswordReset

# Register your models here.

class CustomUserViewAdmin(admin.ModelAdmin):
    list_display=["username", "email", "is_active", "is_staff"]
    
    def get_readonly_fields(self, request, obj):
        """
        Set fields as read-only conditionally:
        - 'password' becomes read-only in edit view
        - 'is_staff' becomes read-only if user lacks permission to change user
        """
        readonly_fields = []

        if obj:  # Falls ein Objekt existiert, ist es die Bearbeitungsansicht -> `password` ist readonly
            readonly_fields.append("password")

        if not request.user.has_perm("auth.change_user"):  # Falls der Benutzer keine Berechtigung hat -> `is_staff` ist readonly
            readonly_fields.append("is_staff")

        return readonly_fields
    
    def get_fieldsets(self, request, obj):
        """
        Define the layout of fields for add and edit views.

        Returns a custom fieldset depending on whether the object exists.
        """
        if obj:  # Wenn ein Objekt existiert, handelt es sich um eine Bearbeitungsansicht
            return [
                (
                    'Individuelle Daten',
                    {
                        'fields': (
                            'username',
                            'email',
                            'is_active',
                            'is_staff',
                            'password',
                        )
                    }
                )
            ]
        else:  # Falls kein Objekt existiert, handelt es sich um die Hinzufügen-Ansicht
            return [
                # *UserAdmin.fieldsets,
                (
                    'Individuelle Daten',
                    {
                        'fields': (
                            'username',
                            'email',
                            'password',
                        )
                    }
                ),
            ]

admin.site.register(CustomUserModel, CustomUserViewAdmin)
admin.site.register(PasswordReset)