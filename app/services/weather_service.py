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
    "tokyo": {"name": "東京", "lat": 35.6762, "lon": 139.6503},
    "osaka": {"name": "大阪", "lat": 34.6937, "lon": 135.5023},
    "nagoya": {"name": "名古屋", "lat": 35.1815, "lon": 136.9066},
    "sapporo": {"name": "札幌", "lat": 43.0618, "lon": 141.3545},
    "fukuoka": {"name": "福岡", "lat": 33.5904, "lon": 130.4017},
    "sendai": {"name": "仙台", "lat": 38.2682, "lon": 140.8694},
    "hiroshima": {"name": "広島", "lat": 34.3853, "lon": 132.4553},
    "kyoto": {"name": "京都", "lat": 35.0116, "lon": 135.7681},
    "naha": {"name": "那覇", "lat": 26.2124, "lon": 127.6809},
}


async def fetch_weather(lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,weather_code,relative_humidity_2m,wind_speed_10m",
        "hourly": "precipitation_probability,weather_code,temperature_2m",
        "timezone": "Asia/Tokyo",
        "forecast_days": 1,
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
        hour = time_str.split("T")[1][:5]
        h_code = hourly["weather_code"][i]
        h_icon, _ = WEATHER_CODES.get(h_code, ("❓", "不明"))
        hours.append({
            "time": hour,
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
