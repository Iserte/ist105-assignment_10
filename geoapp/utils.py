import random
import requests

REST_COUNTRIES_BASE = "https://restcountries.com/v3.1/region"

def fetch_countries_by_continent(continent: str) -> list[dict]:
    url = f"{REST_COUNTRIES_BASE}/{continent}"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json()

def pick_random_countries(countries: list[dict], count: int) -> list[dict]:
    filtered = [c for c in countries if c.get("capital")]
    if len(filtered) < count:
        count = max(1, len(filtered))
    return random.sample(filtered, count) if filtered else []

def fetch_weather_for_capital(capital: str, api_key: str) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": capital, "appid": api_key, "units": "metric"}
    resp = requests.get(url, params=params, timeout=20)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        return {"error": True, "status_code": resp.status_code, "data": resp.json() if resp.content else {}}
    return resp.json()