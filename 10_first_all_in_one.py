import requests
from bs4 import BeautifulSoup
from haversine import haversine
import folium
import webbrowser
import googlemaps
import time
import math
from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import Polygon
start_time = time.time()
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 4 - 시도별 편의점 좌표 가져와서 일정 거리 이상 떨어져있는 편의점 사이에 중앙점 좌표 구하기 - mid_point_list 에 저장
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Seoul = 11
Busan = 21
Daegu = 22
Incheon = 23
Gwangju = 24
Daejeon_Metropolitan_City = 25
Ulsan_Metropolitan_City = 26
Sejong_Special_Self_Governing_City = 29
Gyeonggi = 31
Gangwon_do = 32
Chungcheongbuk_do = 33
Chungcheongnam_do = 34
Jeollabuk_do = 35
Jeollanam_do = 36
Gyeongsangbuk_do = 37
Gyeongsangnam_do = 38
Jeju_Special_Self_Governing_Province = 39

city_code = Seoul

bizesnmList = []
lonList = []
latList = []
for_total_url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong?divId=ctprvnCd&key=11&indsSclsCd=D03A01&divId=ctprvnCd&numOfRows=100000&pageNo=1&type=xml&serviceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'
total_response = requests.get(for_total_url)
total_response.raise_for_status()
soup = BeautifulSoup(total_response.text, 'html.parser')
total = soup.find('total')
for i in range(1, 10):
    url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong?divId=ctprvnCd&key={}&indsSclsCd=D03A01&divId=ctprvnCd&numOfRows=1000&pageNo={}&type=xml&serviceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'.format(city_code, i)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    ItemList = soup.findAll('item')

    for item in ItemList:
        
        bizesnm = item.find('bizesnm').text
        lat = item.find('lat').text  # 위도 ex) 37
        lon = item.find('lon').text  # 경도 ex) 137

        bizesnmList.append(bizesnm)
        lonList.append(lon)
        latList.append(lat)

couple = [] # distance 의 짝궁 : 각 값당 두개의 위도, 경도
distance = [] # 인접한 두 편의점 거리 모음
for i in range(len(lonList)):
    spot = (float(latList[i-1]), float(lonList[i-1])) # (위도, 경도)
    sec_list = [] # spot 과 compares 거리 계산 값
    couple_list = [] # spot 과 compares 의 값[(spot), (compares)]
    for sec in range(len(lonList)):
        compares = (float(latList[sec-1]), float(lonList[sec-1])) # (위도, 경도) : spot 과 같은 값, spot 과 거리 계산을 위해 작성
        sec_list.append(haversine(spot, compares, unit='m')) # spot 과 compares 의 거리를 m 로 계산한 값을 sec_list 로
        couple_list.append([spot, compares]) # index 값이 각 i-1 과 sec-1 인 값의 두개의 위도, 경도 값을 couple_list 로

    def findIndexInList(list_name, value): # 리스트 안에 있는 값의 모든 인덱스 result에 저장
        n = -1
        result = []
        while True:
            if list_name[n + 1:].count(value) == 0:
                break
            n += list_name[n + 1:].index(value) + 1
            result.append(n)
        return result


    zero_value_idx = findIndexInList(sec_list, 0) # sec_list 에서의 거리 값과 couple_list 에서의 두개의 위도, 경도 값의 인덱스가 세트이기 때문에 아래 sec_list에서 0을 제거 해야하기때문에 이에 알맞은 인덱스 값을 구함
    sec_list.remove(0) # 같은 위도 경도 간의 거리를 구한 값을 제거
    for idx in zero_value_idx: # zero_value_idx 값이 sec_list에서 제거당한 0의 인덱스 값과 일치하기 때문에 제거
        idx -= zero_value_idx.index(idx) # 리스트에 있는 인덱스 값이 하나씩 지워지면서 인덱스 위치가 맞지 않아 맞춰줌
        del couple_list[idx] # i = sec_list 에 0의 인덱스 값
    min_dist = min(sec_list) # sec_list 에서 가장 작은 값을 min_dist 에 저장
    distance.append(min_dist) # min_dist 값을 distance 에 append
    min_index = sec_list.index(min_dist) # sec_list(가장 인접한 거리 값 리스트) 중 가장 작은 값의 인덱스를 min_index에 저장
    couple.append(couple_list[min_index]) # distance 에 올라간 값과 세트되는 두개의 위도, 경도 를 couple에 저장
# print(distance)
distance_sum = sum(distance)
dis_avg = distance_sum / len(distance)
# print(couple)
# print(dis_avg)

# 거리가 200이 넘어가는 값을 찾아내는 함수
def up_200(num):
    if num >= int(dis_avg)*3 :
        return num
    else :
        return

dist_far = [] # 거리가 200이 넘어가는 값들
dist_far_spot = [] # dist_far 값들에 해당하는 두 세트의 위도 경도
for i in range(len(distance)): # distance 값들 중에서
    if up_200(distance[i-1]): # 200이 넘어가는 값이 있으면
        dist_far.append(distance[i-1]) # 그 값을 dist_far 에 append
        dist_far_spot.append(couple[i-1]) # dist_far 과 짝궁인 두 세트의 위도, 경도 값을 가져옴

