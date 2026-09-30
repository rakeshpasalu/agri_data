import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os
import sys
import datetime
import math
import re
import unicodedata
from pathlib import Path

# Ensure bulletproof UTF-8 stdout/stderr on Windows consoles to prevent cp1252 charmap crashes
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
PROJECT_ROOT = os.path.dirname(BASE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Evidence-backed catalog and live data providers
CROP_CATALOG_PATH = Path(PROJECT_ROOT) / "knowledge" / "crops" / "catalog.json"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def _utc_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _coordinates(params):
    try:
        lat = float(params["lat"][0])
        lon = float(params["lon"][0])
    except (KeyError, IndexError, TypeError, ValueError):
        raise ValueError("Valid lat and lon query parameters are required.")
    if not math.isfinite(lat) or not math.isfinite(lon) or not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError("Latitude and longitude are outside their valid ranges.")
    return lat, lon


def load_crop_catalog():
    try:
        with CROP_CATALOG_PATH.open("r", encoding="utf-8") as stream:
            catalog = json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("The evidence-linked crop catalog could not be loaded.") from exc
    crops = catalog.get("crops") if isinstance(catalog, dict) else None
    if not isinstance(crops, list) or not crops:
        raise RuntimeError("The evidence-linked crop catalog has no crop records.")
    for crop in crops:
        if not isinstance(crop, dict) or not crop.get("id") or not crop.get("names"):
            raise RuntimeError("The crop catalog contains a record without an id or localized names.")
    return catalog


def fetch_live_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,et0_fao_evapotranspiration",
        "current": "temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m",
        "timezone": "auto",
        "forecast_days": 14,
    }
    url = WEATHER_URL + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "Bhumi-Farmer-Pilot/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            if response.status != 200:
                raise RuntimeError("Open-Meteo returned a non-success response.")
            data = json.loads(response.read().decode("utf-8"))
        daily = data.get("daily")
        if not isinstance(daily, dict) or not isinstance(daily.get("time"), list):
            raise RuntimeError("Open-Meteo returned an incomplete forecast.")
        return {
            "source": "Open-Meteo Forecast API",
            "status": "online",
            "fetched_at": _utc_timestamp(),
            "timezone": data.get("timezone"),
            "current": data.get("current"),
            "daily": daily,
            "elevation_m": data.get("elevation"),
        }
    except Exception:
        return {
            "source": "Open-Meteo Forecast API",
            "status": "unavailable",
            "fetched_at": _utc_timestamp(),
            "current": None,
            "daily": {},
            "elevation_m": None,
            "message": "The weather provider could not be reached or did not return a valid forecast. No synthetic forecast is shown.",
        }


def get_market_data(district):
    try:
        from backend.ingestion.agmarknet_service import get_latest_mandi_prices
        return get_latest_mandi_prices(district=district)
    except Exception:
        return {
            "status": "unavailable",
            "district": district,
            "as_of": None,
            "records": [],
            "source": {"name": "AGMARKNET via data.gov.in"},
            "message": "The official market-price service could not be reached.",
        }


def _fold_term(value):
    text = unicodedata.normalize("NFKD", str(value or "").casefold())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(re.findall(r"[a-z0-9]+", text))


def _crop_market_observations(crop, market_data):
    aliases = set(_fold_term(item) for item in crop.get("market_aliases", []) if _fold_term(item))
    aliases.add(_fold_term(crop.get("canonical_name")))
    aliases.add(_fold_term(crop.get("id")))
    names = crop.get("names", {})
    if isinstance(names, dict):
        aliases.update(_fold_term(item) for item in names.values() if _fold_term(item))
    records = market_data.get("records") if isinstance(market_data, dict) else []
    if not isinstance(records, list):
        return []
    return [
        row for row in records
        if isinstance(row, dict) and _fold_term(row.get("commodity")) in aliases
    ]


def _forecast_temperature_screen(crop, weather):
    envelope = crop.get("ecological_envelope", {})
    temperature = envelope.get("temperature_c", {})
    optimal = temperature.get("optimal")
    absolute = temperature.get("absolute")
    daily = weather.get("daily", {}) if isinstance(weather, dict) else {}
    highs = daily.get("temperature_2m_max", [])
    lows = daily.get("temperature_2m_min", [])
    if weather.get("status") != "online" or not isinstance(highs, list) or not isinstance(lows, list) or not highs or not lows:
        return {
            "status": "unavailable",
            "scope": "14-day forecast only; not a seasonal crop-suitability assessment",
            "source_url": envelope.get("source_url"),
        }
    try:
        forecast_high = max(float(value) for value in highs if value is not None)
        forecast_low = min(float(value) for value in lows if value is not None)
    except (TypeError, ValueError):
        return {
            "status": "unavailable",
            "scope": "14-day forecast only; not a seasonal crop-suitability assessment",
            "source_url": envelope.get("source_url"),
        }
    status = "reference_ranges_unavailable"
    if isinstance(absolute, list) and len(absolute) == 2:
        if forecast_low < float(absolute[0]) or forecast_high > float(absolute[1]):
            status = "forecast_partly_outside_broad_species_range"
        elif isinstance(optimal, list) and len(optimal) == 2 and forecast_low >= float(optimal[0]) and forecast_high <= float(optimal[1]):
            status = "forecast_within_broad_optimal_temperature_range"
        else:
            status = "forecast_within_broad_absolute_range_only"
    return {
        "status": status,
        "forecast_min_c": forecast_low,
        "forecast_max_c": forecast_high,
        "optimal_reference_c": optimal,
        "absolute_reference_c": absolute,
        "scope": "14-day forecast and global species envelope only; not a local or full-season suitability assessment",
        "source_url": envelope.get("source_url"),
    }


