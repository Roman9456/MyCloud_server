from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mycloud_api.models import User, File  # Импортируем модели User и File

# Регистрация кастомной модели User с админским интерфейсом
class CustomUserAdmin(UserAdmin):
    # Отображаем поля в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_admin')
    search_fields = ('username', 'email')  # Поиск по имени пользователя и email
    readonly_fields = ('date_joined',)  # Поля, которые нельзя редактировать

    # Определение полей для редактирования пользователя
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Регистрация модели пользователя в админке с кастомным UserAdmin
admin.site.register(User, CustomUserAdmin)

# Регистрация модели File с настройками отображения в админке
class FileAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке
    list_display = ('name', 'user', 'size', 'upload_date', 'last_downloaded', 'comment')
    
    # Поля, по которым можно будет производить поиск
    search_fields = ('name', 'user__username', 'comment')
    
    # Фильтры, которые будут доступны в админке
    list_filter = ('user', 'upload_date')
    
    # Поля, которые отображаются при редактировании объекта
    fieldsets = (
        (None, {'fields': ('name', 'user', 'file', 'comment', 'size')}),
        ('Dates', {'fields': ('upload_date', 'last_downloaded')}),
    )
    
    # Поля, доступные для редактирования
    readonly_fields = ('upload_date',)

# Регистрируем модель File в админке с кастомным FileAdmin
admin.site.register(File, FileAdmin)
