# 📇 Client & Vendor Contact Management System

A Python-based console application for managing business contacts for small and medium enterprises.

## 📁 Project Structure

```
contact-management-system/
│── contact.py          # Contact model / data class
│── data_handler.py     # JSON read/write + CSV export
│── business_logic.py   # CRUD operations & search logic
│── main.py             # Menu-driven console UI
│── contacts.json       # Auto-created persistent data store
│── contacts_export.csv # Generated on CSV export
│── README.md
```

## 🚀 How to Run

### Requirements
- Python 3.10 or above
- No external libraries needed (stdlib only)

### Steps
```bash
cd contact-management-system
python main.py
```

---

## ✨ Features

| Feature | Description |
|---|---|
| ➕ Add Contact | Create records with name, company, email, phone, category |
| 👁 View All | Tabular display of all contacts |
| 🏷 View by Category | Filter by Client / Vendor / Partner |
| 🔍 Search | Partial keyword search across all or specific fields |
| ✏️ Update | Modify any field of an existing contact |
| 🗑 Delete | Remove a contact with confirmation prompt |
| 📊 Dashboard | Summary count per category with bar chart |
| 📤 Export CSV | Export all contacts to a CSV file |

---

## 🗂 Data Storage

- Contacts are stored in **`contacts.json`** automatically after every change.
- Data persists between sessions — no database setup required.
- Export to **CSV** available from the menu.

---

## 🏗 Architecture

```
main.py  ──calls──►  business_logic.py  ──calls──►  data_handler.py  ──reads/writes──►  contacts.json
                            │
                            └──uses──►  contact.py  (Contact class)
```

---

## 📂 Categories

- **Client** – External clients / customers
- **Vendor** – Suppliers and service providers
- **Partner** – Strategic business partners

---

## 👨‍💻 Author
Built as part of the SME Business Tools internship project.
