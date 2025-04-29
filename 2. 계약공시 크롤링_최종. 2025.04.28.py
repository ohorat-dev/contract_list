# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28, 2025
최종 검토/수정 완료본
"""

import OpenDartReader
import keyring
import pandas as pd
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. DART API 키 가져오기
api_key = keyring.get_password('dart_api_key', 'lgh')
dart = OpenDartReader(api_key)

# 2. HD현대중공업 공시 목록 가져오기
corp_name = 'HD현대중공업'
공시목록 = dart.list(corp=corp_name, start='2017-01-01', end='2025-12-31')

# 3. 단일판매공시 필터링 (정정 포함)
단일판매공시 = 공시목록[
    (공시목록['report_nm'].str.contains('단일판매'))
]

# 4. 결과 저장용 리스트
체결계약명 = []
계약금액 = []
최근매출액 = []
매출액대비 = []
대규모법인여부 = []
계약상대방 = []
계약기간_시작 = []
계약기간_종료 = []
수주일자 = []
공시구분 = []
공시링크 = []

# 5. Selenium 설정
options = webdriver.ChromeOptions()
options.add_argument('headless')  
options.add_argument('no-sandbox')
options.add_argument('disable-dev-shm-usage')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 6. 크롤링
for idx, row in 단일판매공시.iterrows():
    try:
        rcpNo = row['rcept_no']
        report_nm = row['report_nm']

        # 최초공시/기재정정 구분
        if '정정' in report_nm:
            구분 = '기재정정'
        else:
            구분 = '최초'

        url = f'https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcpNo}'
        driver.get(url)
        time.sleep(2)
        driver.switch_to.frame('ifrm')
        time.sleep(1)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        계약명, 금액, 매출, 매출비, 대규모, 상대, 시작일, 종료일 = (None,) * 8

        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for r in rows:
                cols = [col.get_text(strip=True) for col in r.find_all(['th', 'td'])]
                if len(cols) >= 2:
                    # 체결계약명
                    if '체결계약명' in cols[0] and 계약명 is None:
                        계약명 = cols[1]
                    # 계약금액
                    if '계약금액' in cols[0] and 금액 is None:
                        금액 = re.sub(r'[^0-9]', '', cols[1])
                        금액 = int(금액) if 금액.isdigit() else None
                    # 최근매출액
                    if '최근매출액' in cols[0] and 매출 is None:
                        매출 = re.sub(r'[^0-9]', '', cols[1])
                        매출 = int(매출) if 매출.isdigit() else None
                    # 매출액대비
                    if '매출액대비' in cols[0] and 매출비 is None:
                        매출비 = re.sub(r'[^0-9.]', '', cols[1])
                        매출비 = float(매출비) if 매출비 else None
                    # 대규모법인여부
                    if '대규모법인여부' in cols[0] and 대규모 is None:
                        대규모 = cols[1]
                    # 계약상대방 or 계약상대
                    if (('계약상대방' in cols[0].replace(' ', '')) or ('계약상대' in cols[0].replace(' ', ''))) and 상대 is None:
                        상대 = cols[1]
                    # 계약기간 시작일
                    if '시작일' in cols[0] and 시작일 is None:
                        시작일 = cols[1].replace('.', '-')
                    # 계약기간 종료일
                    if '종료일' in cols[0] and 종료일 is None:
                        종료일 = cols[1].replace('.', '-')

        # ✅ 여기부터 데이터 저장 (들여쓰기 맞춰야 함)
        체결계약명.append(계약명)
        계약금액.append(금액)
        최근매출액.append(매출)
        매출액대비.append(매출비)
        대규모법인여부.append(대규모)
        계약상대방.append(상대)
        계약기간_시작.append(시작일)
        계약기간_종료.append(종료일)

        if rcpNo and len(rcpNo) >= 8:
            수주일자.append(f"{rcpNo[:4]}-{rcpNo[4:6]}-{rcpNo[6:8]}")
        else:
            수주일자.append(None)

        공시구분.append(구분)
        공시링크.append(url)

    except Exception as e:
        print(f"⚠️ {rcpNo} 에러 발생:", e)
        체결계약명.append(None)
        계약금액.append(None)
        최근매출액.append(None)
        매출액대비.append(None)
        대규모법인여부.append(None)
        계약상대방.append(None)
        계약기간_시작.append(None)
        계약기간_종료.append(None)

        if rcpNo and len(rcpNo) >= 8:
            수주일자.append(f"{rcpNo[:4]}-{rcpNo[4:6]}-{rcpNo[6:8]}")
        else:
            수주일자.append(None)

        공시구분.append(구분)
        공시링크.append(url)


# 7. 데이터프레임 생성
df = pd.DataFrame({
    '수주일자': 수주일자,
    '공시구분': 공시구분,
    '체결계약명': 체결계약명,
    '계약금액(원)': 계약금액,
    '최근매출액(원)': 최근매출액,
    '매출액대비(%)': 매출액대비,
    '대규모법인여부': 대규모법인여부,
    '계약상대방': 계약상대방,
    '계약기간_시작': 계약기간_시작,
    '계약기간_종료': 계약기간_종료,
    '공시링크': 공시링크
})

# 8. 엑셀 저장
save_path = 'C:/Users/Administrator/Documents/HD현대중공업_수주공시_2017_2025_완성.xlsx'
df.to_excel(save_path, index=False)

# 9. 드라이버 종료
driver.quit()

print('✅ 2017~2025 전체 수주공시 데이터 크롤링 및 저장 완료!')