def build_crop_candidate(crop, weather, market_data):
    varieties = []
    for variety in crop.get("varieties", []) if isinstance(crop.get("varieties"), list) else []:
        if isinstance(variety, dict):
            item = dict(variety)
            item["local_stock_status"] = "unverified"
            item["local_performance_status"] = "unverified"
            varieties.append(item)
    observations = _crop_market_observations(crop, market_data)
    if observations:
        observation_status = "dated_observations_available"
    elif market_data.get("status") in ("setup_required", "unavailable"):
        observation_status = market_data.get("status")
    else:
        observation_status = "no_exact_commodity_match"
    return {
        "id": crop["id"],
        "canonical_name": crop.get("canonical_name"),
        "names": crop.get("names", {}),
        "scientific_name": crop.get("scientific_name"),
        "regional_context": crop.get("regional_context"),
        "decision_status": "candidate_unranked",
        "ecological_envelope": crop.get("ecological_envelope", {}),
        "weather_screen": _forecast_temperature_screen(crop, weather),
        "market_observation_status": observation_status,
        "market_observations": observations,
        "economic_estimate": {
            "status": "unavailable",
            "reason": "No locally validated yield model, complete farm costs, sale grade, and verified farm-gate or buyer quote are connected.",
        },
        "varieties": varieties,
        "evidence": crop.get("evidence", []),
    }


def build_recommendations(lat, lon, water_source, district="Chitradurga"):
    catalog = load_crop_catalog()
    weather = fetch_live_weather(lat, lon)
    market_data = get_market_data(district)
    gaps = [
        "A plot-specific soil test or Soil Health Card",
        "Farmer-confirmed water availability and dependable seasonal supply",
        "Sowing window and preceding crop history",
        "Locally reviewed crop calendar or field-trial evidence",
        "Farm-specific input, labour, irrigation, and transport costs",
        "Sale grade and a verified buyer or farm-gate quote",
    ]
    if market_data.get("status") != "online" or not market_data.get("records"):
        gaps.append("A current official mandi observation feed; the available daily records are not a future price forecast")
    return {
        "status": "insufficient_data",
        "decision": "No crop is ranked as best until critical local inputs are verified.",
        "evaluated_at": _utc_timestamp(),
        "location": {"latitude": lat, "longitude": lon, "provenance": "request_coordinates"},
        "water_source_input": {
            "value": water_source,
            "provenance": "unverified_request_input",
            "note": "A selected option is not evidence of measured supply, borewell capacity, or drip availability.",
        },
        "weather_status": weather.get("status"),
        "weather_source": weather.get("source"),
        "weather_fetched_at": weather.get("fetched_at"),
        "market_status": market_data.get("status", "unavailable"),
        "market_as_of": market_data.get("as_of"),
        "market_source": market_data.get("source"),
        "market_message": market_data.get("message"),
        "catalog_version": catalog.get("catalog_version"),
        "missing_information": gaps,
        "crops": [build_crop_candidate(crop, weather, market_data) for crop in catalog["crops"]],
    }


def empty_soil_profile():
    return {
        "status": "not_measured",
        "source": None,
        "ph": None,
        "organic_carbon_pct": None,
        "available_n_kgha": None,
        "available_p_kgha": None,
        "available_k_kgha": None,
        "message": "No plot-specific soil test is connected. Regional soil context must not be shown as a measured plot result.",
    }
# ============================================================================
# HTTP REQUEST DISPATCHER
# ============================================================================

