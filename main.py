"""
main.py – Main Application Entry Point
Menu-driven console interface for the Contact Management System.
"""

import os
import sys
from contact import VALID_CATEGORIES
from data_handler import export_to_csv
import business_logic as bl

# ── ANSI color helpers
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
RED     = "\033[91m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
DIM     = "\033[2m"

def clr(text, color): return f"{color}{text}{RESET}"
def success(msg): print(f"\n  {GREEN}✔  {msg}{RESET}")
def error(msg):   print(f"\n  {RED}✘  {msg}{RESET}")
def info(msg):    print(f"\n  {CYAN}ℹ  {msg}{RESET}")
def warn(msg):    print(f"\n  {YELLOW}⚠  {msg}{RESET}")

# ── Display helpers
CATEGORY_COLORS = {"Client": CYAN, "Vendor": YELLOW, "Partner": GREEN}

def print_header():
    os.system("cls" if os.name == "nt" else "clear")
    print(clr("""
║       CLIENT & VENDOR CONTACT MANAGEMENT SYSTEM          ║
║                  Business Edition v1.0                   ║
""", BOLD + CYAN))


def print_contact_row(c, index=None):
    tag_color = CATEGORY_COLORS.get(c.category, RESET)
    prefix = f"  {DIM}[{index}]{RESET} " if index is not None else "  "
    cat_tag = clr(f"[{c.category:7}]", tag_color + BOLD)
    print(f"{prefix}{cat_tag}  {BOLD}{c.name:<22}{RESET}  "
          f"{c.company:<20}  {DIM}{c.email:<28}  {c.phone}{RESET}")


def print_contact_detail(c):
    tag_color = CATEGORY_COLORS.get(c.category, RESET)
    sep = clr("─" * 54, DIM)
    print(f"""
  {sep}
  {BOLD}ID       :{RESET}  {c.id}
  {BOLD}Name     :{RESET}  {c.name}
  {BOLD}Company  :{RESET}  {c.company or '—'}
  {BOLD}Email    :{RESET}  {c.email}
  {BOLD}Phone    :{RESET}  {c.phone or '—'}
  {BOLD}Category :{RESET}  {clr(c.category, tag_color + BOLD)}
  {BOLD}Added    :{RESET}  {c.created_at}
  {sep}""")


def print_contact_table(contacts, title="All Contacts"):
    count = len(contacts)
    print(f"\n  {BOLD}{CYAN}{title}{RESET}  {DIM}({count} record{'s' if count != 1 else ''}){RESET}")
    if not contacts:
        warn("No contacts to display.")
        return
    print(f"  {DIM}{'─'*80}{RESET}")
    print(f"  {DIM}  {'Category':<11}  {'Name':<22}  {'Company':<20}  {'Email':<28}  Phone{RESET}")
    print(f"  {DIM}{'─'*80}{RESET}")
    for i, c in enumerate(contacts, 1):
        print_contact_row(c, i)
    print(f"  {DIM}{'─'*80}{RESET}")


def pause():
    input(f"\n  {DIM}Press Enter to continue…{RESET}")

# ── Input helpers
def prompt(label, required=True, default=""):
    val = input(f"  {BOLD}{label}{RESET}: ").strip()
    if not val and default:
        return default
    if required and not val:
        raise ValueError(f"{label} is required.")
    return val


def pick_category():
    print(f"\n  {BOLD}Category:{RESET}")
    for i, cat in enumerate(VALID_CATEGORIES, 1):
        color = CATEGORY_COLORS[cat]
        print(f"    {clr(str(i), BOLD)}. {clr(cat, color)}")
    choice = input("  Enter number (1-3): ").strip()
    idx = int(choice) - 1
    if idx < 0 or idx >= len(VALID_CATEGORIES):
        raise ValueError("Invalid category selection.")
    return VALID_CATEGORIES[idx]


# ── MENU ACTIONS
def add():
    print(clr("\n  ── ADD NEW CONTACT ──────────────────────────────", CYAN))
    try:
        name     = prompt("Name")
        company  = prompt("Company", required=False)
        email    = prompt("Email")
        phone    = prompt("Phone", required=False)
        category = pick_category()
        c = bl.add_contact(name, company, email, phone, category)
        success(f"Contact added successfully! ID: {BOLD}{c.id}{RESET}")
        print_contact_detail(c)
    except (ValueError, KeyboardInterrupt) as e:
        error(str(e))
    pause()


def viewAll():
    print(clr("\n  ── VIEW ALL CONTACTS ────────────────────────────", CYAN))
    contacts = bl.get_all_contacts()
    print_contact_table(contacts)
    pause()


def viewByCategory():
    print(clr("\n  ── VIEW BY CATEGORY ─────────────────────────────", CYAN))
    try:
        cat = pick_category()
        contacts = bl.get_contacts_by_category(cat)
        print_contact_table(contacts, title=f"{cat} Contacts")
    except (ValueError, KeyboardInterrupt) as e:
        error(str(e))
    pause()


