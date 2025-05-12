# -*- coding: utf-8 -*-
"""
공시일 기준 대표 주가 수집 (D+1 우선, 없으면 D+3) 및 엑셀 저장
"""

import pandas as pd
import requests
import time
from datetime import datetime
from pandas.tseries.offsets import CustomBusinessDay
import FinanceDataReader as fdr
import keyring

# ✅ DART API Key
api_key = keyring.get_password('dart_api_key', 'lgh')

# ✅ 사용자 설정
corp_code = "01160363"              # DART 기업 고유번호
stock_name = "에코프로비엠"          # KRX 종목명 (엑셀 저장용 등)
stock_code = "247540"               # FDR 종목코드
years = range(2016, 2026)

# ✅ 영업일 오프셋
krx_bday = CustomBusinessDay(weekmask='Mon Tue Wed Thu Fri')

# ✅ DART 공시 수집 함수
def fetch_dart_reports(corp_code, years, api_key):
    all_data = []
    session = requests.Session()

    for year in years:
        url = "https://opendart.fss.or.kr/api/list.json"
        params = {
            'crtfc_key': api_key,
            'corp_code': corp_code,
            'bgn_de': f"{year}0101",
            'end_de': f"{year}1231",
            'last_reprt_at': 'Y',
            'pblntf_ty': 'A',
            'sort': 'date',
            'sort_mth': 'asc',
            'page_no': '1',
            'page_count': '100'
        }

        try:
            response = session.get(url, params=params)
            data = response.json()
            if data.get('status') == '000' and 'list' in data:
                for report in data['list']:
                    name = report['report_nm']
                    if any(k in name for k in ['사업보고서', '반기보고서', '분기보고서', '3분기보고서']):
                        all_data.append({
                            'rcept_dt': report['rcept_dt'],
                            'report_nm': name
                        })
            time.sleep(1)
        except Exception as e:
            print(f"{year} 수집 실패:", e)

    df = pd.DataFrame(all_data)
    df['rcept_dt'] = pd.to_datetime(df['rcept_dt'])
    return df.sort_values('rcept_dt')

# ✅ 공시일 수집
dart_df = fetch_dart_reports(corp_code, years, api_key)

# ✅ 주가 수집
start_date = dart_df['rcept_dt'].min() - pd.Timedelta(days=5)
end_date = dart_df['rcept_dt'].max() + pd.Timedelta(days=5)
price_df = fdr.DataReader(stock_code, start=start_date, end=end_date)

# ✅ 대표 주가 추출 (D+1 → D+3)
records = []
for _, row in dart_df.iterrows():
    base_date = row['rcept_dt']
    report_name = row['report_nm']

    picked_price = None
    for offset in [1, 3]:
        try:
            target_date = (base_date + offset * krx_bday).date()
            price = price_df.loc[price_df.index.date == target_date, 'Close']
            if not price.empty:
                picked_price = price.values[0]
                used_offset = offset
                break
        except:
            continue

    if picked_price:
        records.append({
            '공시일': base_date.date(),
            '보고서명': report_name,
            '주가기준일': target_date,
            '사용된일수': f"D+{used_offset}",
            '종가': picked_price
        })

# ✅ 결과 저장
result_df = pd.DataFrame(records).sort_values('공시일').reset_index(drop=True)
today = datetime.today().strftime('%Y%m%d')
filename = f"{stock_name}_공시일기준_대표주가_{today}.xlsx"
result_df.to_excel(filename, index=False)
print(f"\n✅ 엑셀 저장 완료: {filename}")