def midpoint_euclidean(t): # 두개의 위도 중앙점을 찾는 함수
    dist_x = abs(t[0][0] - t[1][0]) / 2.
    dist_y = abs(t[0][1] - t[1][1]) / 2.
    res_x = t[0][0] - dist_x if t[0][0] > t[1][0] else t[1][0] - dist_x
    res_y = t[0][1] - dist_y if t[0][1] > t[1][1] else t[1][1] - dist_y
    return [res_x, res_y]

mid_point_list = [] # 거리가 200이 넘는 좌표 세트의 중앙 좌표
for i in range(len(dist_far)): # 거리가 200이 넘어가는 값들의 개수동안
    # print(dist_far[i-1], dist_far_spot[i-1]) # 200이 넘어가는 값과, 그에 해당하는 위도, 경도 출력
    mid_point = midpoint_euclidean(dist_far_spot[i - 1]) # 200이 넘어가는 위도 경도를 중앙점을 찾는 함수에 대입하여 mid_point에 삽입
    # print(dist_far[i-1], mid_point) # 거리가 200이 넘어가는 거리값과 중앙점 좌표 출력
    mid_point_list.append(mid_point)
# print(mid_point_list) # 거리가 200이 넘는 좌표 세트의 중앙 좌표 출력
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 5 - 단지코드, 단지명을 kaptCode_list 와 kaptName_list에 저장
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

kaptCode_list = [] # 서울시 모든 단지코드 리스트
# kaptName_list = [] # 서울시 모든 단지명 리스트

for i in range(1, 4):
    url = 'http://apis.data.go.kr/1613000/AptListService2/getSidoAptList?sidoCode={}&numOfRows=100000&pageNo={}&ServiceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'.format(city_code, i)
    # url = 'http://apis.data.go.kr/1613000/AptListService2/getSidoAptList?sidoCode={}&numOfRows=100000&pageNo={}&type=xml&ServiceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'.format(city_code, i)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    ItemList = soup.findAll('item')

    for item in ItemList:
        kaptCode = item.find('kaptcode').get_text()  # 단지코드
        # kaptName = item.find('kaptname').get_text()  # 단지명

        kaptCode_list.append(kaptCode)
        # kaptName_list.append(kaptName)
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 7 - 단지코드로부터의 단지명, 세대수, 법정동코드 와 이에 해당하는 좌표를 final_lat 과 final_lng 리스트에 저장
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
kaptName_list = []  # 단지명 리스트
kaptdaCnt_list = []  # 세대수 리스트
# kaptDongCnt_list = []  # 동수 리스트
# doroJuso_list = []  # 도로명 주소 리스트
addr_list = []

final_lat = []
final_lng = []

for code in kaptCode_list:
    url = 'http://apis.data.go.kr/1613000/AptBasisInfoService1/getAphusBassInfo?kaptCode={}&numOfRows=1000&pageNo=1&ServiceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'.format(code)
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

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 9 - 주거단지 좌표 중심으로 폴리곤 형성 후 그 폴리건 안에 편의점 중앙좌표가 들어가는지 확인 and 지도에 표시하기까지
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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
polygons = [] # 주거지 기반으로 형성된 다수의 폴리건 리스트
# 주거지 좌표로 세대수에 따른 폴리곤 생성
for idx in range(len(kaptName_list)):
    if int(kaptdaCnt_list[idx - 1]) < 400:  # 세대수가 400 미만이면 반경 = 140
        d = 140
    elif int(kaptdaCnt_list[idx - 1]) >= 400:  # 세대수가 400이상이면 반경 = 340
        d = 340
    c = (final_lat[idx-1], final_lng[idx-1])
    rotating_degree = 45
    offsets = calc_offsets(d, c[1])
    coordinates = [coordinate_after_rotation(c, d, offsets) for d in range(0, 360+1, rotating_degree)]
    polygon_idx = Polygon(coordinates)
    polygons.append(polygon_idx)
# 편의점 좌표가 폴리건 안에 포함되는지 여부 확인
# 편의점 좌표가 폴리건 안에 있으면 그에 해당하는 주거지 명, 세대수, 좌표 출력
selected_kaptName_list = []
selected_kaptdaCnt_list = []
selected_mid_point_list = []
for poly in polygons:
    for point in mid_point_list:
        if poly.contains(Point(point)):
            print(poly.contains(Point(point)))
            print(point)
            a = polygons.index(poly)
            print(kaptName_list[a-1])
            print(kaptdaCnt_list[a-1])
            selected_kaptName_list.append(kaptName_list[a - 1])
            selected_kaptdaCnt_list.append(kaptdaCnt_list[a - 1])
            selected_mid_point_list.append(point)

        else:
            continue

m = folium.Map(location=[37.551348, 126.988259], # 지도 만들기, 시작 포인트
               zoom_start=10,
               )
for i in selected_mid_point_list: # 거리가 200이 넘어가는 중앙값 좌표들
    folium.CircleMarker(i,
                        icon = folium.Icon(color='red'),
                        radius= (dis_avg//2),
                        color= 'blue',
                        fill_color= 'blue',
                        popup= selected_kaptdaCnt_list[selected_mid_point_list.index(i)]).add_to(m) # 마커 만들기
convi_map = "selected_map.html"
m.save(convi_map)
webbrowser.open(convi_map)

elapsed_time = time.time() - start_time
print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))