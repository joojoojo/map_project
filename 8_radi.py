import math
import pandas as pd
from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import Polygon

# 1. haversine distance 식을 이용해 반경에 따른 geography상의 x축과 y축의 오프셋 값을 구한다.
# pi는 math.acos(-1)를 사용해도 무방
def calc_offsets(d, lat):
    return (
        abs(360*math.asin(math.sin(d/6371/2/1000)/math.cos(lat*math.pi/180))/math.pi),
        180*d/6371/1000/math.pi
    )
# 2. 오프셋을 이용해 특정각도로 회전시킨후의 경도와 위도를 구할수 있도록 한다.
def radian(degree):
    return math.acos(-1)/180*degree

# 3. 0~360도까지 45도씩 증가시켜가면서 2.의 처리를 반복해 좌표를 생성한다.
def coordinate_after_rotation(c, degree, offsets):
    return (
        c[0]+math.cos(radian(degree))*offsets[0],
        c[1]+math.sin(radian(degree))*offsets[1]
    )
# 중점(long, lat)
c = (37.5887107, 126.9228244)
# 반경(meter)
d = 100
rotating_degree = 45
offsets = calc_offsets(d, c[1])
coordinates = [coordinate_after_rotation(c, d, offsets) for d in range(0, 360+1, rotating_degree)]
polygon = Polygon(coordinates)

a = polygon.contains(Point(37.8887107, 126.9228245))
print(a)