import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpRequest
from pymongo import MongoClient
from .forms import ContinentForm
from .utils import fetch_countries_by_continent, pick_random_countries, fetch_weather_for_capital

def get_mongo_collection():
    uri = settings.MONGODB_HOST
    if not uri:
        return None
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[settings.MONGODB_NAME]
    return db[settings.MONGODB_COLLECTION]

def continent_form_view(request: HttpRequest):
    if request.method == "POST":
        form = ContinentForm(request.POST)
        if form.is_valid():
            continent = form.cleaned_data["continent"]
            count = form.cleaned_data["count"]
            return redirect("search_results", continent=continent, count=count)
    else:
        form = ContinentForm()
    return render(request, "continent_form.html", {"form": form})

def search_results_view(request: HttpRequest, continent: str, count: int):
    api_key = settings.OPENWEATHERMAP_API_KEY
    errors = []
    results = []

    try:
        countries = fetch_countries_by_continent(continent)
    except Exception as e:
        errors.append(f"Failed to fetch countries for {continent}: {e}")
        countries = []

    random_countries = pick_random_countries(countries, count)

    for c in random_countries:
        country_name = c.get("name", {}).get("common", "Unknown")
        capital_list = c.get("capital", [])
        capital = capital_list[0] if capital_list else None
        population = c.get("population", None)
        latlng = c.get("latlng", None)

        weather = None
        if capital and api_key:
            w = fetch_weather_for_capital(capital, api_key)
            if w and not w.get("error"):
                weather = {
                    "temp": w.get("main", {}).get("temp"),
                    "desc": (w.get("weather") or [{}])[0].get("description"),
                    "wind": w.get("wind", {}).get("speed"),
                    "humidity": w.get("main", {}).get("humidity"),
                }
            else:
                errors.append(f"Error fetching weather for {capital}: {w}")
        else:
            errors.append(f"Missing capital or API key not configured for {country_name}")

        results.append({
            "country": country_name,
            "capital": capital,
            "population": population,
            "latlng": latlng,
            "weather": weather,
        })

    saved_id = None
    col = get_mongo_collection()
    if col is not None:
        doc = {
            "timestamp": datetime.utcnow(),
            "continent": continent,
            "requested_count": count,
            "results": results,
            "errors": errors,
        }
        try:
            res = col.insert_one(doc)
            saved_id = str(res.inserted_id)
        except Exception as e:
            errors.append(f"Error saving to MongoDB: {e}")

    context = {
        "continent": continent,
        "requested_count": count,
        "results": results,
        "errors": errors,
        "saved_id": saved_id,
    }
    return render(request, "search_results.html", context)

def history_view(request: HttpRequest):
    col = get_mongo_collection()
    records = []
    if col:
        try:
            cursor = col.find().sort("timestamp", -1).limit(20)
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                ts = doc.get("timestamp")
                doc["timestamp_str"] = ts.strftime("%Y-%m-%d %H:%M:%S UTC") if ts else "N/A"
                records.append(doc)
        except Exception:
            records = []
    return render(request, "history.html", {"records": records})