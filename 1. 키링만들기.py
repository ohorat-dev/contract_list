# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 11:35:00 2025

@author: Administrator
"""
# 이 창의 내용 전체를 복붙해서 파이썬 스파이터 창에 붙여 넣으세요. 
# 이와 같은 군더더기말은 애써 지우거나 신경쓸 필요가 없습니다. #들어간 문장의 내용은 인식을 하지 않거든요. 

# 먼저 keyring 설치 (처음 1번만 설치)
# 터미널이나 Anaconda Prompt에서 입력:
# pip install keyring(아까 설치했다면 다시 할 필요는 없음)

import keyring

# 📌 저장할 값 설정
service_name = 'dart_api_key' # 서비스 이름 (이건 바꾸지 마시고 그대로 사용하면 됨)
username = '사용자_닉네임'     # 사용자 이름 (본인 id 맘데로 정하기, 저는 lgh)
password = '여기에_API_키_입력'     # 저장할 실제 API 키(찐 api 키 자리, api 생성은 청도군님이 공유하신 블로그 참조)

# (입력시 콤마 지우지 않도록 주의하세요)

# 📌 키링에 저장
keyring.set_password(service_name, username, password)

print("✅ API 키가 키링에 안전하게 저장되었습니다.")

#끝. 키링 설치 간단하죠? 


