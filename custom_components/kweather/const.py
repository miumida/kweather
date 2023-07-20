"""kweather constants."""
DOMAIN   = "kweather"
PLATFORM = "sensor"

SW_VERSION = "1.3.1"
MODEL   = "K-Weather 생활지수"
MANUFAC = "Kweather"

BASE_URL = "https://weather.kweather.co.kr/weather/life_weather/get_life_factor_list/{}"

_AREA_CD = {
    '01' : '11B00000', #서울/경기
    '02' : '11D10000', #강원영서
    '03' : '11D20000', #강원영동
    '04' : '11C10000', #충청북도
    '05' : '11C20000', #충청남도
    '06' : '11H10000', #경상북도
    '07' : '11H20000', #경상남도
    '08' : '11F10000', #전라북도
    '09' : '11F20000', #전라남도
    '10' : '11G00000', #제주도
}

CONF_AREA = 'area'

_ITEMS  = {
    "picnic"     : ["나들이", "mdi:island"],
    "lundary"    : ["빨래",   "mdi:tumble-dryer"],
    "carWash"    : ["세차",   "mdi:car-wash"],
    "fire"       : ["불조심", "mdi:fire"],
    "fitness"    : ["운동",   "mdi:weight-lifter"],
    "pollution"  : ["공해",   "mdi:blur"],
    "spoilage"   : ["부패",   "mdi:virus"],
    "uv"         : ["자외선", "mdi:weather-sunny-alert"],
    "cold"       : ["냉방",   "mdi:air-filter"],
    "heat"       : ["난방",   "mdi:hot-tub"],
    "discomfort" : ["불쾌",   "mdi:emoticon-confused-outline"],
    "influ"      : ["감기",   "mdi:emoticon-sick-outline"],
}

_ATTR = {
    "Name",
    "Factor",
    "Discription",
}
