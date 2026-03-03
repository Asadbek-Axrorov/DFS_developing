from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('avatar_preview', 'username', 'get_full_name', 'email', 'role_badge', 'is_verified', 'is_active', 'created_at')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('-created_at',)
    list_per_page = 20

    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('role', 'phone', 'bio', 'avatar', 'date_of_birth', 'telegram', 'is_verified'),
            'classes': ('wide',),
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="35" height="35" style="border-radius:50%; object-fit:cover;"/>', obj.avatar.url)
        initials = (obj.first_name[:1] + obj.last_name[:1]).upper() if obj.first_name else obj.username[:2].upper()
        colors = {'student': '#4F46E5', 'mentor': '#059669', 'curator': '#D97706', 'admin': '#DC2626'}
        color = colors.get(obj.role, '#6B7280')
        return format_html(
            '<div style="width:35px;height:35px;border-radius:50%;background:{};display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:12px;">{}</div>',
            color, initials
        )
    avatar_preview.short_description = ''

    def role_badge(self, obj):
        colors = {
            'student': ('bg:#EEF2FF', '#4F46E5'),
            'mentor': ('bg:#ECFDF5', '#059669'),
            'curator': ('bg:#FFFBEB', '#D97706'),
            'admin': ('bg:#FEF2F2', '#DC2626'),
        }
        bg, color = colors.get(obj.role, ('bg:#F3F4F6', '#6B7280'))
        return format_html(
            '<span style="padding:3px 10px;border-radius:20px;{};color:{};font-size:11px;font-weight:600;">{}</span>',
            bg, color, obj.get_role_display()
        )
    role_badge.short_description = 'Rol'
