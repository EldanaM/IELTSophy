from django.db import models
from django.contrib.auth.models import User
from ..models import Text


class TestSession(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    text =models.ForeignKey(Text, on_delete=models.CASCADE)
    correct =models.IntegerField(default=0)
    wrong =models.IntegerField(default=0)
    percent =models.IntegerField(default=0)
    time_spent =models.IntegerField(default=0)
    started_at =models.DateTimeField(auto_now_add=True)
    finished_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.text.title} - {self.percent}%"


class Mistake(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    question_type =models.CharField(max_length=50)
    count =models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.question_type}: {self.count}"