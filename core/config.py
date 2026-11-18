"""Central configuration — colors, endpoints, constants."""
from __future__ import annotations

# ── Brand palette ─────────────────────────────────────────────
COLORS = {
    "bg":       "#090E18",
    "surface":  "#111C2D",
    "surface2": "#142238",
    "border":   "#26384D",
    "electric": "#19B8FF",
    "care":     "#A3F56B",
    "text":     "#F0F5FA",
    "muted":    "#9AABC0",
    "danger":   "#FF6B6B",
}

APP_TITLE = "CAREWAY"
APP_TAGLINE = "Smart Mobility & Healthcare Access"

# ── External services ─────────────────────────────────────────
HEADERS = {"User-Agent": "CAREWAY-StudentProject/1.0 (educational)"}
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "https://router.project-osrm.org/route/v1/driving"

# ── Defaults ──────────────────────────────────────────────────
DEFAULT_PLACE = "Пловдив, България"
DEFAULT_RADIUS_KM = 10
RADIUS_OPTIONS = [2, 3, 5, 10, 15, 25]

MODULES = [
    ("Dashboard",            "🏠"),
    ("PharmaNearby",         "💊"),
    ("SafeRide",             "🚐"),
    ("Smart Route",          "🧭"),
    ("Accessibility Center", "♿"),
    ("Data Analytics",       "📊"),
    ("Data Monitor",         "🛡️"),
]