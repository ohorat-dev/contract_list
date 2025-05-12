# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 17:59:54 2024

@author: Administrator
"""

import requests as rq
import pandas as pd
import keyring
import os
import time
import random
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# DART Open API Key 설정
try:
    api_key = keyring.get_password('dart_api_key', 'lgh')
    if not api_key:
        raise ValueError("API 키를 찾을 수 없습니다.")
except Exception as e:
    logging.error(f"API 키를 가져오는 데 문제가 발생했습니다: {e}")
    api_key = None

# API 키가 없을 경우 중단
if not api_key:
    raise SystemExit("API 키가 없으므로 프로그램을 종료합니다.")

# 기업 이름과 고유번호를 딕셔너리로 설정
corp_dict = {
    "디아이동일": "00118345",
    "대보마그네틱": "01259418",
    "에코프로비엠": "01160363",
    "엘엔에프": "00398701",
    "코스모신소재": "00129989",
    "나노신소재": "00439965",
    "대주전자재료": "00177816",
    "솔룩스첨단소재": "01412822",
    "포스코퓨처엠": "00155276",
    "동화기업": "00173032",
    "엔켐": "01011526",
    "천보": "00897752",
    "켐트로스": "01089350",
    "sk아이이테크놀로지": "01386916",
    "더블유씨피": "01291317",
    "나라엠앤디": "00297095",
    "상신이디피": "00480783",
    "상아프론테크": "00181299",
    "신흥에스이씨": "00807379",
    "에이에프더블류": "01223219",
    "브이원텍": "01027794",
    "엔시스": "01310773",
    "이노메트리": "01258710",
    "원준": "01459212",
    "디에이테크놀로지": "00660121",
    "코윈테크": "01211232",
    "강원에너지": "00100601",
    "에이치와이티씨": "00885906",
    "지아이텍": "01311310",
    "티에스아이": "01139035",
    "피엔티": "00612294",
    "필옵틱스": "00938721",
    "나인테크": "01208849",
    "엠플러스": "00833064",
    "유일에너테크": "01368637",
    "하나기술": "00601191",
    "에이프로": "00604268",
    "원익피앤이": "01020848",
    "새빗켐": "00862880",
    "성일하이텍": "01274329",
    "코스모화학": "00160302",
    "와이엠텍": "01215618",
    "금양": "00106119",
    "윤성에프앤씨": "00925374",
    "디이엔티": "00445160",
    "SKC": "0139889",
    "롯데에너지머티리얼즈": "0113997",
    "에코프로머티": "01311408",
    "이수스페셜티케미컬": "01762569",
    "LG화학": "00356361"
    # 필요한 다른 기업 추가
}

# 데이터 수집할 연도 및 분기 코드 설정
bsns_years = [str(year) for year in range(2013, 2023)]  # 최근 10년 (2013~2022)
report_codes = {
    '11013': '03',  # 1분기
    '11012': '06',  # 반기
    '11014': '09',  # 3분기
    '11011': '12'   # 연간 보고서
}

# 기업별로 데이터를 수집하여 개별 엑셀 파일로 저장
for corp_name, corp_code in corp_dict.items():
    all_data = []
    for year in bsns_years:
        for code, month in report_codes.items():
            url_div = f"https://opendart.fss.or.kr/api/stockTotqySttus.json?crtfc_key={api_key}&corp_code={corp_code}&bsns_year={year}&reprt_code={code}"
            
            # 데이터 요청 및 예외 처리
            max_retries = 3
            backoff_factor = 1.5  # 재시도 시 대기 시간 증가 비율
            for attempt in range(max_retries):  # 최대 3번 재시도
                try:
                    response = rq.get(url_div)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('status') == '000' and 'list' in data:
                            for item in data['list']:
                                item['year_month'] = f"{year}_{month}"
                                all_data.append(item)
                        else:
                            logging.warning(f"[ERROR] 데이터 오류: {data.get('message')} (status: {data.get('status')}) for corp_code {corp_code}, year {year}, and month {month}")
                        break
                    else:
                        logging.error(f"[ERROR] HTTP 오류 발생: {response.status_code} for corp_code {corp_code}")
                except rq.RequestException as e:
                    logging.error(f"요청 오류 발생: {e} - 재시도 {attempt+1}/{max_retries}")
                    time.sleep(backoff_factor * (attempt + 1))  # 재시도마다 대기 시간 증가
                time.sleep(random.uniform(1.5, 3.5))  # 요청 사이에 무작위 대기 시간 설정

    # 수집된 데이터를 DataFrame으로 변환
    corp_data_df = pd.DataFrame(all_data)

    # 수집된 데이터가 있는지 확인 후 엑셀 파일로 저장
    if not corp_data_df.empty:
        file_name = f"{corp_name}_stock_total_data.xlsx"
        file_path = os.path.join(os.path.expanduser("~"), "Documents", file_name)
        corp_data_df.to_excel(file_path, index=False)
        logging.info(f"{corp_name}의 데이터가 {file_path}에 저장되었습니다.")
    else:
        logging.info(f"{corp_name}의 수집된 데이터가 없습니다.")
    
    # 각 기업 데이터 수집 후 추가 대기 시간 설정
    logging.info(f"{corp_name}의 데이터 수집 완료. 다음 기업으로 이동하기 전에 대기 중...")
    time.sleep(random.uniform(10, 20))  # 각 기업마다 10-20초 대기
