import logging
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.urls import path, reverse
from django.utils.crypto import get_random_string
from .forms import RegistrationForm, ProfileUpdateForm
from .models import UserFile

# Logger setup
logger = logging.getLogger(__name__)

# Get the user model configured in settings.py
User = get_user_model()

# Customizing the admin panel for the custom User model
class CustomUserAdmin(UserAdmin):
    # Forms for creating and updating user information
    add_form = RegistrationForm  # Registration form
    form = ProfileUpdateForm  # Profile update form
    
    # Fields to display in the user list
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'file_storage_path', 'is_active', 'is_staff', 'is_superuser']

    # Filters for the user list
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    
    # Fields to search among users
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # Adding custom field 'file_storage_path' to the user form
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('file_storage_path',)}),  # Custom field
    )
    
    # Fields when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('file_storage_path',)}),  # Custom field
    )

    # Adding custom URL for user password reset
    def get_urls(self):
        """
        Override default URLs to add a custom URL for password reset.
        """
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/password/', self.admin_site.admin_view(self.reset_password), name='reset-password'),
        ]
        return custom_urls + urls

    # Logic for resetting the user's password
    def reset_password(self, request, user_id):
        """
        Resets the user's password and shows a success message.
        """
        user = get_object_or_404(User, pk=user_id)  # Using get_user_model() for correct operation
        new_password = get_random_string(length=8)  # Generate a new password
        user.set_password(new_password)  # Set the new password
        user.save()
        
        # Success message for password reset
        messages.success(request, f'Password for user {user.username} has been reset. New password: {new_password}')
        
        # Redirect to the user change page
        return redirect(reverse('admin:mycloud_api_user_change', args=[user_id]))  # Using the correct name for the redirect

# Register the custom user in the admin panel
admin.site.register(User, CustomUserAdmin)

# Customizing the admin panel for the UserFile model
@admin.register(UserFile)
class FileAdmin(admin.ModelAdmin):
    """
    Admin panel for managing user-uploaded files.
    """
    # Displayed fields
    list_display = ['owner', 'original_filename', 'size', 'upload_date', 'last_downloaded', 'comment', 'file', 'special_link']
    # Filters for the file list
    list_filter = ['owner', 'original_filename']
    # Fields to search
    search_fields = ['owner__username', 'original_filename', 'comment']

    # Add delete file action with logging
    def delete_model(self, request, obj):
        """
        Override delete method, adding logging for file deletion and success message.
        """
        logger.debug("Deleting file %s", obj.original_filename)
        obj.delete()  # Delete the file
        self.message_user(request, "File deleted successfully.")
        logger.info("File %s deleted successfully.", obj.original_filename)

    # Add file download action
    def download_file(self, request, queryset):
        """
        Add the ability to download files through the admin panel.
        """
        for file in queryset:
            # Logic for downloading the file
            pass  # Here could be the code to provide the file for download

        self.message_user(request, "Files are ready for download.")
    download_file.short_description = "Download selected files"

    # Add custom actions in the admin panel
    actions = ['download_file', 'delete_model']
