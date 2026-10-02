from django.db import models
from django.contrib.auth.models import User


class VocabularyWord(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    word =models.CharField(max_length=100)
    translation =models.CharField(max_length=255, blank=True)
    context =models.TextField(blank=True)
    added_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.word}"