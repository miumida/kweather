# 케이웨더 생활지수 Sensor
케이웨더 생활지수(K-Weather Living Jisu) Sensor 입니다.<br>
- 검은별31님께서 쓰셨던 카페글(<https://cafe.naver.com/koreassistant/809>)을 보고 센서로 만들어 봤습니다.
- 케이웨더 생활지수에서 제공되는 나들이, 빨래, 세차, 불조심, 운동, 공해, 부패, 자외선, 난방, 감기, 냉방, 불쾌지수를 센서를 생성합니다.
<br><br>

## Version history
| Version | Date        |               |
| :-----: | :---------: | ------------- |
| v1.0.0    | 2020.03.03  | First version  |

## Installation
- HA 설치 경로 아래 custom_components 에 파일을 넣어줍니다.<br>
  `<config directory>/custom_components/kweather/__init__.py`<br>
  `<config directory>/custom_components/kweather/manifest.json`<br>
  `<config directory>/custom_components/kweather/sensor.py`<br>
- configuration.yaml 파일에 설정을 추가합니다.<br>
- Home-Assistant 를 재시작합니다<br>
<br><br>
## Usage
### configuration
- HA 설정에 Local Weather RSS sensor를 추가합니다.<br>
```yaml
sensor:
  - platform: kweather
    area: 지역코드
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
## 참조 링크
[1] 검은별31님의 우리나라 환경에 맞는 세차센서 사용하기(<https://cafe.naver.com/koreassistant/809>)<br>
[2] 케이웨더 생활지수(<https://www.kweather.co.kr/forecast/forecast_living_jisu.html>)
