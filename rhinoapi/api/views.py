from django.contrib import auth
from django.http import request
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer

from .models import TwistedTower
from .serializers import UserSerializer, TwistedTowerSerializer
from .rhino_commands.commands import twisted_tower_command
# 後で書きます
from .ownpermissions import ProfilePermission

# ユーザーのviewset
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (ProfilePermission,)
	
# Twisted Towerのviewset
class TwistedTowerViewSet(viewsets.ModelViewSet):
    # モデル
    queryset = TwistedTower.objects.all()
    # シリアライザー
    serializer_class = TwistedTowerSerializer
    # ユーザー認証
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Twisted TowerをつくるAPI
    @action(methods=["post"], detail=False)
    def create_twisted_tower(self, request):
        # リクエストからパラメータを取得
        user = request.user
        title = request.data['title']
        base_curve = request.data['base_curve']
        center_point = request.data['center_point']
        angle = request.data['angle']
        height = request.data['height']
        twisted_tower = twisted_tower_command(base_curve, center_point, float(angle), float(height))

        # 今回は検証のため既存のモデルのデータは毎回削除する
        pre_vm = TwistedTower.objects.all()
        pre_vm.delete()
        # モデルを作成
        item = TwistedTower(title=title, base_curve=base_curve, center_point=center_point, twisted_tower=twisted_tower, angle=angle, height=height,created_by=user)
        item.save()

        # シリアライズ
        serializer = TwistedTowerSerializer(data={"title": title, "base_curve":base_curve, "center_point":center_point, "twisted_tower":twisted_tower,
                                                    'angle':angle, 'height':height}, context={'request': request})
        
        # シリアライザが有効なら200、無効なら400を返す
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DBにあるモデルを参照
    # rhinoのurllib2がdata付きでGETたたけないのでPOSTで代用
    @action(methods=["post"], detail=False)
    def get(self, request):
        user = request.user
        title = request.data['title']

        # リクエストから取得したタイトルのモデルを取得
        vm = TwistedTower.objects.filter(title = title, created_by = user)[0]
        # シリアライズ
        serializer = TwistedTowerSerializer(vm)
        # データを返す
        return Response(serializer.data, status=status.HTTP_200_OK)