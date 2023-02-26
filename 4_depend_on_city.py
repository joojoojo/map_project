import pandas
import requests
from bs4 import BeautifulSoup
from haversine import haversine
import folium
import webbrowser

#http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong?divId=ctprvnCd&key=11&indsSclsCd=D03A01&divId=ctprvnCd&numOfRows=100000&pageNo=1&type=xml&serviceKey={}


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
for i in range(1, 10):
    url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong?divId=ctprvnCd&key={}&indsSclsCd=D03A01&divId=ctprvnCd&numOfRows=100000&pageNo={}&type=xml&serviceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'.format(city_code, i)
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

# data =pandas.concat([pandas.DataFrame(bizesnmList), pandas.DataFrame(lonList), pandas.DataFrame(latList)], axis = 1) # 데이터 프레임으로 변환
# data.to_excel('편의점_데이터.xlsx') # 데이터 프레임으로 변환된 값들을 엑셀로 저장

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
    if num >= 250:
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
print(mid_point_list) # 거리가 200이 넘는 좌표 세트의 중앙 좌표 출력

# # 지도에 찍기
# m = folium.Map(location=[37.551348, 126.988259], # 지도 만들기, 시작 포인트
#                zoom_start=10,
#                )
# for i in mid_point_list: # 거리가 200이 넘어가는 중앙값 좌표들
#     folium.Marker(i,
#                   icon = folium.Icon(color='red')).add_to(m) # 마커 만들기
# convi_map = "seoul_map.html"
# m.save(convi_map)
# webbrowser.open(convi_map)