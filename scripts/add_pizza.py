#!/usr/bin/env python3
"""
add_pizza.py — add a new pizza entry to the log.
Usage: python scripts/add_pizza.py
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
PIZZAS_DIR = ROOT / "pizzas"
PLACES_FILE = ROOT / "places.json"

SERVICE_OPTIONS = ["eat-in", "delivery", "take-away"]
TYPE_OPTIONS = ["rossa", "bianca", "well-done"]


def load_places():
    with open(PLACES_FILE) as f:
        return json.load(f)


def save_places(places):
    with open(PLACES_FILE, "w") as f:
        json.dump(places, f, indent=2)
        f.write("\n")


def pick_place(places):
    print("\nKnown places:")
    for i, p in enumerate(places, 1):
        print(f"  {i}. {p['name']}")
    print(f"  {len(places) + 1}. Add new place")

    choice = input("\nPick a place: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(places):
            return places[idx], places
        elif idx == len(places):
            return add_new_place(places)
    print("Invalid choice, try again.")
    return pick_place(places)


def add_new_place(places):
    name = input("Place name: ").strip()
    maps = input("Google Maps link (optional): ").strip() or None
    slug = name.lower().replace(" ", "-")
    new_place = {"id": slug, "name": name, "maps": maps}
    places.append(new_place)
    save_places(places)
    print(f"Added '{name}' to places.json")
    return new_place, places


def pick_option(label, options):
    print(f"\n{label}:")
    for i, o in enumerate(options, 1):
        print(f"  {i}. {o}")
    choice = input("Pick: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        return options[int(choice) - 1]
    print("Invalid, try again.")
    return pick_option(label, options)


def main():
    today = datetime.now().strftime("%Y%m%d")
    date_input = input(f"Date [{today}]: ").strip() or today
    filename = PIZZAS_DIR / f"{date_input}.json"

    if filename.exists():
        print(f"Warning: {filename.name} already exists. Overwrite? (y/N) ", end="")
        if input().strip().lower() != "y":
            print("Aborted.")
            return

    places = load_places()
    place, places = pick_place(places)

    pizza_name = input("\nPizza name: ").strip()
    service = pick_option("Service", SERVICE_OPTIONS)
    pizza_type = pick_option("Type", TYPE_OPTIONS)

    stars_input = input("\nStars (1–5): ").strip()
    stars = int(stars_input) if stars_input.isdigit() and 1 <= int(stars_input) <= 5 else 3

    notes = input("Notes (optional): ").strip()

    entry = {
        "name": pizza_name,
        "place": place["id"],
        "service": service,
        "type": pizza_type,
        "stars": stars,
    }
    if notes:
        entry["notes"] = notes

    with open(filename, "w") as f:
        json.dump(entry, f, indent=2)
        f.write("\n")

    print(f"\nSaved {filename.name}")

    # Git commit + push
    push = input("Commit and push? (Y/n): ").strip().lower()
    if push != "n":
        subprocess.run(["git", "add", str(filename), str(PLACES_FILE)], cwd=ROOT)
        subprocess.run(["git", "commit", "-m", f"pizza: {date_input} — {pizza_name} at {place['name']}"], cwd=ROOT)
        subprocess.run(["git", "push"], cwd=ROOT)
        print("Pushed.")


if __name__ == "__main__":
    main()
