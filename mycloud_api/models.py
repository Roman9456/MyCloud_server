import os
import uuid
import logging
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver

logger = logging.getLogger(__name__)

def user_directory_path(instance, filename):
    """
    Function to generate a file upload path for a directory associated with the user.
    """
    return os.path.join('user_files', instance.owner.file_storage_path, f'{uuid.uuid4().hex}_{filename}')


class UserProfile(AbstractUser):
    """
    Custom user model including a field for the file storage path.
    """
    file_storage_path = models.CharField(
        max_length=255, 
        verbose_name='File Storage Path', 
        default=''
    )

    def save(self, *args, **kwargs):
        """
        Overridden save method to automatically generate the file storage path 
        if not provided. Also ensures the directory for storage exists.
        """
        super().save(*args, **kwargs)
        
        if not self.file_storage_path:
            self.file_storage_path = f'user_{self.id}_{uuid.uuid4()}'
            user_directory = os.path.join(settings.MEDIA_ROOT, 'user_files', self.file_storage_path)
            os.makedirs(user_directory, exist_ok=True)
            logger.info(f"Directory created for user {self.username}: {user_directory}")
            
            # Save the user again to persist the generated file_storage_path
            self.save(update_fields=['file_storage_path'])


class UserFile(models.Model):
    """
    Model to store information about uploaded files, including file name, size,
    comments, and upload date. Also handles file paths and unique links.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='user_files'
    )
    original_filename = models.CharField(
        max_length=255, 
        verbose_name='Original File Name'
    )
    file = models.FileField(upload_to=user_directory_path, verbose_name='File Location', max_length=500)
    comment = models.TextField(blank=True, null=True, verbose_name='File Comment')
    size = models.BigIntegerField(verbose_name='File Size')  # Using BigIntegerField for large files
    upload_date = models.DateTimeField(
        auto_now_add=True, 
        db_index=True,  # Index for faster queries by upload date
        verbose_name='Upload Date'
    )
    last_downloaded = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Last Downloaded Date'
    )
    special_link = models.CharField(
        max_length=255, 
        unique=True, 
        editable=False, 
        verbose_name='Unique File Link'
    )

    class Meta:
        unique_together = ('owner', 'original_filename')  # Enforcing unique file names for each user
        indexes = [
            models.Index(fields=['upload_date']),
            models.Index(fields=['owner']),
        ]

    def __str__(self):
        return f"File {self.original_filename} uploaded by {self.owner.username}"

    def save(self, *args, **kwargs):
        """
        Overridden save method to generate a unique link for the file
        and calculate the file size before saving.
        """
        if not self.pk:  # Generate a unique link only for new files
            self.special_link = uuid.uuid4().hex
            logger.info(f"Generated special link for file: {self.original_filename} - {self.special_link}")
        
        # If the file size is not specified, calculate it
        if self.file and not self.size:
            self.size = self.file.size  # Automatically determine the file size if not provided

        super().save(*args, **kwargs)

    def update_last_downloaded(self):
        """
        Updates the 'last_downloaded' field when the file is accessed.
        """
        self.last_downloaded = timezone.now()
        self.save(update_fields=['last_downloaded'])  # Save only the updated field


@receiver(post_delete, sender=UserFile)
def delete_file_on_disk(sender, instance, **kwargs):
    """
    Deletes the file from disk when the corresponding record in the database is deleted.
    This prevents "orphaned" files from remaining on the server.
    """
    if instance.file:
        try:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
                logger.info(f"File '{instance.original_filename}' successfully deleted from disk.")
        except Exception as e:
            logger.error(f"Error deleting file '{instance.original_filename}': {str(e)}")
