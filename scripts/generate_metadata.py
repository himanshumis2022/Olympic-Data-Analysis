import os
import math
import requests
from collections import defaultdict
from statistics import fmean, median, pstdev

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
PAGE_LIMIT = 1000  # pull up to 1000 per page


def fetch_profiles(limit=PAGE_LIMIT, max_pages=50):
    """Fetch profiles in pages from the running API.
    Adjust as needed for your dataset size.
    """
    results = []
    page = 0
    while page < max_pages:
        resp = requests.get(f"{API_URL}/data/profiles", params={
            "skip": page * limit,
            "limit": limit,
        }, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("results", [])
        if not items:
            break
        results.extend(items)
        if len(items) < limit:
            break
        page += 1
    return results


def lat_band(lat: float, band=5) -> str:
    """Quantize latitude into bands like "-10_to_0", "0_to_10"."""
    lo = math.floor(lat / band) * band
    hi = lo + band
    return f"{int(lo)}_to_{int(hi)}"


def build_docs(profiles):
    """Aggregate profiles into concise region/time summaries suitable for RAG."""
    groups = defaultdict(list)
    for p in profiles:
        try:
            b = lat_band(float(p["latitude"]))
            y = int(p.get("year") or 0)
            m = int(p.get("month") or 0)
            key = (b, y, m)
            groups[key].append(p)
        except Exception:
            continue

    docs = []
    for (band, year, month), rows in groups.items():
        try:
            temps = [float(r["temperature"]) for r in rows if r.get("temperature") is not None]
            sals = [float(r["salinity"]) for r in rows if r.get("salinity") is not None]
            depths = [float(r["depth"]) for r in rows if r.get("depth") is not None]
            if not rows:
                continue
            summary_parts = [
                f"Latitude band {band.replace('_', ' ')}",
                f"Year {year}, Month {month}",
                f"Profiles {len(rows)}",
            ]
            if temps:
                t_avg = fmean(temps)
                t_med = median(temps)
                t_sd = pstdev(temps) if len(temps) > 1 else 0.0
                summary_parts.append(
                    f"Temp avg {t_avg:.2f}°C, med {t_med:.2f}, sd {t_sd:.2f} (min {min(temps):.2f}, max {max(temps):.2f})"
                )
            if sals:
                s_avg = fmean(sals)
                s_med = median(sals)
                s_sd = pstdev(sals) if len(sals) > 1 else 0.0
                summary_parts.append(
                    f"Sal avg {s_avg:.2f} PSU, med {s_med:.2f}, sd {s_sd:.2f} (min {min(sals):.2f}, max {max(sals):.2f})"
                )
            if depths:
                summary_parts.append(
                    f"Depth range {min(depths):.0f}–{max(depths):.0f} m"
                )
            text = ". ".join(summary_parts) + "."
            doc_id = f"band:{band}|y:{year}|m:{month}"
            docs.append({"id": doc_id, "text": text})
        except Exception:
            continue
    return docs


def post_docs(docs):
    if not docs:
        print("No docs to index.")
        return
    payload = {"docs": docs}
    resp = requests.post(f"{API_URL}/admin/index", json=payload, timeout=120)
    resp.raise_for_status()
    print(resp.json())


if __name__ == "__main__":
    print(f"Using API_URL={API_URL}")
    profs = fetch_profiles()
    print(f"Fetched {len(profs)} profiles")
    docs = build_docs(profs)
    print(f"Built {len(docs)} docs")
    post_docs(docs)
