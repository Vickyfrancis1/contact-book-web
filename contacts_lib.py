import sqlite3

def find_contact(conn, name):
    cur = conn.cursor()
    name = name.strip().title()
    cur.execute("SELECT name, phone FROM contacts WHERE name = ?", (name,))
    return cur.fetchone()

def add_contact(conn, name, phone):
    name = name.strip().title()
    try:
        conn.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone.strip()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def delete_contact(conn, name):
    name = name.strip().title()
    cur = conn.execute("DELETE FROM contacts WHERE name = ?", (name,))
    conn.commit()
    return cur.rowcount > 0