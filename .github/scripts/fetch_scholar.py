"""Fetch Google Scholar citation count via SerpAPI and write shields.io endpoint JSON."""

import json
import os
import sys
import requests

SCHOLAR_ID = "5Wecal8AAAAJ"


def fetch_citations() -> int:
    api_key = os.environ.get("SERPAPI_KEY")
    if not api_key:
        raise EnvironmentError("SERPAPI_KEY environment variable not set.")

    params = {
        "engine": "google_scholar_author",
        "author_id": SCHOLAR_ID,
        "api_key": api_key,
    }
    resp = requests.get("https://serpapi.com/search", params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    try:
        total = data["cited_by"]["table"][0]["citations"]["all"]
    except (KeyError, IndexError) as e:
        print(json.dumps(data, indent=2), file=sys.stderr)
        raise RuntimeError(f"Unexpected SerpAPI response structure: {e}")

    print(f"Total citations: {total}")
    return total


def main():
    total = fetch_citations()
    data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(total),
        "color": "9cf",
    }
    with open("gs_data_shieldsio.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Saved gs_data_shieldsio.json")


if __name__ == "__main__":
    main()
