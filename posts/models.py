from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    rate = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True) # При каждом создании модели будет автоматически обновляться
    updated_at = models.DateTimeField(auto_now=True, null=True) # При каждом изменении модели будет автоматически обновляться

    def __str__(self):
        return self.title
