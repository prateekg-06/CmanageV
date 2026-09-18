
"""
business_logic.py – Business Logic Layer
Handles all CRUD operations and search/filter logic.
"""

from contact import Contact, VALID_CATEGORIES
from data_handler import load_contacts, save_contacts


# ──────────────────────────────────────────────
# CREATE
def add_contact(name: str, company: str, email: str, phone: str, category: str) -> Contact:
    """Create and persist a new contact. Returns the new Contact object."""
    contacts = load_contacts()

    # Duplicate email check
    for c in contacts:
        if c.email.lower() == email.strip().lower():
            raise ValueError(f"A contact with email '{email}' already exists (ID: {c.id}).")

    new_contact = Contact(name, company, email, phone, category)
    contacts.append(new_contact)
    save_contacts(contacts)
    return new_contact


# ──────────────────────────────────────────────
# READ
def get_all_contacts() -> list[Contact]:
    """Return all stored contacts."""
    return load_contacts()


def get_contact_by_id(contact_id: str) -> Contact | None:
    """Find a contact by its unique ID."""
    for c in load_contacts():
        if c.id == contact_id.upper():
            return c
    return None


def get_contacts_by_category(category: str) -> list[Contact]:
    """Return contacts filtered by category."""
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category. Choose from: {', '.join(VALID_CATEGORIES)}")
    return [c for c in load_contacts() if c.category == category]


# ──────────────────────────────────────────────
# SEARCH
def search_contacts(keyword: str, field: str = "all") -> list[Contact]:
    """
    Search contacts by keyword.
    field options: 'name', 'company', 'category', 'all'
    Supports partial/case-insensitive matching.
    """
    kw = keyword.strip().lower()
    results = []
    for c in load_contacts():
        if field == "name" and kw in c.name.lower():
            results.append(c)
        elif field == "company" and kw in c.company.lower():
            results.append(c)
        elif field == "category" and kw in c.category.lower():
            results.append(c)
        elif field == "all" and (
            kw in c.name.lower()
            or kw in c.company.lower()
            or kw in c.email.lower()
            or kw in c.category.lower()
        ):
            results.append(c)
    return results


# ──────────────────────────────────────────────
# UPDATE
def update_contact(contact_id: str, **fields) -> Contact:
    """
    Update fields of an existing contact.
    Allowed fields: name, company, email, phone, category
    """
    contacts = load_contacts()
    target = None
    for c in contacts:
        if c.id == contact_id.upper():
            target = c
            break

    if target is None:
        raise ValueError(f"No contact found with ID '{contact_id}'.")

    allowed = {"name", "company", "email", "phone", "category"}
    for key, value in fields.items():
        if key not in allowed:
            raise ValueError(f"'{key}' is not an updatable field.")
        if key == "category" and value not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")
        if value is not None:
            setattr(target, key, value.strip())

    save_contacts(contacts)
    return target


# ──────────────────────────────────────────────
# DELETE
def delete_contact(contact_id: str) -> Contact:
    """Delete a contact by ID. Returns the deleted contact."""
    contacts = load_contacts()
    for i, c in enumerate(contacts):
        if c.id == contact_id.upper():
            removed = contacts.pop(i)
            save_contacts(contacts)
            return removed
    raise ValueError(f"No contact found with ID '{contact_id}'.")
