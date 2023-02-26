import pandas
import requests
from bs4 import BeautifulSoup

# url : 시도별
# http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong?divId=ctprvnCd&key=11&indsSclsCd=D03A01&divId=ctprvnCd&numOfRows=100000&pageNo=1&type=xml&serviceKey={}
# url : 전국
# http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInUpjong?divId=indsSclsCd&key=D03A01&key=Q&numOfRows=10000&pageNo={}&serviceKey=

bizesnmList = []
lonList = []
latList = []

for i in range(1, 50):
    url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInUpjong?divId=indsSclsCd&key=D03A01&key=Q&numOfRows=10000&pageNo={}&serviceKey=%2BJTG2GnVWVXZAxaul97F7f9DHnabKZ5Oiaw5eMiZJ1jGKGxyPSNm89FrSrS9pq5%2FLD5DMiDRMT2JJFp6AnK9eQ%3D%3D'.format(i)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    ItemList = soup.findAll('item')

    for item in ItemList:
        bizesnm = item.find('bizesnm').text
        lon = item.find('lon').text
        lat = item.find('lat').text

        bizesnmList.append(bizesnm)
        lonList.append(lon)
        latList.append(lat)

data =pandas.concat([pandas.DataFrame(bizesnmList), pandas.DataFrame(lonList), pandas.DataFrame(latList)], axis = 1)
data.to_excel('편의점_데이터.xlsx')