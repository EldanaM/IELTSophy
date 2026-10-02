from django.db import models


class PreparingVideo(models.Model):
    TYPE_CHOICES =[
        ('video', 'Video'),
        ('link', 'Useful Link'),
    ]

    title =models.CharField(max_length=255)
    description =models.TextField()
    tag =models.CharField(max_length=50)
    type =models.CharField(max_length=20, choices=TYPE_CHOICES, default='video')
    url =models.URLField(blank=True, null=True)
    date =models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name ='Preparing Video'
        verbose_name_plural ='Preparing Videos'