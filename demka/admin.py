from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Application, Review


# Тут регистрируем нужные для админки данные и как с ними можно взаимодействовать - фильтры, поля по которым можно искать, сортировка, неизменяемые поля.
# Для экзамена - не обязательно, так как относится к джанговской админке, а не кастомной в templates. Но тут нужно смотреть критерии какая из админок вообще требуется. Если кастомная - этот файл может быть пустым


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'phone', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'patronymic', 'email', 'phone')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('patronymic', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('first_name', 'last_name', 'patronymic', 'phone', 'email')}),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_user_full_name', 'course_name', 'desired_start_date', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__patronymic', 'course_name', 'user__phone', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    ordering = ('-created_at',)

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
    get_user_full_name.short_description = 'ФИО пользователя'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_user_full_name', 'application', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'application__course_name', 'comment')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
    get_user_full_name.short_description = 'ФИО пользователя'