from rest_framework import serializers

from boards.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['user_id', 'is_opened', 'depth1', 'depth2', 'depth3']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        exclude = ['is_deleted', 'deleted_at', 'updated_at']

    def create(self, validated_data):
        return Board.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_id', 'board_id', 'content']

    def create(self, validated_data):
        validated_data['created_at'] = datetime.now()
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        validated_data['updated_at'] = datetime.now()
        instance.save()
        return instance

