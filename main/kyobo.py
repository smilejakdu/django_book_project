from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

# 첨언 : 사실 urllib 같은 것 보다는 request라는 라이브러리를 이용해서 HTTP Request를 요청하는게 좋습니다..(훨씬 편함)


conn = pymysql.connect(host='localhost', user='root', password='##tkakrnl12', db='django_book', charset='utf8')
myCursor = conn.cursor()
sql = "truncate table book"
myCursor.execute(sql)
# 교보문고의 베스트셀러 웹페이지를 가져옵니다.
html = urlopen('http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf')
bs_obj = BeautifulSoup(html, "html.parser")

# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
book_page_urls = []
for cover in bs_obj.find_all('div', {'class': 'detail'}):
    link = cover.select('a')[0].get('href')
    book_page_urls.append(link)

# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.
for index, book_page_url in enumerate(book_page_urls):
    html = urlopen(book_page_url)
    bsObject = BeautifulSoup(html, "html.parser")
    title = bsObject.find('meta', {'property': 'rb:itemName'}).get('content')
    author = bsObject.select('span.name a')[0].text
    image = bsObject.find('meta', {'property': 'rb:itemImage'}).get('content')
    url = bsObject.find('meta', {'property': 'rb:itemUrl'}).get('content')
    original_price = bsObject.find('meta', {'property': 'rb:originalPrice'}).get('content')
    original_price = format(int(original_price), ',')
    sale_price = bsObject.find('meta', {'property': 'rb:salePrice'}).get('content')
    print(title, author, image, url, original_price, sale_price)
    myCursor.execute(
        'INSERT INTO book(title,'
        'author,'
        'image,'
        'url,'
        'original_price,'
        'sale_price) VALUES("{}", "{}", "{}", "{}", "{}", "{}");'.format(
            title, author, image, url, original_price, sale_price))

conn.commit()
conn.close()
