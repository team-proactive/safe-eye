from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Tag(models.Model):
    """
    객체에 tag를 추가하기 위한 모델.
    어떤 모델의 객체에도 tag를 추가 가능.
    tag의 유형(tag_type)과 내용(tag_content)을 지정, ContentType과 object_id를 통해 해당 객체와 연결.

    Attributes
    id (AutoField): tag의 고유 식별자
    tag_type (CharField): tag의 유형
    tag_content (CharField): tag의 내용
    content_type (ForeignKey): tag가 연결된 모델의 ContentType
    object_id (PositiveIntegerField): tag가 연결된 객체의 id
    content_object (GenericForeignKey): tag가 연결된 객체
    """

    id = models.AutoField(primary_key=True)
    tag_type = models.CharField(max_length=100)
    tag_content = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class Status(models.Model):
    """
    객체의 status를 나타내는 모델.
    어떤 모델의 객체에도 status를 추가 가능.
    객체의 사용 가능 여부(available)를 나타내고, ContentType과 object_id를 통해 해당 객체와 연결.
    생성 시간(created_at)과 업데이트 시간(updated_at)도 자동으로 기록.

    Attributes
    available (BooleanField): 객체의 사용 가능 여부.
    content_type (ForeignKey): status가 연결된 모델의 ContentType.
    object_id (PositiveIntegerField): status가 연결된 객체의 id.
    content_object (GenericForeignKey): status가 연결된 객체.
    created_at (DateTimeField): status가 생성된 시간.
    updated_at (DateTimeField): status가 업데이트된 시간.
    """

    available = models.BooleanField(default=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TagMixin(models.Model):
    """
    Tag 모델과의 관계를 정의하는 클래스.
    이 클래스를 상속받는 모델은 자동으로 Tag 모델과 일대다 관계를 가지고, 해당 모델의 객체에 tag를 추가할 수 있음.

    Attributes
    tags (GenericRelation): Tag 모델과의 일대다 관계.
    """

    tags = GenericRelation(Tag)

    class Meta:
        abstract = True


class StatusMixin(models.Model):
    """
    Status 모델과의 관계를 정의하는 추상 기본 클래스.
    이 클래스를 상속받는 모델은 자동으로 Status 모델과 일대다 관계를 가지고, 해당 모델의 객체에 대한 status 정보를 추가할 수 있음.

    Attributes
    status (GenericRelation): Status 모델과의 일대다 관계.
    """

    status = GenericRelation(Status)

    class Meta:
        abstract = True
