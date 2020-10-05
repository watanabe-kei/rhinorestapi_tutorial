from django.db.models import fields
from django.db.models.fields.related_descriptors import create_reverse_many_to_one_manager
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import TwistedTower

# ユーザー情報のシリアライザー
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only':True, 'required':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

# Twisted Towerのシリアライザー
class TwistedTowerSerializer(serializers.ModelSerializer):
    # 日時系はここで文字列化
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    # 現在のユーザーをデフォルトに設定
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        # モデルを指定
        model = TwistedTower
        fields = ['id', 'title', 'base_curve', 'center_point', 'twisted_tower', 'angle', 'height', 'created_at', 'updated_at', 'created_by']