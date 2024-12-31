from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Users


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = user.id
        token['nickname'] = user.nickname

        return token


class UserSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    nickname = serializers.JSONField()
    password = serializers.JSONField()

    class Meta:
        model = Users
        fields = ['nickname', 'password']

    def create(self, validated_data):
        return Users.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
