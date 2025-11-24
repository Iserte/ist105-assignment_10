# 🌍 Geo Weather Adventure

A Django web application that lets users explore random countries by continent and view real-time weather data for their capitals.  
Results are stored in **MongoDB** for persistence, while Django manages the UI and forms.
  
---

## ✨ Features

- Select a continent and number of random countries.
- Fetch country details (capital, population, coordinates) from the REST Countries API.
- Fetch real-time weather data from OpenWeatherMap API.
- Display results in a clean grid layout with error handling.
- Save search results into MongoDB (`searches` collection).
- View search history (last 20 records) with JSON output.

---

## 🛠️ Requirements

- Python 3.9+
- Django 4.2.7
- Requests 2.32.3
- PyMongo 4.7.2
- python-dotenv 1.0.1
  
---

## Student Information

- **Name:** Gustavo Iserte Bonfim
- **Student ID:** CT1010953
