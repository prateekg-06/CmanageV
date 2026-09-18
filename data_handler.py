"""
data_handler.py – Data Handling Module
Manages reading and writing contact data to/from a JSON file.
"""

import json
import os
from contact import Contact

DATA_FILE = "contacts.json"


def load_contacts() -> list[Contact]:
    """Load all contacts from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Contact.from_dict(record) for record in raw]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  [Warning] Could not read data file: {e}. Starting fresh.")
        return []


def save_contacts(contacts: list[Contact]) -> None:
    """Persist all contacts to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in contacts], f, indent=4, ensure_ascii=False)


def export_to_csv(contacts: list[Contact], filename: str = "contacts_export.csv") -> str:
    """Export contact list to a CSV file."""
    import csv
    fieldnames = ["id", "name", "company", "email", "phone", "category", "created_at"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in contacts:
            writer.writerow(c.to_dict())
    return filename