def search():
    print(clr("\n  ── SEARCH CONTACTS ──────────────────────────────", CYAN))
    print(f"""
  Search in:
    {BOLD}1{RESET}. All fields
    {BOLD}2{RESET}. Name
    {BOLD}3{RESET}. Company
    {BOLD}4{RESET}. Category
""")
    field_map = {"1": "all", "2": "name", "3": "company", "4": "category"}
    choice = input("  Choose field (1-4): ").strip()
    field = field_map.get(choice, "all")
    keyword = input(f"  Enter keyword: ").strip()
    if not keyword:
        warn("Search keyword cannot be empty.")
    else:
        results = bl.search_contacts(keyword, field)
        print_contact_table(results, title=f'Search results for "{keyword}"')
    pause()


def update():
    print(clr("\n  ── UPDATE CONTACT ───────────────────────────────", CYAN))
    cid = input("  Enter Contact ID to update: ").strip().upper()
    c = bl.get_contact_by_id(cid)
    if not c:
        error(f"No contact found with ID '{cid}'.")
        pause()
        return

    print_contact_detail(c)
    print(f"  {DIM}Leave a field blank to keep the current value.{RESET}\n")
    try:
        fields = {}
        v = input(f"  Name       [{c.name}]: ").strip()
        if v: fields["name"] = v
        v = input(f"  Company    [{c.company}]: ").strip()
        if v: fields["company"] = v
        v = input(f"  Email      [{c.email}]: ").strip()
        if v: fields["email"] = v
        v = input(f"  Phone      [{c.phone}]: ").strip()
        if v: fields["phone"] = v
        print(f"\n  Current category: {clr(c.category, BOLD)}")
        change_cat = input("  Change category? (y/N): ").strip().lower()
        if change_cat == "y":
            fields["category"] = pick_category()

        if not fields:
            warn("No changes made.")
        else:
            updated = bl.update_contact(cid, **fields)
            success(f"Contact {BOLD}{updated.id}{RESET} updated successfully!")
            print_contact_detail(updated)
    except (ValueError, KeyboardInterrupt) as e:
        error(str(e))
    pause()


def delete():
    print(clr("\n  ── DELETE CONTACT ───────────────────────────────", CYAN))
    cid = input("  Enter Contact ID to delete: ").strip().upper()
    c = bl.get_contact_by_id(cid)
    if not c:
        error(f"No contact found with ID '{cid}'.")
        pause()
        return

    print_contact_detail(c)
    confirm = input(f"  {RED}Delete this contact? (yes/N): {RESET}").strip().lower()
    if confirm == "yes":
        try:
            bl.delete_contact(cid)
            success(f"Contact '{c.name}' (ID: {c.id}) deleted.")
        except ValueError as e:
            error(str(e))
    else:
        info("Delete cancelled.")
    pause()


def export():
    print(clr("\n  ── EXPORT TO CSV ────────────────────────────────", CYAN))
    contacts = bl.get_all_contacts()
    if not contacts:
        warn("No contacts to export.")
    else:
        fname = export_to_csv(contacts)
        success(f"Exported {len(contacts)} contact(s) to '{fname}'.")
    pause()


def summary():
    """Show a quick dashboard summary."""
    print(clr("\n  ── SUMMARY DASHBOARD ────────────────────────────", CYAN))
    contacts = bl.get_all_contacts()
    total = len(contacts)
    print(f"\n  {BOLD}Total Contacts:{RESET} {total}\n")
    for cat in VALID_CATEGORIES:
        count = len([c for c in contacts if c.category == cat])
        bar = clr("█" * count, CATEGORY_COLORS[cat])
        print(f"  {CATEGORY_COLORS[cat]}{cat:<8}{RESET}  {bar}  {count}")
    pause()


# ── MAIN MENU
MENU = [
    ("Add Contact",             add),
    ("View All Contacts",       viewAll),
    ("View by Category",        viewByCategory),
    ("Search / Filter",         search),
    ("Update Contact",          update),
    ("Delete Contact",          delete),
    ("Summary Dashboard",       summary),
    ("Export to CSV",           export),
    ("Exit",                    None),
]


def main():
    while True:
        print_header()
        print(f"  {BOLD}MAIN MENU{RESET}\n")
        for i, (label, _) in enumerate(MENU, 1):
            icon = "🚪" if label == "Exit" else "  "
            print(f"  {clr(str(i), BOLD + CYAN)}.  {icon} {label}")

        print()
        choice = input(f"  {BOLD}Select option (1–{len(MENU)}): {RESET}").strip()

        if not choice.isdigit():
            continue

        idx = int(choice) - 1
        if idx < 0 or idx >= len(MENU):
            continue

        label, action = MENU[idx]

        if action is None:  # Exit
            print(clr("\n  Goodbye! Thanks for using... 👋\n", GREEN + BOLD))
            sys.exit(0)

        print_header()
        action()


if __name__ == "__main__":
    main()
