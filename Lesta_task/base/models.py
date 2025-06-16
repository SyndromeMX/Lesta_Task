from django.db import models
from django.contrib.auth.models import AbstractUser


# 👤 Кастомный пользователь
class User(AbstractUser):
    # Используем встроенные поля: username, password и т.д.
    def __str__(self):
        return self.username


# 📁 Загруженные документы
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} (от {self.user.username})"


# 📦 Коллекция документов
class Collection(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    documents = models.ManyToManyField(Document, related_name='collections')

    def __str__(self):
        return f"{self.name} (владелец: {self.user.username})"


# 📊 Метрики обработки
class FileMetric(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(help_text="Размер файла в байтах")
    processed = models.BooleanField(default=False)
    error_count = models.IntegerField(default=0)
    processing_time = models.FloatField(
        help_text="Время обработки в секундах", null=True, blank=True
    )

    def __str__(self):
        return f"{self.filename} ({self.file_size} байт)"
