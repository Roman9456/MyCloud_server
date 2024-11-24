import logging
import re
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework import serializers
from .models import UserProfile, UserFile

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model with basic fields and custom validation.
    """
    class Meta:
        model = UserProfile 
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']  # Use existing fields

    def validate_username(self, value):
        """
        Validate that the username contains only Latin letters and digits,
        starts with a letter, and is between 4 and 20 characters long.
        """
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', value):
            raise serializers.ValidationError(
                "Username must contain only Latin letters and numbers, start with a letter, and be between 4 and 20 characters long."
            )
        return value

    def validate_email(self, value):
        """
        Validate the email address format.
        """
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Please enter a valid email address.")
        return value


class FileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserFile model with custom validation logic.
    """
    class Meta:
        model = UserFile
        fields = ['id', 'original_filename', 'file', 'comment', 'size', 'upload_date', 'last_downloaded']
        read_only_fields = ['owner', 'upload_date', 'last_downloaded']  # Read-only fields

    def create(self, validated_data):
        """
        Override the create method to set the current user as the file's owner.
        """
        user = self.context['request'].user  # Get the current authenticated user
        validated_data['owner'] = user
        return super().create(validated_data)

    def validate_comment(self, value):
        """
        Validate that the comment does not exceed 500 characters.
        """
        if value and len(value) > 500:
            raise serializers.ValidationError("Comment is too long. Max length is 500 characters.")
        return value

    def validate_original_filename(self, value):
        """
        Validate the uniqueness and allowed characters of the file name.
        """
        if UserFile.objects.filter(original_filename=value).exists():
            raise serializers.ValidationError("A file with this name already exists.")
        if not re.match(r'^[a-zA-Z0-9._-]+$', value):  # Allowed characters for file name
            raise serializers.ValidationError("Invalid characters in file name. Only letters, numbers, '-', '_', and '.' are allowed.")
        return value

    def validate_file(self, value):
        """
        Validate the file size and format.
        """
        max_size = 10 * 1024 * 1024  # Max size 10MB
        if value.size > max_size:
            raise serializers.ValidationError(f"File size should not exceed {max_size / (1024 * 1024)} MB.")
        if not value.name.endswith(('.jpg', '.png', '.jpeg')):  # Allowed formats
            raise serializers.ValidationError("File format must be JPG, PNG, or JPEG.")
        return value

    def validate(self, data):
        """
        Custom validation to check if the user is authenticated before uploading the file.
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to upload files.")
        return data

    def update(self, instance, validated_data):
        """
        Override the update method to update the 'last_downloaded' field.
        """
        if 'last_downloaded' in validated_data:
            instance.last_downloaded = validated_data['last_downloaded']
        return super().update(instance, validated_data)
