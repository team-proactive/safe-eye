from django.db import models

class MediaFile(models.Model):

    video = models.FileField(upload_to='sample-video/')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    result = models.JSONField(null=True, blank=True)

    app_label = 'media'
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    result = models.JSONField(null=True, blank=True)

