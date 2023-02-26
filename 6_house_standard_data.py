import pandas
import requests
from bs4 import BeautifulSoup
from haversine import haversine
import folium
import webbrowser

# 6을 복사해서 7, 8과 연결해서 만듦

kaptCode_list = ['A12009201', 'A12009202', 'A12009203', 'A12009303', 'A12009304', 'A12009305'] # 단지코드 리스트


kaptName_list = []  # 단지명 리스트
kaptdaCnt_list = []  # 세대수 리스트
# kaptDongCnt_list = []  # 동수 리스트
# doroJuso_list = []  # 도로명 주소 리스트
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

print(kaptName_list)
print(kaptdaCnt_list)
print(addr_list)