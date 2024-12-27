from rest_framework import serializers

from boards.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['user_id', 'is_opened', 'depth1', 'depth2', 'depth3']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.id = validated_data.get('id', instance.id)
        instance.is_opened = validated_data.get('is_opened', instance.is_opened)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.depth1 = validated_data.get('depth1', instance.depth1)
        instance.depth2 = validated_data.get('depth2', instance.depth2)
        instance.depth3 = validated_data.get('depth3', instance.depth3)
        instance.save()
        return instance


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

    def create(self, validated_data):
        return Board.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.deleted_at = validated_data.get('deleted_at', instance.deleted_at)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.board_id = validated_data.get('board_id', instance.board_id)
        instance.content = validated_data.get('content', instance.content)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.deleted_at = validated_data.get('deleted_at', instance.deleted_at)
        instance.save()
        return instance

