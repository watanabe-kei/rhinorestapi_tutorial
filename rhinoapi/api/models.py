from django.db import models
from django.contrib.auth.models import User

class TwistedTower(models.Model):
    # タイトル
    title = models.CharField(max_length=50)
    # ベースカーブ
    base_curve = models.TextField(blank=True)
    # 中心点
    center_point = models.TextField(blank=True)
    # タワー
    twisted_tower = models.TextField(blank=True)
    # ねじれ角度
    angle = models.CharField(max_length=50)
    # タワーの高さ
    height = models.CharField(max_length=50)   
    # 作成日
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日
    updated_at = models.DateTimeField(auto_now=True)
    # 作成者
    created_by = models.ForeignKey(User, null= True, blank= True, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title