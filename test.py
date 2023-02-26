# nums = {x for x in range(2, 10_001) if x == 2 or x % 2 == 1}
# # nums = 2와 홀수로 이루어진 집합
# for odd in range(3, 101, 2): # 101 == int(math.sqrt(10_000)) + 1
#     nums -= {i for i in range(2 * odd, 10_001, odd) if i in nums}
#     # 홀수의 배수로 이루어진 집합을 빼줌
#
# n = int(input())
# for _ in range(n):
#     jjack = int(input())
#     half = jjack//2
#     for x in range(half, 1, -1):
#         if (jjack-x in nums) and (x in nums):
#             print(x, jjack-x)
#             break
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

for_total_url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong?divId=ctprvnCd&key=11&indsSclsCd=D03A01&divId=ctprvnCd&numOfRows=1000&pageNo=1&type=xml&serviceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'
total_response = requests.get(for_total_url)
total_response.raise_for_status()
total_soup = BeautifulSoup(total_response.text, 'html.parser')
total = total_soup.find('totalcount').get_text()
print(total)

mid_time = time.time()-start_time
print(time.strftime("%H:%M:%S", time.gmtime(mid_time)))

for_total2_url = 'http://apis.data.go.kr/1613000/AptListService2/getSidoAptList?sidoCode=11&numOfRows=1000&pageNo=1&ServiceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'
total2_response = requests.get(for_total2_url)
total2_response.raise_for_status()
total2_soup = BeautifulSoup(total2_response.text, 'html.parser')
total2 = total2_soup.find('totalcount').get_text()
print(int(total2)//1000 + 2)

end_time = time.time()-start_time
print(time.strftime("%H:%M:%S", time.gmtime(end_time)))