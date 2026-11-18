"""External API wrappers — geocoding, Overpass, OSRM."""
from __future__ import annotations

import math
from typing import Optional

import requests

from core.config import HEADERS, NOMINATIM_URL, OSRM_URL, OVERPASS_ENDPOINTS


# ── Geo helpers ───────────────────────────────────────────────
def haversine_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = math.radians(b[0] - a[0])
    dl = math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


def geocode(query: str) -> Optional[tuple[float, float, str]]:
    r = requests.get(
        NOMINATIM_URL,
        params={"q": query, "format": "jsonv2", "limit": 1, "countrycodes": "bg"},
        headers=HEADERS,
        timeout=20,
    )
    r.raise_for_status()
    data = r.json()
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]


# ── Overpass ──────────────────────────────────────────────────
def pharmacies_near(lat: float, lon: float, meters: int) -> list[dict]:
    query = (
        f'[out:json][timeout:35];'
        f'('
        f'node["amenity"="pharmacy"](around:{meters},{lat},{lon});'
        f'way["amenity"="pharmacy"](around:{meters},{lat},{lon});'
        f'relation["amenity"="pharmacy"](around:{meters},{lat},{lon});'
        f');out center tags;'
    )
    last_err: Optional[Exception] = None
    for endpoint in OVERPASS_ENDPOINTS:
        try:
            r = requests.post(endpoint, data={"data": query}, headers=HEADERS, timeout=45)
            r.raise_for_status()
            result = []
            for e in r.json().get("elements", []):
                t = e.get("tags", {})
                c = e.get("center", {})
                la = e.get("lat", c.get("lat"))
                lo = e.get("lon", c.get("lon"))
                if la is None or lo is None:
                    continue
                addr_parts = [
                    t.get("addr:street"),
                    t.get("addr:housenumber"),
                    t.get("addr:city") or t.get("addr:place"),
                ]
                result.append({
                    "id": f'{e["type"]}_{e["id"]}',
                    "name": t.get("name") or t.get("brand") or "Аптека без име",
                    "lat": float(la),
                    "lon": float(lo),
                    "address": ", ".join(str(x) for x in addr_parts if x) or "Няма адрес в OSM",
                    "phone": t.get("phone") or t.get("contact:phone") or "Няма телефон в OSM",
                    "hours": t.get("opening_hours") or "Няма работно време в OSM",
                    "wheelchair": t.get("wheelchair", "unknown"),
                })
            # deduplicate by name+coords
            unique = {(p["name"].lower(), round(p["lat"], 5), round(p["lon"], 5)): p for p in result}
            return list(unique.values())
        except Exception as ex:  # try next endpoint
            last_err = ex
    raise RuntimeError(f"Overpass failed: {last_err}")


# ── OSRM ──────────────────────────────────────────────────────
def road_route(a: tuple[float, float], b: tuple[float, float]) -> Optional[dict]:
    url = f"{OSRM_URL}/{a[1]},{a[0]};{b[1]},{b[0]}"
    r = requests.get(url, params={"overview": "full", "geometries": "geojson"}, headers=HEADERS, timeout=25)
    r.raise_for_status()
    data = r.json()
    if data.get("code") != "Ok":
        return None
    rt = data["routes"][0]
    return {
        "km": rt["distance"] / 1000,
        "min": rt["duration"] / 60,
        "line": [(y, x) for x, y in rt["geometry"]["coordinates"]],
    }