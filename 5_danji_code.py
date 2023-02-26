import pandas
import requests
from bs4 import BeautifulSoup
from haversine import haversine
import folium
import webbrowser

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

kaptCode_list = [] # 서울시 모든 단지코드 리스트
kaptName_list = [] # 서울시 모든 단지명 리스트

for i in range(1, 4):
    url = 'http://apis.data.go.kr/1613000/AptListService2/getSidoAptList?sidoCode={}&numOfRows=100000&pageNo={}&ServiceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'.format(city_code, i)
    # url = 'http://apis.data.go.kr/1613000/AptListService2/getSidoAptList?sidoCode={}&numOfRows=100000&pageNo={}&type=xml&ServiceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'.format(city_code, i)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    ItemList = soup.findAll('item')

    for item in ItemList:
        kaptCode = item.find('kaptcode').get_text()  # 단지코드
        kaptName = item.find('kaptname').get_text()  # 단지명

        kaptCode_list.append(kaptCode)
        kaptName_list.append(kaptName)

print(kaptCode_list)
