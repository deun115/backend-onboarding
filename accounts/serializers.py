from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Users


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['nickname'] = user.nickname

        return token


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    nickname = serializers.JSONField()
    password = serializers.JSONField()

    class Meta:
        model = Users
        fields = '__all__'

    def create(self, validated_data):
        return Users.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.uuid)
        instance.password = validated_data.get('password', instance.password)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()
        return instance
