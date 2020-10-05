import rhinoinside
rhinoinside.load()
import Rhino.Geometry as rg
import System
import Newtonsoft.Json
import json
import math

def twisted_tower_command(base_curve_json, center_point_json, angle, height):
    # desirialize : stringをjsonに戻してからRhinoオブジェクトに変換
    base_curve = Newtonsoft.Json.JsonConvert.DeserializeObject(json.loads(base_curve_json), rg.Curve)
    center_point = Newtonsoft.Json.JsonConvert.DeserializeObject(json.loads(center_point_json), rg.Point3d)
    # 角度をラジアンに変換
    rad = math.radians(angle)
    # 回転させるtransform
    print(rad, rg.Vector3d(0.0,0.0,1.0), center_point)
    rotation = rg.Transform.Rotation(rad, rg.Vector3d(0.0,0.0,1.0), center_point)
    # 上に動かすtransform
    move = rg.Transform.Translation(0.0,0.0,height)
    # transformを結合
    trns = rg.Transform.Multiply(rotation, move)
    # 上のカーブを作成
    top_curve = base_curve.Duplicate()
    top_curve.Transform(trns)
    # カーブのリスト
    curvs = System.Collections.Generic.List[rg.Curve]()
    curvs.Add(base_curve)
    curvs.Add(top_curve)
    # ロフト
    loft = rg.Brep.CreateFromLoft(curvs, rg.Point3d.Unset, rg.Point3d.Unset, rg.LoftType.Normal,False)[0]
    # シリアライズして更にstringに変換
    loft_json = json.dumps(Newtonsoft.Json.JsonConvert.SerializeObject(loft))
    return loft_json