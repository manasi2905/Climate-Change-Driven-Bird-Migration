import requests
import csv
from datetime import datetime, timedelta

API_KEY = "d9vqrt0vijm4"

# Example regions (must be subnational for US)
regions = [
    # Pacific US + Alaska
    "US-CA", "US-OR", "US-WA", "US-AK",
    # Pacific Canada
    "CA-BC", "CA-YT",
    # Mexico & south
    "MX-BCN", "MX-SON", "MX-SIN", "MX-NAY", "MX-JAL",
    # Wintering areas
    "EC-G", "PE-LA", "CL-VS"
]

species_code = "wessan"

start_date = datetime(2013, 10, 1)
end_date   = datetime(2014, 10, 10)

headers = {"x-ebirdapitoken": API_KEY}

all_results = []

current = start_date
while current <= end_date:

    print(f"\n--- DATE {current.strftime('%Y-%m-%d')} ---")

    for region in regions:
        url = (
            f"https://api.ebird.org/v2/data/obs/{region}/historic/"
            f"{current.year}/{current.month:02}/{current.day:02}"
        )

        print(f"Requesting region {region} ... ", end="")

        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"ERROR {resp.status_code}")
            continue

        day_data = resp.json()

        # filter for species
        matches = [obs for obs in day_data if obs.get("speciesCode") == species_code]
        all_results.extend(matches)

        print(f"found {len(matches)} records")

    print(f"Total so far: {len(all_results)}")

    current += timedelta(days=1)

print(f"\nFINAL total records for {species_code}: {len(all_results)}")

# ---- Build full CSV header ----
keys = set()
for obs in all_results:
    keys.update(obs.keys())
keys = list(keys)

# ---- Save to CSV ----
with open("ebird_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(all_results)

print("\nSaved to ebird_data.csv")



