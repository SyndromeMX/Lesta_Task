from django.db import models


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



class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name



