from django.contrib.auth.models import User
from django.db import models


class Motion(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False)
    index = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['index']


class Video(models.Model):
    motion = models.ForeignKey(to=Motion, on_delete=models.PROTECT, null=False, blank=False, related_name='video_set')
    name = models.CharField(max_length=32, null=False, blank=False)
    img1 = models.ImageField(upload_to='media/img', null=True, blank=False)
    img2 = models.ImageField(upload_to='media/img', null=True, blank=False)
    img3 = models.ImageField(upload_to='media/img', null=True, blank=False)
    model = models.FileField(upload_to='media/model', help_text='모델 파일 업로드')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


"""
class VideoModel(models.Model):
    video = models.ForeignKey(to=Video, on_delete=models.PROTECT, null=False, blank=False,
                              related_name='video_model_set')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False, related_name='video_model_set')
    model = models.FileField(upload_to='media/model')
"""


class Log(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=False, blank=False, related_name='log_set')
    motion = models.ForeignKey(to=Motion, on_delete=models.PROTECT, null=False, blank=False, related_name='log_set')
    count = models.IntegerField(null=False, blank=False)
    created_at = models.DateField(null=False, blank=False, auto_now=True)

    class Meta:
        ordering = ['created_at']
