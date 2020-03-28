import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np

# pip install requests beautifulsoup4 pandas openpyxl
page_url = "http://ncov.mohw.go.kr/bdBoardList_Real.do"
params = {
    'brdId': 1,
    'brdGubun': 14,
}

res = requests.get(page_url, params=params)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'html.parser')
html = str(soup.select_one(".data_table.mgt16"))

df = pd.read_html(html)[0]
df.columns = ['area', 'country', '환자발생수(사망)']

df2 = df['환자발생수(사망)'].str.extract(r'([\d,]+)[ㄱ-힣\s\(\)]+([\d,]*)')
df = df.drop('환자발생수(사망)', axis=1)

df['patient'] = df2[0].str.replace(',', '').apply(lambda s: s and int(s))
df['dead'] = df2[1].str.replace(',', '').apply(lambda s: s and int(s) or 0)

df.to_csv("./covid.csv")
