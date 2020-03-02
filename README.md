# 케이웨더 생활지수 Sensor
케이웨더 생활지수(K-Weather Living Jisu) Sensor 입니다.<br>
- 검은별31님께서 쓰셨던 카페글(<https://cafe.naver.com/koreassistant/809>)을 보고 센서로 만들어 봤습니다.
- 케이웨더 생활지수에서 제공되는 나들이, 빨래, 세차, 불조심, 운동, 공해, 부패, 자외선, 난방, 감기지수를 센서를 생성합니다.
<br><br>
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
```
<br><br>
### 지역코드
- 아래 표를 참고하여 지역코드를 적습니다.<br>
<br><br>
## History
##### 2020-03-03 최초 작성
- 최초 작성<br>
<br><br>
## 참조 링크
[1] 검은별31님의 우리나라 환경에 맞는 세차센서 사용하기(<https://cafe.naver.com/koreassistant/809>)<br>
[2] 케이웨더 생활지수(<https://www.kweather.co.kr/forecast/forecast_living_jisu.html>)
