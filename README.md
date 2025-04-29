# 단일판매, 공급계약체결 파이썬 크롤링 방법

## 1. 설치 준비

먼저 파이썬 프로그램을 설치해야 합니다: 저는 파이썬, 스파이더 프로그램을 사용하였습니다. 

- 파이썬, 스파이더는 아나콘다🐍(Anaconda)프로그램을 설치하면 같이 들어있습니다. 이에 아나콘다 프로그램을 다운받아주세요.
- 아나콘다 프로그램의 다운로드 링크는 다음과 같습니다
- https://www.anaconda.com/products/distribution
- 설치가 쉽지 않다면 유튜브를 검색해 보세요. 설치를 안내해주는 유튜브 영상이 많이 있습니다. 

설치를 마친 후에는 Spyder 프로그램을 바로 실행할 수 있으며, Anaconda Prompt를 통해 필요한 라이브러리를 설치하거나 코드를 실행할 수도 있습니다.

본 프로그램이 설치된 운영체계는 아래와 같습니다.
- 혹 운영체계가 서로 맞지 않으면 실행이 되지 않을 수 있는데 그럴때는 chat GPT가 해결방법을 안내해 줄테니 걱정 마시고 실행해 보세요.

✅ 실행 환경 정보
운영체제: Windows 11
파이썬 버전: 3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 15:03:56) [MSC v.1929 64 bit (AMD64)]

✅ 설치된 패키지 버전
pandas==2.2.2
requests==2.32.2
keyring==24.3.1
selenium==4.25.0
openpyxl==3.1.2
tqdm==4.66.4
beautifulsoup4==4.12.3


## 2. 필수 라이브러리 설치

이 프로그램을 실행하기 위해서는 몇 가지 파이썬 라이브러리가 필요합니다.  
아래 명령어를 복사해서 `Anaconda Prompt`에 붙여넣으면 필요한 라이브러리를 한 번에 설치할 수 있습니다.

### ▶ 어떻게 설치하나요?

1. **바탕화면 또는 시작 메뉴**에서  
   `Anaconda Prompt`를 검색해 실행하세요.

2. 아래 명령어를 복사해 붙여넣습니다:

pip install pandas requests keyring selenium openpyxl tqdm beautifulsoup4
> 이미 설치된 라이브러리는 자동으로 건너뜁니다.

### ▶ 라이브러리별 개별 설치 명령어

아래처럼 라이브러리를 하나씩 따로 설치할 수도 있습니다:
pip install pandas pip install requests pip install keyring pip install selenium pip install openpyxl pip install tqdm pip install beautifulsoup4
> 설치 중 오류가 발생하면, 아래 개별 설치 명령어를 참고해서 설치하시기 바랍니다.

설치가 완료될 때까지 기다려 주세요. 
설치 오류가 발생하면 해당 라이브러리만 따로 설치해도 됩니다
만약 `pip` 명령어로 설치가 되지 않는 경우, `conda install` 명령어도 사용할 수 있습니다.

### 📦 설치되는 라이브러리 목록

- `pandas` – 표 형태 데이터 다루기
- `requests` – 인터넷 요청 처리 (API 호출)
- `keyring` – 비밀번호 안전 저장
- `selenium` – 웹 브라우저 자동화
- `openpyxl` – 엑셀 파일(.xlsx) 저장
- `tqdm` – 진행률 표시
- `beautifulsoup4` – HTML 분석 및 텍스트 추출


