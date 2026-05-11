# ==========================================================
# ADVANCED GEOLOCATION ENGINE
# GIS + HOTSPOT INTELLIGENCE
# ==========================================================

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

import time

# ==========================================================
# GEOLOCATOR
# ==========================================================

geolocator = Nominatim(

    user_agent="wildlife_crime_ai"
)

print("✅ GEOLOCATION ENGINE LOADED")

# ==========================================================
# CACHE
# ==========================================================

location_cache = {}

# ==========================================================
# INDIA CHECK
# ==========================================================

def is_india_location(location_data):

    if location_data is None:

        return False

    address = str(

        location_data.address
    ).lower()

    if "india" in address:

        return True

    return False

# ==========================================================
# NORMALIZE LOCATION
# ==========================================================

def normalize_location(location):

    location = location.strip()

    location = location.replace(
        "\n",
        " "
    )

    location = " ".join(
        location.split()
    )

    return location

# ==========================================================
# GEOLOCATION ENGINE
# ==========================================================

def get_coordinates(location):

    # ======================================
    # CLEAN
    # ======================================

    location = normalize_location(
        location
    )

    # ======================================
    # CACHE CHECK
    # ======================================

    if location in location_cache:

        return location_cache[
            location
        ]

    try:

        # ==================================
        # GEOCODE
        # ==================================

        geo_data = geolocator.geocode(

            location,

            timeout=10
        )

        # ==================================
        # INVALID LOCATION
        # ==================================

        if geo_data is None:

            result = {

                "success": False,

                "latitude": None,

                "longitude": None,

                "formatted_address":

                None,

                "country":

                None
            }

            location_cache[
                location
            ] = result

            return result

        # ==================================
        # INDIA FILTER
        # ==================================

        if not is_india_location(

            geo_data
        ):

            result = {

                "success": False,

                "latitude": None,

                "longitude": None,

                "formatted_address":

                geo_data.address,

                "country":

                "NON_INDIA"
            }

            location_cache[
                location
            ] = result

            return result

        # ==================================
        # BUILD RESULT
        # ==================================

        result = {

            "success": True,

            "latitude":

            geo_data.latitude,

            "longitude":

            geo_data.longitude,

            "formatted_address":

            geo_data.address,

            "country":

            "India"
        }

        # ==================================
        # CACHE SAVE
        # ==================================

        location_cache[
            location
        ] = result

        # ==================================
        # API SAFETY DELAY
        # ==================================

        time.sleep(1)

        return result

    except GeocoderTimedOut:

        return {

            "success": False,

            "latitude": None,

            "longitude": None,

            "formatted_address":

            None,

            "country":

            None
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }

# ==========================================================
# BULK GEOLOCATION
# ==========================================================

def geocode_multiple_locations(

    locations
):

    results = []

    for location in locations:

        result = get_coordinates(
            location
        )

        results.append({

            "location": location,

            "geo_data": result
        })

    return results

# ==========================================================
# HOTSPOT GRID
# ==========================================================

def build_hotspot_grid(

    geo_records
):

    hotspot_points = []

    for record in geo_records:

        geo_data = record.get(
            "geo_data",
            {}
        )

        if not geo_data.get(
            "success"
        ):

            continue

        hotspot_points.append({

            "latitude":

            geo_data["latitude"],

            "longitude":

            geo_data["longitude"]
        })

    return hotspot_points

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample_location = (

        "Kaziranga National Park Assam"
    )

    result = get_coordinates(

        sample_location
    )

    print("\n===================")

    for key, value in result.items():

        print(f"{key}: {value}")

    print("===================")
    # ==========================================================
# COMPATIBILITY FUNCTION
# REQUIRED BY collector.py
# ==========================================================

def geocode_location(location):

    try:

        return get_coordinates(
            location
        )

    except Exception as e:

        print(
            f"Geolocation Error: {e}"
        )

        return {

            "success": False,

            "latitude": None,

            "longitude": None,

            "formatted_address": None,

            "country": None
        }