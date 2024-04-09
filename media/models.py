from django.db import models


class MediaFile(models.Model):
    app_label = 'media'
    file = models.FileField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=100, null=True, blank=True)
    ai_model = models.FileField(upload_to='ai_models/', blank=True, null=True)

#위 예시에서는 description 필드를 추가하여 파일에 대한 설명을 저장할 수 있도록 하였고, 
# file_size 필드를 추가하여 파일 크기를 저장할 수 있도록 하였습니다. 
# 또한 file_type 필드를 추가하여 파일의 형식을 저장할 수 있도록 하였습니다.