import requests
import pandas as pd
from bs4 import BeautifulSoup
import pymysql

main_url = 'http://ncov.mohw.go.kr/'

mCols = ['area', 'patient', 'patent_increase']
df = pd.DataFrame(columns=mCols)

conn = pymysql.connect(host='localhost', user='root', password='##tkakrnl12', db='django_book', charset='utf8')
myCursor = conn.cursor()

request_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

req = requests.get(main_url, request_header)
soup = BeautifulSoup(req.text, 'html.parser')

for s in soup.select('div#main_maplayout > button'):
    name = s.select_one('span.name').text
    num = s.select_one('span.num').text
    before = s.select_one('span.before').text
    print(name, num, before)
    myCursor.execute(
        'INSERT INTO korea_covids('
        'area,'
        'patient,'
        'increase) VALUES("{}", "{}","{}");'.format(
            name, num, before))

    info = [name, num, before]
    df.loc[len(df)] = info

print('데이터 수집완료')
df.to_csv("./korea_covid.csv", encoding='utf8')

conn.commit()
conn.close()
