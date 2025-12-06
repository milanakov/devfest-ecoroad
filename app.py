from flask import Flask, request, jsonify
from flask_cors import CORS
import openrouteservice as ors
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

# ORS client
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjgyOGYxNGQ4YzE1YzQxN2Q4ZWQyNTg2MjE3ZjVjODA4IiwiaCI6Im11cm11cjY0In0="
client = ors.Client(key=ORS_API_KEY)

# CO2 emissions (kg per km)
EMISSIONS_KG_PER_KM = {
    "car": 0.20,
    "bus": 0.08,
    "ebike": 0.007,
    "escooter": 0.015,
    "bicycle": 0.0,
    "walking": 0.0,
}

# 1 point = 10 g CO₂ saved
def calculate_reward_from_co2(co2_kg):
    grams = co2_kg * 1000.0
    return int(grams / 10.0)

# Geocoder
def geocode_anything(text):
    text = text.strip()

    if "," in text:
        try:
            lat, lon = map(float, text.split(","))
            return lat, lon
        except:
            pass

    try:
        geo = client.pelias_search(
            text=text,
            boundary_country="AT",
            focus_point={"lat": 48.3069, "lon": 14.2858}
        )
        feature = geo["features"][0]
        lon, lat = feature["geometry"]["coordinates"]
        return lat, lon
    except Exception as e:
        raise ValueError(f"Could not geocode '{text}'. {e}")

# Route calculation
def calculate_route_real(start, end, eco_mode):
    lat1, lon1 = geocode_anything(start)
    lat2, lon2 = geocode_anything(end)

    coords = [[lon1, lat1], [lon2, lat2]]

    res, used_profile, last_error = None, None, None
    for profile in ["cycling-regular", "foot-walking", "driving-car"]:
        try:
            res = client.directions(coords, profile=profile, format="json")
            used_profile = profile
            break
        except Exception as e:
            last_error = e

    if res is None:
        raise RuntimeError(f"Routing failed: {last_error}")

    summary = res["routes"][0]["summary"]
    dist_m = summary["distance"]
    dist_km = dist_m / 1000.0

    # CO₂ saving
    car_emission = EMISSIONS_KG_PER_KM["car"]
    eco_emission = EMISSIONS_KG_PER_KM.get(eco_mode, 0.0)
    co2_saved = max((car_emission - eco_emission) * dist_km, 0.0)

    points = calculate_reward_from_co2(co2_saved)

    return {
        "distance_km": round(dist_km, 2),
        "co2_saved": round(co2_saved, 2),
        "points": points,
        "eco_mode": eco_mode,
        "description": (
            f"Eco route: {round(dist_km, 2)} km using {eco_mode.replace('-', ' ')} "
            f"instead of a car (routing profile: {used_profile})."
        ),
    }

# API endpoint
@app.route("/route", methods=["POST"])
def route():
    try:
        data = request.get_json()
        start = data.get("start")
        end = data.get("end")
        eco_mode = data.get("eco_mode", "bicycle")

        if not start or not end:
            return jsonify({"status": "error", "message": "Missing start or end"}), 400

        result = calculate_route_real(start, end, eco_mode)

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        logging.error(f"Server Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/")
def home():
    return "EcoRoute API Running"

if __name__ == "__main__":
    app.run(debug=True)
