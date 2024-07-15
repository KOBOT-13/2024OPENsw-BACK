# ossKobot_BACK README.md


# ossKobot_BACK Setup 문서
## 요구사항

## 설치 및 실행 방법
### 가상환경 세팅
```bash
virtualenv venv
```
또는
```bash
python -m venv venv
```
명령어를 활용하여 가상환경을 만들어 줍니다.

```bash
source venv/bin/activate
```
명령어를 활용하여 가상환경을 활성화 시켜줍니다.

### secrets.json 설치하기
```bash
C:\...\Github\2024OpenSW-BACK\secret.json
```
위 위치에 secret.json 을 설치합니다.

### postgreSQL DB 설치
```bash
https://www.postgresql.org/download/ # 원하는 버전을 설치합니다.
# 설치 과정에서 입력하는 superuser의 비밀번호를 잘 기억해야 합니다.
```
웹에서 postgreSQL을 설치하고 초기 비밀번호를 설정합니다.  
설치된 SQL Shell을 실행하여 엔터를 몇번 누른 뒤, 패스워드 입력란에 초기 비밀번호를 입력합니다.

### postgreSQL과 장고 연동하기
```bash
CREATE DATABASE ('데이터베이스 이름');
CREATE USER ('유저명') WITH PASSWORD ('비밀번호');
ALTER ROLE ('유저명') SET client_encoding TO 'utf8';
ALTER ROLE ('유저명') SET default_transaction_isolation TO 'read committed';
ALTER ROLE ('유저명') SET TIME ZONE 'Asia/Seoul';
GRANT ALL PRIVILEGES ON DATABASE data_planet_db TO root;
ALTER USER ('유저명') SUPERUSER;
```
secret.json 파일에 설정되어 있는 '데이터베이스 이름', '유저명', '비밀번호'를 보고  
위 명령어를 차례로 SQL Shell 에서 실행합니다.

### postgreSQL이 작동을 멈추었을 경우(Windows)
```bash
윈도우 로고 우클릭 > 컴퓨터 관리 > 서비스 및 응용 프로그램 > 서비스 > postgresql-x64-16 을 찾아 우클릭 > 시작
```
윈도우 최적화 프로그램 등을 사용했을 때, 콘솔이 꺼지는 듯 합니다.  
꺼지면 python manage.py runserver가 동작하지 않으므로 오류 발생시 잘 켜주도록 합시다.

### 의존성 패키지 설치
```bash
pip install -r requirements.txt
```
동봉되어있는 requirements.txt를 활용하여 의존성 패키지를 설치하여 줍니다.

### 데이터베이스 postgreSQL 설치 및 Django 연동
```bash
https://seokii.tistory.com/199 
URL 참조
```

### 데이터베이스 초기화
```bash
python manage.py makemigrations
python manage.py migrate
```
위 명령어를 활용하여 데이터베이스를 초기화해 줍니다.  
makemigrations 명령어를 실행시키면 각 앱별로 데이터베이스 마이그레이션 파일들이 생성되니  
git을 활용할 때, 이때 만들어지는 마이그레이션 파일들도 푸시해 줍니다.


### 로컬 서버 실행
```bash
python manage.py runserver
```

### API 관리 페이지 접속(수정해야함)
```bash
http://127.0.0.1:8000/??????
```
해당 URL로 접속하여 api를 확인하고 사용할 수 있습니다.

## 프로젝트 구성

## Team



### Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![Windows 11](https://img.shields.io/badge/Windows%2011-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Google](https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)
![KakaoTalk](https://img.shields.io/badge/kakaotalk-ffcd00.svg?style=for-the-badge&logo=kakaotalk&logoColor=000000)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)
![Apple](https://img.shields.io/badge/Apple-%23000000.svg?style=for-the-badge&logo=apple&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

