"""Fetch total citation count from Google Scholar and write a shields.io endpoint JSON."""

import json
from scholarly import scholarly

SCHOLAR_ID = "5Wecal8AAAAJ"

def main():
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["indices"])
    total_citations = author.get("citedby", 0)
    print(f"Total citations: {total_citations}")

    # shields.io endpoint badge format
    data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(total_citations),
        "color": "9cf",
        "namedLogo": "Google Scholar",
        "logoColor": "blue",
    }

    with open("gs_data_shieldsio.json", "w") as f:
        json.dump(data, f, indent=2)
    print("Saved gs_data_shieldsio.json")

if __name__ == "__main__":
    main()
