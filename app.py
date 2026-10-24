import sqlite3
from flask import Flask, request
from contacts_lib import add_contact

app = Flask(__name__)

def setup_database():
    conn = sqlite3.connect("contacts.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

setup_database()

@app.route("/")
def home():
    return "Hello from my first web app!"

@app.route("/about")
def about():
    return "I am learning Python."

@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    conn = sqlite3.connect("contacts.db")
    message = ""
    
    if request.method == "POST":
        name = request.form["name"].strip()
        phone = request.form["phone"].strip()
        if not name or not phone:
            message = "<p style='color:red'>Please fill in both name and phone.</p>"
        elif add_contact(conn, name, phone):    
            message = "<p>Saved.</p>"
        else:
            message = "<p>That contact already exists.</p>"
             
    rows = conn.execute("SELECT name, phone FROM contacts ORDER BY name").fetchall()
    conn.close()
    
    html = "<h1>My Contacts</h1>" + message
    html = html + """
        <form method="post">
            <input name="name" placeholder="Name">
            <input name="phone" placeholder="Phone">
            <button type="submit">Add</button>
        </form>
    """          
    if not rows:
        html = html + "<p>No contacts yet.</p>"
    else:    
        html = html + "<ul>"
        for name, phone in rows:
            html = html + f"<li>{name}: {phone}</li>"
        html = html + "</ul>"
    return html

if __name__ == "__main__":
    app.run(debug=True)
