import pandas
import requests
from bs4 import BeautifulSoup
from haversine import haversine
import folium
import webbrowser
import googlemaps
import time
import math
import pandas as pd
from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import Polygon

start_time = time.time()
kaptCode_list = ['A12009201', 'A12009202', 'A12009203', 'A12009303', 'A12009304', 'A12009305', 'A12010101', 'A12010202',
                 'A12010203', 'A12011002', 'A12012001', 'A12012101', 'A12012202', 'A12013001', 'A12013002', 'A12013003',
                 'A12013101', 'A12013201', 'A12013202', 'A12017001', 'A12070201', 'A12071001', 'A12071003', 'A12071101',
                 'A12071102', 'A12072801', 'A12072802', 'A12076401', 'A12076601', 'A12078201', 'A12078704', 'A12078705',
                 'A12078706', 'A12079501', 'A12079601', 'A12081602', 'A12081703', 'A12084504', 'A12085303', 'A12086001',
                 'A12101001', 'A12102002', 'A12102005', 'A12102008', 'A12103006', 'A12104005', 'A12105001', 'A12106001',
                 'A12109001', 'A12111001', 'A12112001', 'A12114001', 'A12115001', 'A12119006', 'A12125001', 'A12125202',
                 'A12127001', 'A12127002', 'A12127003', 'A12127004', 'A10028201', 'A10044001', 'A10044002', 'A10045001',
                 'A10045002', 'A10045301', 'A10045402', 'A10045403', 'A10045404', 'A10072501', 'A10078102', 'A10078103',
                 'A10078901', 'A10078902', 'A10085902', 'A10085903', 'A10086301', 'A10086801', 'A10088101', 'A10088102',
                 'A11001203', 'A11005401', 'A11007001', 'A11014001', 'A11034001']  # 단지코드 리스트

kaptName_list = []  # 단지명 리스트
kaptdaCnt_list = []  # 세대수 리스트
addr_list = []

final_lat = []
final_lng = []

for code in kaptCode_list:
    url = 'http://apis.data.go.kr/1613000/AptBasisInfoService1/getAphusBassInfo?kaptCode={}&numOfRows=100000&pageNo=1&ServiceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'.format(code)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    item = soup.find('item')

    try:
        kaptName = item.find('kaptname').text  # 단지명
        kaptName_list.append(kaptName)
    except:
        kaptName_list.append('주택')

    try:
        addr = item.find('kaptaddr').text
        addr_list.append(addr)
    except:
        addr_list.append('none')

    try:
        kaptdaCnt = item.find('kaptdacnt').text  # 세대 수
        kaptdaCnt_list.append(kaptdaCnt)
    except:
        kaptdaCnt_list.append('0')

for address in addr_list:
    if address == 'none':
        print('none')
    else:

        gmaps = googlemaps.Client(key='AIzaSyCJV-ePI7fojeb_eeNZmbnzdktl2SozkLI')
        geo_location = gmaps.geocode(address)[0].get('geometry')

        lat = geo_location['location']['lat']
        lng = geo_location['location']['lng']
        final_lat.append(lat)
        final_lng.append(lng)

# for i in range(len(final_lat)):
#     print(kaptName_list[i-1], kaptdaCnt_list[i-1], (final_lat[i-1], final_lng[i-1]))

data =pandas.concat([pandas.DataFrame({'거주명':kaptName_list}), pandas.DataFrame({'동 수':kaptdaCnt_list}), pandas.DataFrame({'위도':final_lat}), pandas.DataFrame({'경도':final_lng})], axis = 1) # 데이터 프레임으로 변환


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
points = [(37.5741357, 127.0143296), (37.580401, 127.0139816), (37.6109493, 126.9786561)] # 편의점 추천 자리 좌표
# 중점(long, lat)
centers = [(37.6109493, 126.9786561), (37.5743814, 126.9686187), (37.5732644, 126.9719961), (37.580401, 127.0139816), (37.5749752, 126.9812194), (37.5887107, 126.9228244)]
polygons = [] # 주거지 기반으로 형성된 다수의 폴리건 리스트
# 주거지 좌표로 세대수에 따른 폴리곤 생성
for idx in range(len(kaptName_list)):
    if int(kaptdaCnt_list[idx-1]) < 400: # 세대수가 400 미만이면 반경 = 140
        d = 140
    elif int(kaptdaCnt_list[idx-1]) >= 400: # 세대수가 400이상이면 반경 = 340
        d = 340
    c = (final_lat[idx-1], final_lng[idx-1])
    rotating_degree = 45
    offsets = calc_offsets(d, c[1])
    coordinates = [coordinate_after_rotation(c, d, offsets) for d in range(0, 360+1, rotating_degree)]
    polygon_idx = Polygon(coordinates)
    polygons.append(polygon_idx)
# 편의점 좌표가 폴리건 안에 포함되는지 여부 확인
# 편의점 좌표가 폴리건 안에 있으면 그에 해당하는 주거지 명, 세대수, 좌표 출력
for poly in polygons:
    for point in points:
        if poly.contains(Point(point)):
            print(poly.contains(Point(point)))
            print(point)
            a = polygons.index(poly)
            print(kaptName_list[a-1])
            print(kaptdaCnt_list[a-1])
        else:
            continue


elapsed_time = time.time() - start_time
print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))