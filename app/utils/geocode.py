# app/utils/geocode.py
import requests

def get_lat_lon_from_address(address: str, city: str = None):
    """
    Fetch latitude and longitude for a given address using OpenStreetMap Nominatim.
    Returns (latitude, longitude) or (None, None) if not found.
    """
    if not address:
        return None, None

    try:
        query = f"{address}, {city}" if city else address
        url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1"
        print(url)
        headers = {"User-Agent": "tirupur-homes-geocoder"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None, None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon

    except Exception as e:
        print(f"Geocoding failed for address '{address}': {e}")
        return None, None
