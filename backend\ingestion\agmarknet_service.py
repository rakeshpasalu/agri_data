"""AGMARKNET daily wholesale-price ingestion for the Molakalmuru pilot.

This module has no commodity whitelist and never supplies example prices. It
returns source observations from data.gov.in, with the original arrival date,
or an explicit setup/unavailable status when it cannot verify the feed.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
RESOURCE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"
RESOURCE_PAGE = "https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi"
SOURCE_NAME = "AGMARKNET via data.gov.in"
STATE = "Karnataka"
CACHE_TTL_SECONDS = 24 * 60 * 60
REQUEST_TIMEOUT_SECONDS = 15
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
_ROOT = Path(__file__).resolve().parents[2]
CACHE_PATH = _ROOT / "data" / "cache" / "mandi_prices.json"
_lock = threading.RLock()


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _iso_utc(value: dt.datetime | None = None) -> str:
    return (value or _utc_now()).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _fold(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or "").casefold())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(re.findall(r"[a-z0-9]+", text))


def _field_key(value: Any) -> str:
    text = str(value or "").casefold()
    text = re.sub(r"_x0*020_", " ", text)
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def _row_value(row: dict, *names: str) -> Any:
    lookup = {_field_key(k): v for k, v in row.items()}
    for name in names:
        key = _field_key(name)
        if key in lookup:
            return lookup[key]
    return None


def _price(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    text = re.sub(r"[^0-9.+-]", "", text)
    try:
        result = float(text)
    except (TypeError, ValueError):
        return None
    if result < 0 or result != result or result in (float("inf"), float("-inf")):
        return None
    return result


def _arrival_date(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return dt.datetime.strptime(text[:19], fmt).date().isoformat()
        except ValueError:
            continue
    try:
        return dt.datetime.fromisoformat(text.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def _normalize_record(row: dict, requested_district: str) -> dict | None:
    state = str(_row_value(row, "state") or "").strip()
    district = str(_row_value(row, "district") or "").strip()
    commodity = str(_row_value(row, "commodity") or "").strip()
    market = str(_row_value(row, "market") or "").strip()
    variety = str(_row_value(row, "variety") or "").strip()
    grade = str(_row_value(row, "grade") or "").strip()
    arrival = _arrival_date(_row_value(row, "arrival_date", "arrival date"))
    modal = _price(_row_value(row, "modal_price", "modal price", "modal"))
    minimum = _price(_row_value(row, "min_price", "min price", "minimum_price", "minimum price"))
    maximum = _price(_row_value(row, "max_price", "max price", "maximum_price", "maximum price"))

    # Require an actual district and state in the source row, rather than
    # backfilling them from the request; this keeps every returned row traceable.
    if _fold(state) != _fold(STATE) or _fold(district) != _fold(requested_district):
        return None
    if not commodity or not market or not arrival or modal is None:
        return None

    record = {
        "commodity": commodity,
        "market": market,
        "district": district,
        "variety": variety,
        "min_price": minimum,
        "modal_price": modal,
        "max_price": maximum,
        "arrival_date": arrival,
        "price_unit": "INR/quintal",
        "source": SOURCE_NAME,
    }
    if grade:
        record["grade"] = grade
    return record


def _fetch_official(district: str, api_key: str) -> list[dict]:
    params = [
        ("api-key", api_key),
        ("format", "json"),
        ("limit", "1000"),
        ("offset", "0"),
        ("sort[arrival_date]", "desc"),
        ("filters[State]", STATE),
        ("filters[District]", district),
    ]
    url = f"{RESOURCE_URL}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Bhumi-Farmer-Pilot/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            if response.status != 200:
                raise RuntimeError(f"data.gov.in returned HTTP {response.status}")
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except urllib.error.HTTPError as exc:
        # Do not propagate the request URL: it contains the API key.
        raise RuntimeError(f"data.gov.in returned HTTP {exc.code}") from None
    if len(body) > MAX_RESPONSE_BYTES:
        raise RuntimeError("data.gov.in response exceeded the configured size limit")
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("data.gov.in returned invalid JSON") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise RuntimeError("data.gov.in response did not contain a records list")

    records = []
    for row in payload["records"]:
        if isinstance(row, dict):
            normalized = _normalize_record(row, district)
            if normalized:
                records.append(normalized)
    return _deduplicate(records)


def _deduplicate(records: list[dict]) -> list[dict]:
    unique = {}
    for row in records:
        key = (
            _fold(row.get("commodity")),
            _fold(row.get("market")),
            _fold(row.get("variety")),
            _fold(row.get("grade")),
            row.get("arrival_date"),
        )
        unique[key] = row
    return sorted(
        unique.values(),
        key=lambda row: (
            row.get("arrival_date", ""),
            _fold(row.get("market")),
            _fold(row.get("commodity")),
        ),
        reverse=True,
    )


def _read_cache(district: str) -> dict | None:
    try:
        with CACHE_PATH.open("r", encoding="utf-8") as stream:
            payload = json.load(stream)
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or _fold(payload.get("district")) != _fold(district):
        return None
    if not isinstance(payload.get("records"), list) or not payload.get("fetched_at"):
        return None
    return payload


def _cache_age_seconds(payload: dict) -> float | None:
    try:
        fetched = dt.datetime.fromisoformat(str(payload["fetched_at"]).replace("Z", "+00:00"))
        if fetched.tzinfo is None:
            fetched = fetched.replace(tzinfo=dt.timezone.utc)
        return max(0.0, (_utc_now() - fetched.astimezone(dt.timezone.utc)).total_seconds())
    except (KeyError, TypeError, ValueError):
        return None


def _write_cache(district: str, records: list[dict]) -> dict:
    as_of = max((row["arrival_date"] for row in records), default=None)
    payload = {
        "schema_version": 1,
        "status": "online" if records else "no_data",
        "state": STATE,
        "district": district,
        "as_of": as_of,
        "fetched_at": _iso_utc(),
        "source": {
            "name": SOURCE_NAME,
            "resource_id": RESOURCE_ID,
            "url": RESOURCE_PAGE,
            "granularity": "daily",
        },
        "delivery": "upstream",
        "records": records,
    }
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = CACHE_PATH.with_suffix(CACHE_PATH.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp_path, CACHE_PATH)
    return payload


def _response_from_cache(payload: dict, status: str, delivery: str, message: str | None = None) -> dict:
    result = dict(payload)
    result["status"] = status
    result["delivery"] = delivery
    result["cache_ttl_seconds"] = CACHE_TTL_SECONDS
    if message:
        result["message"] = message
    return result


def get_latest_mandi_prices(district: str = "Chitradurga") -> dict:
    """Return verified daily district mandi rows in the shared HTTP schema.

    Successful upstream responses are cached for 24 hours. On a keyless start,
    this function returns setup_required unless it can serve a previously
    verified cache; expired verified rows are explicitly marked stale.
    """
    district = " ".join(str(district or "").split())
    if not district or len(district) > 80:
        return {
            "status": "unavailable",
            "records": [],
            "as_of": None,
            "source": {"name": SOURCE_NAME, "resource_id": RESOURCE_ID, "url": RESOURCE_PAGE},
            "message": "A valid district name is required.",
        }

    with _lock:
        cached = _read_cache(district)
        age = _cache_age_seconds(cached) if cached else None
        fresh = cached is not None and age is not None and age < CACHE_TTL_SECONDS
        api_key = os.environ.get("DATA_GOV_IN_API_KEY", "").strip()

        if fresh:
            return _response_from_cache(
                cached,
                cached.get("status", "online"),
                "cache",
                "Official daily response served from the local cache; see each arrival date.",
            )

        if not api_key:
            if cached and cached.get("records"):
                return _response_from_cache(
                    cached,
                    "stale",
                    "cache",
                    "API key is not configured. Showing older verified observations with their original dates.",
                )
            return {
                "status": "setup_required",
                "state": STATE,
                "district": district,
                "as_of": None,
                "fetched_at": None,
                "source": {"name": SOURCE_NAME, "resource_id": RESOURCE_ID, "url": RESOURCE_PAGE, "granularity": "daily"},
                "delivery": "none",
                "records": [],
                "message": "Set DATA_GOV_IN_API_KEY on the server to connect the official feed. No sample prices are shown.",
            }

        try:
            rows = _fetch_official(district, api_key)
        except Exception:
            if cached and cached.get("records"):
                return _response_from_cache(
                    cached,
                    "stale",
                    "cache",
                    "The official feed could not be refreshed. Showing older verified observations with their original dates.",
                )
            return {
                "status": "unavailable",
                "state": STATE,
                "district": district,
                "as_of": None,
                "fetched_at": None,
                "source": {"name": SOURCE_NAME, "resource_id": RESOURCE_ID, "url": RESOURCE_PAGE, "granularity": "daily"},
                "delivery": "none",
                "records": [],
                "message": "The official data.gov.in feed could not be verified. No sample prices are shown.",
            }

        payload = _write_cache(district, rows)
        return _response_from_cache(
            payload,
            "online" if rows else "no_data",
            "upstream",
            None if rows else "The official feed returned no matching district records for this refresh.",
        )


__all__ = ["get_latest_mandi_prices", "CACHE_PATH", "CACHE_TTL_SECONDS", "RESOURCE_ID"]
