"""
contact.py – Contact Model
Defines the Contact class representing a single contact record.
"""

import uuid
from datetime import datetime

VALID_CATEGORIES = ["Client", "Vendor", "Partner"]


class Contact:
    """Represents a single business contact."""

    def __init__(self, name: str, company: str, email: str, phone: str, category: str, contact_id: str = None):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if not email.strip():
            raise ValueError("Email cannot be empty.")
        if category not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")

        self.id = contact_id or str(uuid.uuid4())[:8].upper()
        self.name = name.strip()
        self.company = company.strip()
        self.email = email.strip()
        self.phone = phone.strip()
        self.category = category
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self) -> dict:
        """Serialize contact to a dictionary for storage."""
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "email": self.email,
            "phone": self.phone,
            "category": self.category,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Contact":
        """Deserialize a contact from a dictionary."""
        c = cls(
            name=data["name"],
            company=data.get("company", ""),
            email=data["email"],
            phone=data.get("phone", ""),
            category=data["category"],
            contact_id=data.get("id"),
        )
        c.created_at = data.get("created_at", c.created_at)
        return c

    def __repr__(self) -> str:
        return f"Contact(id={self.id}, name={self.name}, category={self.category})"
