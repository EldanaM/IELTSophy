from django.db import models
from django.contrib.auth.models import User

class Text(models.Model):
    title =models.CharField(max_length=255)
    content =models.TextField()
    level =models.CharField(max_length=2)
    topic =models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} ({self.level})"


class Question(models.Model):
    text =models.ForeignKey(Text, on_delete=models.CASCADE, related_name='questions')
    question_text =models.TextField()
    option_a =models.CharField(max_length=255)
    option_b =models.CharField(max_length=255)
    option_c =models.CharField(max_length=255)
    option_d =models.CharField(max_length=255)
    correct_option =models.CharField(max_length=1, choices=[
        ('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')
    ])
    question_type =models.CharField(max_length=50, default='multiple')

    def __str__(self):
        return self.question_text[:60]


from .models_extra.user import UserProfile, Achievement
from .models_extra.video import PreparingVideo
from .models_extra.vocabulary import VocabularyWord
from .models_extra.session import TestSession, Mistake