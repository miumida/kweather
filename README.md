# 케이웨더 생활지수 Sensor

![HAKC)][hakc-shield]
![Version v1.0.1][version-shield]

케이웨더 생활지수(K-Weather Living Jisu) Sensor 입니다.<br>
- 검은별31님께서 쓰셨던 카페글(<https://cafe.naver.com/koreassistant/809>)을 보고 센서로 만들어 봤습니다.
- 케이웨더 생활지수에서 제공되는 나들이, 빨래, 세차, 불조심, 운동, 공해, 부패, 자외선, 난방, 감기, 냉방, 불쾌지수를 센서를 생성합니다.

![screenshot_1](https://github.com/miumida/kweather/blob/master/img/Screenshot_1.png?raw=true)<br>
![screenshot_2](https://github.com/miumida/kweather/blob/master/img/Screenshot_2.png?raw=true)<br>

통합구성요소 적용<br>
![integrations_01](https://github.com/miumida/kweather/blob/master/img/integrations_01.png?raw=true)<br>
![integrations_02](https://github.com/miumida/kweather/blob/master/img/integrations_02.png?raw=true)<br>
<br><br>
## Version history
| Version | Date        | 내용            |
| :-----: | :---------: | ------------- |
| v1.0.0    | 2020.03.03  | First version  |
| v1.0.1    | 2020.03.04  | 공해지수 MDI 아이콘 변경  |
| v1.0.2    | 2020.09.21  | 불쾌지수 MDI 아이콘 변경  |
| v1.1.0    | 2020.10.28  | 통합구성요소 적용  |
| v1.1.1    | 2020.11.10  | 통합구성요소 기기증가 오류 수정   |
| v1.1.2    | 2020.11.26  | 통합구성요소 문구 수정   |
| v1.1.3    | 2020.12.14  | 버전체계 변경에 따른 수정   |
| v1.1.4    | 2021.03.05  | manifest.json 파일 version 정보 추가  |
| v1.2.0    | 2021.04.08  | 통합구성요소 로직 수정 |
| v1.2.1    | 2021.12.15  | Fixed bug |

<br><br>
## Installation
### Manual
- HA 설치 경로 아래 custom_components 에 파일을 넣어줍니다.<br>
  `<config directory>/custom_components/kweather/__init__.py`<br>
  `<config directory>/custom_components/kweather/manifest.json`<br>
  `<config directory>/custom_components/kweather/sensor.py`<br>
- configuration.yaml 파일에 설정을 추가합니다.<br>
- Home-Assistant 를 재시작합니다<br>
### HACS
- HACS > SETTINGS 메뉴 선택
- ADD CUSTOM REPOSITORY에 'https://github.com/miumida/kweather' 입력하고 Category에 'integration' 선택 후, 저장
- HACS > INTEGRATIONS 메뉴 선택 후, 검색하여 설치

<br><br>
## Usage
### configuration
- HA 설정에 Local Weather RSS sensor를 추가합니다.<br>
```yaml
sensor:
  - platform: kweather
    area: '지역코드'
    monitored_conditions:
     - picnic
     - laundry
     - carwash
     - fire
     - exercise
     - pollution
     - corruption
     - uv
     - heating
     - cold
     - cooling
     - feel
```
<br><br>
### 지역코드(area)
- 아래 표를 참고하여 지역코드를 적습니다.

|코드|지역|
|--|-------|
|01|서울/경기|
|02|강원영서 |
|03|강원영동 |
|04|충청북도 |
|05|충청남도 |
|06|경상북도 |
|07|경상남도 |
|08|전라북도 |
|09|전라남도 |
|10|제주도|

<br><br>
### 생활지수(monitored_conditions)
- 아래 표를 참고하여 필요한 항목을 추가합니다.

|코드|항목|
|--------|------|
|picnic   |나들이|
|laundry  |빨래| 
|carwash  |세차| 
|fire     |불조심|
|exercise |운동|
|pollution|공해| 
|corruption|부패| 
|uv       |자외선|
|heating  |난방| 
|cold     |감기| 
|cooling  |냉방| 
|feel     |불쾌| 

<br><br>
## Lovelace
- button card를 통해서 조금 더 이쁘게 꾸며볼 수 있다.
- 몽쉘좋아님의 "버튼카드 + 케이웨더 생활지수" 카페 게시글(<https://cafe.naver.com/koreassistant/848>)
- 상큼한레몬님의 "케이웨더 생활지수 디자인 고민... (+ 디자인 추가)" 카페 게시글(<https://cafe.naver.com/koreassistant/853>)

<br><br>
## 참조 링크
[1] 검은별31님의 우리나라 환경에 맞는 세차센서 사용하기(<https://cafe.naver.com/koreassistant/809>)<br>
[2] 케이웨더 생활지수(<https://www.kweather.co.kr/forecast/forecast_living_jisu.html>)

<br>

#### Thanks your support!
<a href="https://www.buymeacoffee.com/miumida" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee"></a>


[version-shield]: https://img.shields.io/badge/version-v1.2.1-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
