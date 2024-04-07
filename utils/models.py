from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tag_type = models.CharField(max_length=100)
    tag_content = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Status(models.Model):
    available = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TagMixin(models.Model):
    tags = GenericRelation(Tag)

    class Meta:
        abstract = True


class StatusMixin(models.Model):
    status = GenericRelation(Status)

    class Meta:
        abstract = True