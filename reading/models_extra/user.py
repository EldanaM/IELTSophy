from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    level =models.CharField(max_length=2, default='B1')
    streak =models.IntegerField(default=0)
    last_test_date =models.DateField(null=True, blank=True)
    total_tests =models.IntegerField(default=0)
    total_correct =models.IntegerField(default=0)
    total_wrong =models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.level}"

    @property
    def avg_percent(self):
        total =self.total_correct + self.total_wrong
        if total == 0:
            return 0
        return round(self.total_correct / total * 100)

    @property
    def forecast_band(self):
        percent = self.avg_percent
        if percent >= 90: return "8.0"
        elif percent >= 80: return "7.0"
        elif percent >= 70: return "6.5"
        elif percent >= 60: return "6.0"
        elif percent >= 50: return "5.5"
        elif percent >= 40: return "5.0"
        return "-"


class Achievement(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    code =models.CharField(max_length=50)
    title =models.CharField(max_length=100)
    icon =models.CharField(max_length=10)
    unlocked_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"