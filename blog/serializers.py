from rest_framework import serializers
from .models import Post, Comment, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    is_deleted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at', 'parent', 'is_deleted')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['replies'] = CommentSerializer(instance.replies.filter(is_deleted=False), many=True).data
        return representation


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'author', 'created_at', 'updated_at', 'published', 'published_at', 'view_count', 'category', 'category_id', 'tags', 'tag_ids', 'comments')
        read_only_fields = ('id', 'created_at', 'updated_at', 'published_at', 'view_count', 'comments')

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("제목은 5글자 이상이어야 합니다.")
        return value

    def create(self, validated_data):
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        post = Post.objects.create(**validated_data)
        if category_id:
            post.category_id = category_id
        post.tags.set(tag_ids)
        return post

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', [])
        instance = super().update(instance, validated_data)
        if category_id:
            instance.category_id = category_id
        instance.tags.set(tag_ids)
        return instance