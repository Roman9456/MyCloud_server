from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile 

# Renaming and updating form for user creation
class RegistrationForm(UserCreationForm):
    """
    Form to handle user registration with necessary fields.
    """
    class Meta(UserCreationForm.Meta):
        model = UserProfile  # Use UserProfile model
        fields = ('username', 'email', 'first_name', 'last_name')  # You can include additional fields if needed

# Renaming and updating form for user profile change
class ProfileUpdateForm(UserChangeForm):
    """
    Form to handle updating user profile details.
    """
    class Meta:
        model = UserProfile  # Use UserProfile model
        fields = ('username', 'email', 'first_name', 'last_name', 'file_storage_path')  # Update 'storage_path' to 'file_storage_path'