class DynamicEnterpriseAgriHandler(http.server.SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def send_json(self, status_code, data):
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        # 0. Health Check API
        if parsed.path == "/api/health":
            self.send_json(200, {
                "status": "UP",
                "version": "2.0.0",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
            return

        # Farmer profile: only user-provided identifiers are known at this stage.
        if parsed.path == "/api/farmer/profile":
            self.send_json(200, {
                "status": "profile_setup_required",
                "identity": {
                    "status": "not_authenticated",
                    "phone": None,
                    "message": "No authenticated identity or persisted farmer profile is configured."
                },
                "location": {
                    "village": "Hosanagalapura",
                    "taluk": "Molakalmuru",
                    "district": "Chitradurga",
                    "provenance": "pilot_locality",
                    "field_pin_status": "not_confirmed"
                },
                "parcel": {
                    "survey_number": "3",
                    "hissa_numbers": ["2", "4"],
                    "provenance": "farmer_declared",
                    "rtc_verification_status": "not_verified",
                    "area_acres": None,
                    "geometry": None
                },
                "soil_test": {"status": "not_provided", "results": None},
                "water_source": {"status": "not_confirmed", "details": None}
            })
            return
        # 0.08 Bhoomi Statutory Context API
        if parsed.path == "/api/cadastral/bhoomi":
            survey = params.get("survey", ["3"])[0]
            hissas = params.get("hissas", ["2,4"])[0].split(",")
            try:
                from backend.cadastral.bhoomi_gateway import get_bhoomi_rtc_context
                bhoomi_data = get_bhoomi_rtc_context(survey_number=survey, hissa_numbers=hissas)
                self.send_json(200, bhoomi_data)
                return
            except Exception as e:
                self.send_json(400, {"error": str(e)})
                return

        # 0.1 Mandi Prices API (Delegates directly to verified AGMARKNET service)
        if parsed.path == "/api/market/prices":
            district = params.get("district", ["Chitradurga"])[0]
            try:
                from backend.ingestion.agmarknet_service import get_latest_mandi_prices
                mandi_data = get_latest_mandi_prices(district=district)
                self.send_json(200, mandi_data)
                return
            except Exception as e:
                self.send_json(500, {"status": "error", "message": str(e)})
                return

        # Geographic coordinates are returned without fabricated soil, boundary, or route inferences.
        if parsed.path == "/api/geo/detect":
            try:
                lat, lon = _coordinates(params)
            except ValueError as exc:
                self.send_json(400, {"status": "invalid_request", "message": str(exc)})
                return
            self.send_json(200, {
                "status": "partial",
                "coordinates": {
                    "latitude": lat,
                    "longitude": lon,
                    "provenance": "request_coordinates"
                },
                "administrative": {
                    "status": "not_resolved",
                    "message": "Administrative boundaries are not inferred from an unverified point."
                },
                "soil_profile": empty_soil_profile(),
                "nearby_mandis": {
                    "status": "not_connected",
                    "message": "Verified market locations and road-route distances are not connected."
                }
            })
            return
        # Live weather only; upstream failure is reported without generated fallback values.
        if parsed.path == "/api/weather/live":
            try:
                lat, lon = _coordinates(params)
            except ValueError as exc:
                self.send_json(400, {"status": "invalid_request", "message": str(exc)})
                return
            weather = fetch_live_weather(lat, lon)
            self.send_json(200 if weather["status"] == "online" else 503, weather)
            return
        # Evidence-linked candidates; no profit ranking until local evidence supports it.
        if parsed.path == "/api/recommendations":
            try:
                lat, lon = _coordinates(params)
            except ValueError as exc:
                self.send_json(400, {"status": "invalid_request", "message": str(exc)})
                return
            water_source = params.get("water", [""])[0].strip().upper()
            if water_source not in ("BOREWELL", "RAINFED"):
                self.send_json(400, {
                    "status": "invalid_request",
                    "message": "Choose a water-source input; it will be treated as unverified until the farmer confirms it."
                })
                return
            district = params.get("district", ["Chitradurga"])[0]
            try:
                response = build_recommendations(lat, lon, water_source, district)
                self.send_json(200, response)
            except RuntimeError as exc:
                self.send_json(503, {"status": "unavailable", "message": str(exc), "crops": []})
            return
        # No unreviewed local package-of-practice or chemical advice is served.
        if parsed.path.startswith("/api/crops/") and parsed.path.endswith("/protocol"):
            crop_id = parsed.path.split("/")[-2]
            try:
                catalog = load_crop_catalog()
            except RuntimeError as exc:
                self.send_json(503, {"status": "unavailable", "message": str(exc)})
                return
            crop = next((item for item in catalog["crops"] if item.get("id") == crop_id), None)
            if crop is None:
                self.send_json(404, {"status": "not_found", "message": "Crop profile was not found in the evidence-linked catalog."})
                return
            self.send_json(200, {
                "status": "protocol_not_available",
                "crop": crop,
                "message": "A locally reviewed package of practices is not connected. No fertilizer dose, pesticide dose, or treatment instruction is provided."
            })
            return
        # 5. Serve Frontend App
        if parsed.path == "/" or parsed.path == "/index.html":
            file_path = os.path.join(FRONTEND_DIR, "farmer_app.html")
            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                self.send_json(500, {"error": str(e)})
                return

        return super().do_GET()

def start_server():
    os.chdir(FRONTEND_DIR)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), DynamicEnterpriseAgriHandler) as httpd:
        print("=" * 76)
        print("  BHUMI INTELLIGENCE — REAL-TIME DYNAMIC AGRONOMIC SERVER")
        print(f"  Live Server listening at: http://localhost:{PORT}")
        print("  Biophysical Suitability, STCR, & Mandi Logistics Engine Active")
        print("=" * 76)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    start_server()
