import httpx

WEATHER_CODES = {
    0: ("☀️", "快晴"),
    1: ("🌤️", "晴れ"),
    2: ("⛅", "くもり時々晴れ"),
    3: ("☁️", "くもり"),
    45: ("🌫️", "霧"),
    48: ("🌫️", "霧氷"),
    51: ("🌦️", "小雨"),
    53: ("🌧️", "雨"),
    55: ("🌧️", "強い雨"),
    61: ("🌧️", "小雨"),
    63: ("🌧️", "雨"),
    65: ("🌧️", "大雨"),
    71: ("🌨️", "小雪"),
    73: ("🌨️", "雪"),
    75: ("🌨️", "大雪"),
    80: ("🌦️", "にわか雨"),
    81: ("🌧️", "にわか雨(強)"),
    82: ("🌧️", "激しいにわか雨"),
    95: ("⛈️", "雷雨"),
    96: ("⛈️", "雷雨(雹)"),
    99: ("⛈️", "激しい雷雨(雹)"),
}

CITIES = {
    "hokkaido": {"name": "北海道(札幌)", "lat": 43.0618, "lon": 141.3545},
    "aomori": {"name": "青森", "lat": 40.8244, "lon": 140.7400},
    "iwate": {"name": "岩手(盛岡)", "lat": 39.7036, "lon": 141.1527},
    "miyagi": {"name": "宮城(仙台)", "lat": 38.2682, "lon": 140.8694},
    "akita": {"name": "秋田", "lat": 39.7186, "lon": 140.1024},
    "yamagata": {"name": "山形", "lat": 38.2405, "lon": 140.3634},
    "fukushima": {"name": "福島", "lat": 37.7503, "lon": 140.4676},
    "ibaraki": {"name": "茨城(水戸)", "lat": 36.3418, "lon": 140.4468},
    "tochigi": {"name": "栃木(宇都宮)", "lat": 36.5658, "lon": 139.8836},
    "gunma": {"name": "群馬(前橋)", "lat": 36.3912, "lon": 139.0608},
    "saitama": {"name": "埼玉(さいたま)", "lat": 35.8617, "lon": 139.6455},
    "chiba": {"name": "千葉", "lat": 35.6047, "lon": 140.1233},
    "tokyo": {"name": "東京", "lat": 35.6762, "lon": 139.6503},
    "kanagawa": {"name": "神奈川(横浜)", "lat": 35.4478, "lon": 139.6425},
    "niigata": {"name": "新潟", "lat": 37.9026, "lon": 139.0233},
    "toyama": {"name": "富山", "lat": 36.6953, "lon": 137.2114},
    "ishikawa": {"name": "石川(金沢)", "lat": 36.5946, "lon": 136.6256},
    "fukui": {"name": "福井", "lat": 36.0652, "lon": 136.2219},
    "yamanashi": {"name": "山梨(甲府)", "lat": 35.6642, "lon": 138.5684},
    "nagano": {"name": "長野", "lat": 36.2381, "lon": 138.1813},
    "gifu": {"name": "岐阜", "lat": 35.3912, "lon": 136.7223},
    "shizuoka": {"name": "静岡", "lat": 34.9769, "lon": 138.3831},
    "aichi": {"name": "愛知(名古屋)", "lat": 35.1815, "lon": 136.9066},
    "mie": {"name": "三重(津)", "lat": 34.7303, "lon": 136.5086},
    "shiga": {"name": "滋賀(大津)", "lat": 35.0045, "lon": 135.8686},
    "kyoto": {"name": "京都", "lat": 35.0116, "lon": 135.7681},
    "osaka": {"name": "大阪", "lat": 34.6937, "lon": 135.5023},
    "hyogo": {"name": "兵庫(神戸)", "lat": 34.6913, "lon": 135.1830},
    "nara": {"name": "奈良", "lat": 34.6851, "lon": 135.8329},
    "wakayama": {"name": "和歌山", "lat": 34.2260, "lon": 135.1675},
    "tottori": {"name": "鳥取", "lat": 35.5039, "lon": 134.2381},
    "shimane": {"name": "島根(松江)", "lat": 35.4723, "lon": 133.0505},
    "okayama": {"name": "岡山", "lat": 34.6618, "lon": 133.9344},
    "hiroshima": {"name": "広島", "lat": 34.3853, "lon": 132.4553},
    "yamaguchi": {"name": "山口", "lat": 34.1860, "lon": 131.4714},
    "tokushima": {"name": "徳島", "lat": 34.0658, "lon": 134.5593},
    "kagawa": {"name": "香川(高松)", "lat": 34.3401, "lon": 134.0434},
    "ehime": {"name": "愛媛(松山)", "lat": 33.8416, "lon": 132.7657},
    "kochi": {"name": "高知", "lat": 33.5597, "lon": 133.5311},
    "fukuoka": {"name": "福岡", "lat": 33.5904, "lon": 130.4017},
    "saga": {"name": "佐賀", "lat": 33.2494, "lon": 130.2988},
    "nagasaki": {"name": "長崎", "lat": 32.7448, "lon": 129.8737},
    "kumamoto": {"name": "熊本", "lat": 32.7898, "lon": 130.7417},
    "oita": {"name": "大分", "lat": 33.2382, "lon": 131.6126},
    "miyazaki": {"name": "宮崎", "lat": 31.9111, "lon": 131.4239},
    "kagoshima": {"name": "鹿児島", "lat": 31.5602, "lon": 130.5581},
    "okinawa": {"name": "沖縄(那覇)", "lat": 26.2124, "lon": 127.6809},
}


async def fetch_weather(lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code,relative_humidity_2m,wind_speed_10m",
        "hourly": "precipitation_probability,weather_code,temperature_2m",
        "timezone": "Asia/Tokyo",
        "forecast_days": 2,
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        res.raise_for_status()
        data = res.json()

    current = data["current"]
    code = current["weather_code"]
    icon, label = WEATHER_CODES.get(code, ("❓", "不明"))

    hourly = data["hourly"]
    hours = []
    for i, time_str in enumerate(hourly["time"]):
        h_code = hourly["weather_code"][i]
        h_icon, _ = WEATHER_CODES.get(h_code, ("❓", "不明"))
        hours.append({
            "time": time_str,
            "precipitation_probability": hourly["precipitation_probability"][i],
            "weather_icon": h_icon,
            "temperature": hourly["temperature_2m"][i],
        })

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "weather_code": code,
        "weather_icon": icon,
        "weather_label": label,
        "hourly": hours,
    }
