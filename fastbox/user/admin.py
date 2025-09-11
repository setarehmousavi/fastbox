from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile

# ✅ Inline to include UserProfile in the User admin page
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# ✅ Your existing UserAdmin, only slightly extended
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'username', 'get_role', 'is_staff', 'is_superuser']
    search_fields = ['email', 'username']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')

    # ✅ Include UserProfile in User admin
    inlines = (UserProfileInline,)

    # ✅ Show role in list_display
    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else '-'
    get_role.short_description = 'Role'

# ✅ Register with custom UserAdmin
admin.site.register(User, UserAdmin)
