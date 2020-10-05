# -*- coding: utf-8 -*-
import Rhino
import Rhino.Geometry as rg
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

title = 'test01'
url = 'http://127.0.0.1:8000/api/twisted_tower/get/?'
# "YOUR_TOKEN"を書き換えてください
token = 'Token YOUR_TOKEN'
values = {'title': title}
headers = {'Authorization': token}


data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
response = urllib2.urlopen(req)
res = response.read()
res_dict = json.loads(res)
title = res_dict['title']
twisted_tower_json = json.loads(res_dict['twisted_tower'])
# Rhinoオブジェクトに変換
twisted_tower = Newtonsoft.Json.JsonConvert.DeserializeObject(twisted_tower_json, rg.Brep)
# Rhinoに追加
sc.doc.Objects.AddBrep(twisted_tower)
# 再描画
sc.doc.Views.Redraw()

