import uuid

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Users


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['uuid'] = str(user.uuid)
        token['nickname'] = user.nickname

        return token


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    nickname = serializers.JSONField()
    password = serializers.JSONField()

    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        return Users.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.password = validated_data.get('password', instance.password)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()
        return instance
