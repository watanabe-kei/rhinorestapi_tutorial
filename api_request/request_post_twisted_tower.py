
# -*- coding: utf-8 -*-
import Rhino
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import scriptcontext as sc
import System
import json
import clr
import urllib
import urllib2

# Rhinoのバージョンを確認
rhino_version = str(Rhino.RhinoApp.Version)[0]
# .Net FrameworkのJsonシリアライザー
if rhino_version == '6':
    clr.AddReference('Newtonsoft.Json')
elif rhino_version == '7':
    clr.AddReference('Newtonsoft.Json.Rhino')
import Newtonsoft.Json


# ベースカーブ
base_curve = rs.coercecurve(rs.GetObject(message="select base curve"))
# 回転させる中心点
center_point = rg.AreaMassProperties.Compute(base_curve).Centroid
# 角度
angle = 30
# 高さ
height = 100
# シリアライズ
base_curve_json = json.dumps(Newtonsoft.Json.JsonConvert.SerializeObject(base_curve))
center_point_json = json.dumps(Newtonsoft.Json.JsonConvert.SerializeObject(center_point))

# HTTPリクエスト
url = 'http://127.0.0.1:8000/api/twisted_tower/create_twisted_tower/'
# "YOUR_TOKEN"を書き換えてください
token = 'Token YOUR_TOKEN'
values = {'title': 'test01',
          'base_curve': base_curve_json,
          'center_point': center_point_json,
          'angle': angle,
          'height': height}
headers = {'Authorization': token}
# エンコード
data = urllib.urlencode(values)
# リクエストを作成
req = urllib2.Request(url, data, headers)
# リクエスト
response = urllib2.urlopen(req)
# レスポンスをdictonaryに変換
res = response.read()
res_dict = json.loads(res)
# パラメータを取得
title = res_dict['title']
twisted_tower_json = json.loads(res_dict['twisted_tower'])
# Rhinoオブジェクトに変換
twisted_tower = Newtonsoft.Json.JsonConvert.DeserializeObject(twisted_tower_json, rg.Brep)
# Rhinoに追加
sc.doc.Objects.AddBrep(twisted_tower)
# 再描画
sc.doc.Views.Redraw()

