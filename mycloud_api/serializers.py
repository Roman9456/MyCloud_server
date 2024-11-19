from rest_framework import serializers
from .models import User, File
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_admin']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'comment', 'size', 'upload_date', 'last_downloaded']
        read_only_fields = ['user', 'upload_date', 'last_downloaded'] 

    def create(self, validated_data):
        # Извлекаем пользователя из контекста запроса и добавляем его к файлу
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    # Валидация для комментариев
    def validate_comment(self, value):
        if value and len(value) > 500:  # Проверка на длину комментария
            raise serializers.ValidationError("Comment is too long.")
        return value

    # Валидация имени файла
    def validate_name(self, value):
        if File.objects.filter(name=value).exists():
            raise serializers.ValidationError("A file with this name already exists.")
        if not re.match(r'^[a-zA-Z0-9._-]+$', value):  # Допустимые символы
            raise serializers.ValidationError("Invalid characters in file name.")
        return value

    # Валидация поля file
    def validate_file(self, value):
        max_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_size:
            raise serializers.ValidationError(f"File size should not exceed {max_size / (1024 * 1024)} MB.")
        if not value.name.endswith(('.jpg', '.png', '.jpeg')):  # Разрешенные форматы
            raise serializers.ValidationError("File format must be JPG, PNG or JPEG.")
        return value

    # Логика авторизации пользователя
    def validate(self, data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to upload files.")
        return data

    # Дополнительная логика при обновлении файла
    def update(self, instance, validated_data):
        if 'last_downloaded' in validated_data:
            instance.last_downloaded = validated_data['last_downloaded']
        return super().update(instance, validated_data)
