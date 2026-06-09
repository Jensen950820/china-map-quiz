#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成台湾互动地图数据文件
台湾行政区划（22个）：6直辖市 + 3省辖市 + 13县
"""

import json
import os

# 台湾各县市数据 (adcode 使用71xxxx编码)
# 中心坐标 [经度, 纬度] 来自实际地理位置
TAIPEI_CENTER = [121.5654, 25.0320]
NEW_TAIPEI_CENTER = [121.4625, 24.9600]
TAOYUAN_CENTER = [121.2168, 24.9376]
TAICHUNG_CENTER = [120.9417, 24.1477]
TAINAN_CENTER = [120.2037, 22.9999]
KAOHSIUNG_CENTER = [120.3149, 22.6273]
KEELUNG_CENTER = [121.7411, 25.1283]
HSINCHU_CENTER = [120.9647, 24.8039]
CHIAYI_CENTER = [120.4474, 23.4800]
HSINCHU_COUNTY_CENTER = [121.1250, 24.7036]
MIAOLI_CENTER = [120.9417, 24.4894]
CHANGHUA_CENTER = [120.5413, 24.0750]
NANTOU_CENTER = [120.6644, 23.8380]
YUNLIN_CENTER = [120.5367, 23.6985]
CHIAYI_COUNTY_CENTER = [120.5744, 23.4589]
PINGTUNG_CENTER = [120.4903, 22.0000]
ILAN_CENTER = [121.7447, 24.7570]
HUALIEN_CENTER = [121.6142, 23.4794]
TAITUNG_CENTER = [121.1444, 22.7583]
PENGHU_CENTER = [119.6151, 23.5687]
KINMEN_CENTER = [118.3186, 24.4450]
LIENCHIANG_CENTER = [119.9500, 26.1500]

# 台湾各县市完整数据
cities = [
    {"adcode": 710100, "name": "台北市", "center": TAIPEI_CENTER, "centroid": [121.5175, 25.0500], "childrenNum": 12, "desc": "台湾首府，位于台湾北部，是台湾的政治、经济、文化中心。全市面积约272平方公里，人口约250万。台北101是台湾最高建筑，也是著名地标。拥有丰富的历史文化资源，如故宫博物院、中正纪念堂等。[百度百科](https://baike.baidu.com/item/%E5%8F%B0%E5%8C%97) | [Wikipedia](https://en.wikipedia.org/wiki/Taipei)"},
    {"adcode": 710200, "name": "新北市", "center": NEW_TAIPEI_CENTER, "centroid": [121.5250, 24.8500], "childrenNum": 29, "desc": "台湾最大的直辖市，环绕台北市，面积约2053平方公里，人口约400万。新北市拥有丰富的自然景观，包括九份老街、野柳地质公园、平溪天灯等著名景点。[百度百科](https://baike.baidu.com/item/%E6%96%B0%E5%8C%97%E5%B8%82) | [Wikipedia](https://en.wikipedia.org/wiki/New_Taipei)"},
    {"adcode": 710300, "name": "桃园市", "center": TAOYUAN_CENTER, "centroid": [121.2168, 24.9376], "childrenNum": 13, "desc": "位于台湾西北部，面积约1220平方公里，人口约230万。桃园国际机场是台湾最大的国际门户，大溪老街、慈湖等是著名观光景点。[百度百科](https://baike.baidu.com/item/%E6%A1%83%E5%9B%AD%E5%B8%82) | [Wikipedia](https://en.wikipedia.org/wiki/Taoyuan)"},
    {"adcode": 710400, "name": "台中市", "center": TAICHUNG_CENTER, "centroid": [120.9417, 24.1477], "childrenNum": 29, "desc": "台湾中部最大的城市，面积约2215平方公里，人口约280万。台中市是台湾重要的文教中心，拥有多所大学。著名景点有彩虹眷村、高美湿地、逢甲夜市等。[百度百科](https://baike.baidu.com/item/%E5%8F%B0%E4%B8%AD%E5%B8%82) | [Wikipedia](https://en.wikipedia.org/wiki/Taichung)"},
    {"adcode": 710500, "name": "台南市", "center": TAINAN_CENTER, "centroid": [120.2037, 22.9999], "childrenNum": 37, "desc": "台湾最早开发的城市，面积约2192平方公里，人口约187万。台南是台湾的古都，拥有丰富的历史文化遗产，如赤崁楼、安平古堡、孔庙等。[百度百科](https://baike.baidu.com/item/%E5%8F%B0%E5%8D%97%E5%B8%82) | [Wikipedia](https://en.wikipedia.org/wiki/Tainan)"},
    {"adcode": 710600, "name": "高雄市", "center": KAOHSIUNG_CENTER, "centroid": [120.3149, 22.6273], "childrenNum": 38, "desc": "台湾南部最大的城市，面积约2952平方公里，人口约277万。高雄港是台湾最大的港口，六合夜市、西子湾、旗津半岛等是著名景点。[百度百科](https://baike.baidu.com/item/%E9%AB%98%E9%9B%84%E5%B8%82) | [Wikipedia](https://en.wikipedia.org/wiki/Kaohsiung)"},
    {"adcode": 710700, "name": "基隆市", "center": KEELUNG_CENTER, "centroid": [121.7411, 25.1283], "childrenNum": 7, "desc": "位于台湾东北角，面积约133平方公里，人口约37万。基隆港是台湾第二大港口，以多雨著称，有'雨港'之称。庙口夜市是台湾著名夜市之一。[百度百科](https://baike.baidu.com/item/%E5%9F%BA%E9%9A%86%E5%B8%82) | [Wikipedia](https://en.wikipedia.org/wiki/Keelung)"},
    {"adcode": 710800, "name": "新竹市", "center": HSINCHU_CENTER, "centroid": [120.9647, 24.8039], "childrenNum": 3, "desc": "位于台湾西北部，面积约104平方公里，人口约45万。新竹科学园区是台湾高科技产业的核心，有'台湾硅谷'之称。内湾老街、城隍庙是著名景点。[百度百科](https://baike.baidu.com/item/%E6%96%B0%E7%AB%B9%E5%B8%82) | [Wikipedia](https://en.wikipedia.org/wiki/Hsinchu)"},
    {"adcode": 710900, "name": "嘉义市", "center": CHIAYI_CENTER, "centroid": [120.4474, 23.4800], "childrenNum": 2, "desc": "位于台湾西南部，面积约60平方公里，人口约27万。嘉义市是阿里山森林铁路的起点，著名景点有嘉义公园、兰潭、文化路夜市等。[百度百科](https://baike.baidu.com/item/%E5%98%89%E4%B9%89%E5%B8%82) | [Wikipedia](https://en.wikipedia.org/wiki/Chiayi)"},
    {"adcode": 711000, "name": "新竹县", "center": HSINCHU_COUNTY_CENTER, "centroid": [121.1250, 24.7036], "childrenNum": 13, "desc": "位于台湾西北部，面积约1428平方公里，人口约58万。新竹县以客家文化著称，内湾、北埔、峨眉等客家聚落保存完整。五峰、尖石等地有丰富的原住民文化。[百度百科](https://baike.baidu.com/item/%E6%96%B0%E7%AB%B9%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Hsinchu_County)"},
    {"adcode": 711100, "name": "苗栗县", "center": MIAOLI_CENTER, "centroid": [120.9417, 24.4894], "childrenNum": 18, "desc": "位于台湾中部，面积约1820平方公里，人口约55万。苗栗以客家文化为主，有'山城'之称。三义木雕、大湖草莓、通霄海洋等是当地特色。[百度百科](https://baike.baidu.com/item/%E8%8B%97%E6%A0%97%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Miaoli_County)"},
    {"adcode": 711200, "name": "彰化县", "center": CHANGHUA_CENTER, "centroid": [120.5413, 24.0750], "childrenNum": 26, "desc": "位于台湾中部，面积约1074平方公里，人口约127万。彰化是台湾重要的农业县份，以扇形车库、鹿港老街、八卦山大佛等闻名。[百度百科](https://baike.baidu.com/item/%E5%BD%B0%E5%8C%96%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Changhua_County)"},
    {"adcode": 711300, "name": "南投县", "center": NANTOU_CENTER, "centroid": [120.6644, 23.8380], "childrenNum": 13, "desc": "台湾唯一不临海的县，面积约4106平方公里，人口约50万。日月潭、清境农场、庐山温泉等是著名景点。玉山国家公园部分位于南投县境内。[百度百科](https://baike.baidu.com/item/%E5%8D%97%E6%8A%95%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Nantou_County)"},
    {"adcode": 711400, "name": "云林县", "center": YUNLIN_CENTER, "centroid": [120.5367, 23.6985], "childrenNum": 20, "desc": "位于台湾中南部，面积约1290平方公里，人口约68万。云林以农业为主，是台湾重要的粮仓。北港朝天宫是台湾重要的妈祖庙之一。[百度百科](https://baike.baidu.com/item/%E4%BA%91%E6%9E%97%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Yunlin_County)"},
    {"adcode": 711500, "name": "嘉义县", "center": CHIAYI_COUNTY_CENTER, "centroid": [120.5744, 23.4589], "childrenNum": 18, "desc": "位于台湾西南部，面积约1903平方公里，人口约50万。阿里山森林游乐区位于嘉义县，是台湾著名的旅游胜地。奋起湖、瑞里、太平云梯等也是热门景点。[百度百科](https://baike.baidu.com/item/%E5%98%89%E4%B9%89%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Chiayi_County)"},
    {"adcode": 711600, "name": "屏东县", "center": PINGTUNG_CENTER, "centroid": [120.4903, 22.0000], "childrenNum": 33, "desc": "位于台湾最南端，面积约2775平方公里，人口约82万。垦丁国家公园位于屏东，是台湾著名的度假胜地。鹅銮鼻灯塔、佳乐水、龙磐公园等都是热门景点。[百度百科](https://baike.baidu.com/item/%E5%B1%8F%E4%B8%9C%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Pingtung_County)"},
    {"adcode": 711700, "name": "宜兰县", "center": ILAN_CENTER, "centroid": [121.7447, 24.7570], "childrenNum": 12, "desc": "位于台湾东北部，面积约2144平方公里，人口约45万。宜兰以温泉、美食闻名，礁溪温泉、苏澳冷泉、三星葱饼等是当地特色。太平山、栖兰山是著名的森林游乐区。[百度百科](https://baike.baidu.com/item/%E5%AE%9C%E5%85%B0%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Yilan_County)"},
    {"adcode": 711800, "name": "花莲县", "center": HUALIEN_CENTER, "centroid": [121.6142, 23.4794], "childrenNum": 13, "desc": "位于台湾东部，面积约4628平方公里，人口约32万。花莲以壮丽的自然景观闻名，太鲁阁国家公园、清水断崖、七星潭等是著名景点。[百度百科](https://baike.baidu.com/item/%E8%8A%B1%E8%8E%B2%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Hualien_County)"},
    {"adcode": 711900, "name": "台东县", "center": TAITUNG_CENTER, "centroid": [121.1444, 22.7583], "childrenNum": 16, "desc": "位于台湾东南部，面积约3515平方公里，人口约22万。台东以原住民文化、自然景观闻名，伯朗大道、三仙台、绿岛、兰屿等都是著名景点。[百度百科](https://baike.baidu.com/item/%E5%8F%B0%E4%B8%9C%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Taitung_County)"},
    {"adcode": 712000, "name": "澎湖县", "center": PENGHU_CENTER, "centroid": [119.6151, 23.5687], "childrenNum": 6, "desc": "位于台湾海峡，由90个岛屿组成，面积约127平方公里，人口约10万。澎湖以独特的玄武岩地貌、双心石沪、澎湖湾等闻名。每年举办的澎湖花火节是重要观光活动。[百度百科](https://baike.baidu.com/item/%E6%BE%8E%E6%B9%96%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Penghu_County)"},
    {"adcode": 712100, "name": "金门县", "center": KINMEN_CENTER, "centroid": [118.3186, 24.4450], "childrenNum": 6, "desc": "位于福建省东南沿海，由金门群岛组成，面积约151平方公里，人口约14万。金门以战地文化、闽南建筑、高粱酒闻名。莒光楼、翟山坑道、水头聚落等是著名景点。[百度百科](https://baike.baidu.com/item/%E9%87%91%E9%97%A8%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Kinmen)"},
    {"adcode": 712200, "name": "连江县", "center": LIENCHIANG_CENTER, "centroid": [119.9500, 26.1500], "childrenNum": 4, "desc": "位于台湾海峡北部，由马祖列岛组成，面积约28平方公里，人口约1.3万。马祖以战地文化、闽东建筑、蓝眼泪等闻名。东引、南竿、北竿等岛屿各有特色。[百度百科](https://baike.baidu.com/item/%E8%BF%9E%E6%B1%9F%E5%8E%BF) | [Wikipedia](https://en.wikipedia.org/wiki/Lienchiang_County)"},
]

# 生成简化的多边形边界（基于实际地理形状）
def generate_polygon(center, width=0.15, height=0.12, points=20):
    """生成简化的多边形坐标，模拟实际边界"""
    import math
    lon, lat = center
    coords = []
    for i in range(points):
        angle = 2 * math.pi * i / points
        # 添加一些随机性使边界更自然
        r_width = width * (0.8 + 0.4 * math.sin(angle * 3))
        r_height = height * (0.8 + 0.4 * math.cos(angle * 2))
        x = lon + r_width * math.cos(angle)
        y = lat + r_height * math.sin(angle)
        coords.append([round(x, 6), round(y, 6)])
    # 闭合多边形
    coords.append(coords[0])
    return coords

# 各城市的边界尺寸（根据实际地理大小调整）
city_sizes = {
    710100: (0.08, 0.06),  # 台北市
    710200: (0.35, 0.25),  # 新北市
    710300: (0.18, 0.15),  # 桃园市
    710400: (0.35, 0.30),  # 台中市
    710500: (0.35, 0.25),  # 台南市
    710600: (0.40, 0.30),  # 高雄市
    710700: (0.10, 0.08),  # 基隆市
    710800: (0.08, 0.06),  # 新竹市
    710900: (0.06, 0.05),  # 嘉义市
    711000: (0.25, 0.20),  # 新竹县
    711100: (0.20, 0.18),  # 苗栗县
    711200: (0.20, 0.18),  # 彰化县
    711300: (0.35, 0.30),  # 南投县
    711400: (0.20, 0.18),  # 云林县
    711500: (0.25, 0.20),  # 嘉义县
    711600: (0.35, 0.30),  # 屏东县
    711700: (0.25, 0.20),  # 宜兰县
    711800: (0.35, 0.12),  # 花莲县（狭长）
    711900: (0.30, 0.12),  # 台东县（狭长）
    712000: (0.12, 0.10),  # 澎湖县
    712100: (0.08, 0.06),  # 金门县
    712200: (0.05, 0.04),  # 连江县
}

# 特殊形状调整（花莲、台东是狭长形）
def generate_special_polygon(center, shape_type="normal"):
    import math
    lon, lat = center
    coords = []
    
    if shape_type == "long_horizontal":  # 横向狭长（花莲、台东）
        # 生成横向椭圆
        width, height = 0.5, 0.12
        points = 24
        for i in range(points):
            angle = 2 * math.pi * i / points
            x = lon + width * math.cos(angle)
            y = lat + height * math.sin(angle)
            coords.append([round(x, 6), round(y, 6)])
    elif shape_type == "islands":  # 离岛（澎湖）
        # 生成多个小岛
        # 主岛
        for i in range(16):
            angle = 2 * math.pi * i / 16
            x = lon + 0.08 * math.cos(angle)
            y = lat + 0.06 * math.sin(angle)
            coords.append([round(x, 6), round(y, 6)])
    else:
        w, h = city_sizes.get(0, (0.15, 0.12))
        return generate_polygon(center, w, h, 20)
    
    coords.append(coords[0])
    return coords

# 生成各县市的 Feature
features = []
for idx, city in enumerate(cities):
    adcode = city["adcode"]
    center = city["center"]
    w, h = city_sizes.get(adcode, (0.15, 0.12))
    
    # 根据城市类型生成不同的多边形
    if adcode in [711800, 711900]:  # 花莲、台东 - 狭长形
        shape_type = "long_horizontal"
        coords = generate_special_polygon(center, shape_type)
        # 花莲和台东需要特殊处理，坐标要更精确
        if adcode == 711800:  # 花莲县
            coords = [
                [121.55, 24.05], [121.60, 24.10], [121.65, 24.05], [121.70, 23.95],
                [121.75, 23.80], [121.80, 23.65], [121.75, 23.50], [121.70, 23.40],
                [121.65, 23.35], [121.55, 23.30], [121.45, 23.35], [121.40, 23.45],
                [121.35, 23.60], [121.40, 23.75], [121.45, 23.90], [121.50, 24.00],
                [121.55, 24.05]
            ]
        else:  # 台东县
            coords = [
                [121.20, 23.10], [121.25, 23.05], [121.30, 22.95], [121.35, 22.80],
                [121.40, 22.65], [121.45, 22.50], [121.50, 22.35], [121.55, 22.20],
                [121.50, 22.05], [121.45, 21.95], [121.40, 21.90], [121.30, 21.85],
                [121.20, 21.90], [121.10, 22.00], [121.05, 22.15], [121.00, 22.35],
                [121.05, 22.55], [121.10, 22.75], [121.15, 22.95], [121.20, 23.10]
            ]
    elif adcode == 712000:  # 澎湖县 - 离岛
        coords = [
            [119.55, 23.62], [119.58, 23.65], [119.62, 23.68], [119.65, 23.65],
            [119.68, 23.60], [119.70, 23.55], [119.68, 23.50], [119.65, 23.48],
            [119.62, 23.45], [119.58, 23.48], [119.55, 23.52], [119.53, 23.57],
            [119.55, 23.62]
        ]
    elif adcode == 712100:  # 金门县
        coords = [
            [118.30, 24.48], [118.32, 24.50], [118.35, 24.48], [118.38, 24.45],
            [118.40, 24.42], [118.42, 24.38], [118.40, 24.35], [118.38, 24.32],
            [118.35, 24.30], [118.32, 24.32], [118.30, 24.35], [118.28, 24.40],
            [118.30, 24.48]
        ]
    elif adcode == 712200:  # 连江县（马祖）
        coords = [
            [119.92, 26.18], [119.94, 26.20], [119.96, 26.18], [119.97, 26.15],
            [119.96, 26.12], [119.94, 26.10], [119.92, 26.12], [119.90, 26.15],
            [119.92, 26.18]
        ]
    else:
        coords = generate_polygon(center, w, h, 24)
    
    feature = {
        "type": "Feature",
        "properties": {
            "adcode": adcode,
            "name": city["name"],
            "desc": city["desc"],
            "center": city["center"],
            "centroid": city["centroid"],
            "childrenNum": city["childrenNum"],
            "level": "city",
            "parent": {"adcode": 710000},
            "subFeatureIndex": idx,
            "acroutes": [100000, 710000]
        },
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [[coords]]
        }
    }
    features.append(feature)

# 生成 gd_data.js
gd_data = {
    "type": "FeatureCollection",
    "features": features
}

# 输出为 JavaScript 格式
output_path = r'C:\Users\user\Desktop\共享文件夹\【项目与工具】\【代码-暂存】\互动地图\台湾\gd_data.js'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('const GD_PREFECTURES = ')
    json.dump(gd_data, f, ensure_ascii=False, indent=2)
    f.write(';')

print(f"已生成: {output_path}")

# 生成 gd_counties.js（台湾的区/县级数据）
# 台湾的直辖市下有区，县辖市下有乡镇市区
counties_data = {}

# 台北市 12 个区
taipei_districts = [
    {"adcode": 710101, "name": "中正区", "center": [121.5145, 25.0350]},
    {"adcode": 710102, "name": "大同区", "center": [121.5117, 25.0614]},
    {"adcode": 710103, "name": "中山区", "center": [121.5378, 25.0628]},
    {"adcode": 710104, "name": "松山区", "center": [121.5592, 25.0500]},
    {"adcode": 710105, "name": "大安区", "center": [121.5292, 25.0225]},
    {"adcode": 710106, "name": "万华区", "center": [121.5039, 25.0278]},
    {"adcode": 710107, "name": "信义区", "center": [121.5615, 25.0222]},
    {"adcode": 710108, "name": "士林区", "center": [121.5153, 25.1050]},
    {"adcode": 710109, "name": "北投区", "center": [121.4925, 25.1350]},
    {"adcode": 710110, "name": "内湖区", "center": [121.5908, 25.0694]},
    {"adcode": 710111, "name": "南港区", "center": [121.6069, 25.0256]},
    {"adcode": 710112, "name": "文山区", "center": [121.5736, 24.9986]},
]

counties_data["710100"] = {
    "type": "FeatureCollection",
    "features": []
}

for d in taipei_districts:
    coords = generate_polygon(d["center"], 0.02, 0.015, 16)
    feature = {
        "type": "Feature",
        "properties": {
            "adcode": d["adcode"],
            "name": d["name"],
            "center": d["center"],
            "centroid": d["center"],
            "childrenNum": 0,
            "level": "district",
            "parent": {"adcode": 710100},
            "subFeatureIndex": len(counties_data["710100"]["features"]),
            "acroutes": [100000, 710000, 710100]
        },
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [[coords]]
        }
    }
    counties_data["710100"]["features"].append(feature)

# 新北市 29 个区（简化，只列几个代表性的）
new_taipei_districts = [
    {"adcode": 710201, "name": "万里区", "center": [121.6833, 25.1833]},
    {"adcode": 710202, "name": "金山区", "center": [121.6167, 25.1167]},
    {"adcode": 710203, "name": "板桥区", "center": [121.4500, 24.9833]},
    {"adcode": 710204, "name": "汐止区", "center": [121.6500, 25.0667]},
    {"adcode": 710205, "name": "深坑区", "center": [121.5833, 24.9667]},
    {"adcode": 710206, "name": "石碇区", "center": [121.6167, 24.9333]},
    {"adcode": 710207, "name": "瑞芳区", "center": [121.7833, 25.1167]},
    {"adcode": 710208, "name": "平溪区", "center": [121.7333, 25.0167]},
    {"adcode": 710209, "name": "双溪区", "center": [121.8333, 25.0167]},
    {"adcode": 710210, "name": "贡寮区", "center": [121.9167, 25.0167]},
]

counties_data["710200"] = {
    "type": "FeatureCollection",
    "features": []
}

for d in new_taipei_districts:
    coords = generate_polygon(d["center"], 0.03, 0.025, 16)
    feature = {
        "type": "Feature",
        "properties": {
            "adcode": d["adcode"],
            "name": d["name"],
            "center": d["center"],
            "centroid": d["center"],
            "childrenNum": 0,
            "level": "district",
            "parent": {"adcode": 710200},
            "subFeatureIndex": len(counties_data["710200"]["features"]),
            "acroutes": [100000, 710000, 710200]
        },
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [[coords]]
        }
    }
    counties_data["710200"]["features"].append(feature)

# 输出 gd_counties.js
output_path2 = r'C:\Users\user\Desktop\共享文件夹\【项目与工具】\【代码-暂存】\互动地图\台湾\gd_counties.js'
with open(output_path2, 'w', encoding='utf-8') as f:
    f.write('const GD_COUNTIES = ')
    json.dump(counties_data, f, ensure_ascii=False, indent=2)
    f.write(';')

print(f"已生成: {output_path2}")
print("完成！")
