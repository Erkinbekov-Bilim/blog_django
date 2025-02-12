from tkinter.constants import CASCADE

from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=24)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=24)

    def __str__(self):
        return self.name

class Post(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    rate = models.IntegerField(null=True, blank=  True)
    created_at = models.DateTimeField(auto_now_add=True, null=True) # При каждом создании модели будет автоматически обновляться
    updated_at = models.DateTimeField(auto_now=True, null=True) # При каждом изменении модели будет автоматически обновляться
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)


    def __str__(self):
        return self.title
