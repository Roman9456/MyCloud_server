from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    """
    Переопределенная модель User с добавлением поля is_admin.
    Также переопределены связи для групп и разрешений с уникальными именами.
    """
    is_admin = models.BooleanField(default=False)

    # Переопределение полей groups и user_permissions с уникальными related_name
    groups = models.ManyToManyField(
        Group,
        related_name='mycloud_user_groups',  # Уникальное имя для обратного отношения
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='mycloud_user_permissions',  # Уникальное имя для обратного отношения
        blank=True
    )


class File(models.Model):
    """
    Модель для хранения информации о загруженных файлах.
    Содержит информацию о файле, его размере, комментариях и времени загрузки.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    comment = models.TextField(blank=True, null=True)
    size = models.BigIntegerField()  # Используем BigIntegerField для больших файлов
    upload_date = models.DateTimeField(auto_now_add=True, db_index=True)  # Индексация для поиска по дате
    last_downloaded = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"File {self.name} uploaded by {self.user.username}"

    # Метод для обновления времени последнего скачивания
    def update_last_downloaded(self):
        """Обновляет поле last_downloaded при скачивании файла."""
        self.last_downloaded = timezone.now()
        self.save(update_fields=['last_downloaded'])  # Сохраняем только обновленное поле
