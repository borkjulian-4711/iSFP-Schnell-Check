import streamlit as st
import sqlite3
import hashlib

st.set_page_config(page_title="iSFP SaaS", layout="wide")

# -------------------------
# DB
# -------------------------
conn = sqlite3.connect("saas.db", check_same_thread=False)
c = conn.cursor()

# Tabellen
c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    customer_id INTEGER,
    name TEXT,
    data TEXT
)""")

conn.commit()

# -------------------------
# Passwort Hash
# -------------------------
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# -------------------------
# LOGIN / REGISTER
# -------------------------
st.sidebar.title("Login / Registrierung")

mode = st.sidebar.selectbox("Modus", ["Login", "Registrieren"])

username = st.sidebar.text_input("Benutzer")
password = st.sidebar.text_input("Passwort", type="password")

if mode == "Registrieren":
    if st.sidebar.button("Account erstellen"):
        c.execute("INSERT INTO users (username,password) VALUES (?,?)",
                  (username, hash_pw(password)))
        conn.commit()
        st.sidebar.success("Account erstellt")

if mode == "Login":
    if st.sidebar.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, hash_pw(password)))
        user = c.fetchone()
        
        if user:
            st.session_state["user_id"] = user[0]
            st.sidebar.success("Eingeloggt")
        else:
            st.sidebar.error("Falsche Daten")

# Stop wenn nicht eingeloggt
if "user_id" not in st.session_state:
    st.stop()

# -------------------------
# DASHBOARD
# -------------------------
st.title("📊 Dashboard")

user_id = st.session_state["user_id"]

# -------------------------
# KUNDEN
# -------------------------
st.header("👥 Kunden")

name = st.text_input("Kundenname")
email = st.text_input("E-Mail")

if st.button("Kunde speichern"):
    c.execute("INSERT INTO customers (name,email) VALUES (?,?)", (name,email))
    conn.commit()
    st.success("Kunde gespeichert")

c.execute("SELECT * FROM customers")
kunden = c.fetchall()

for k in kunden:
    st.write(f"{k[1]} – {k[2]}")

# -------------------------
# PROJEKTE
# -------------------------
st.header("🏠 Projekte")

proj_name = st.text_input("Projektname")

kunde_namen = [k[1] for k in kunden]
kunde = st.selectbox("Kunde auswählen", kunde_namen)

kunde_id = [k[0] for k in kunden if k[1] == kunde][0] if kunden else None

if st.button("Projekt speichern"):
    c.execute(
        "INSERT INTO projects (user_id,customer_id,name,data) VALUES (?,?,?,?)",
        (user_id, kunde_id, proj_name, "Demo-Daten")
    )
    conn.commit()
    st.success("Projekt gespeichert")

# Projekte anzeigen
c.execute("""
SELECT projects.name, customers.name
FROM projects
JOIN customers ON projects.customer_id = customers.id
WHERE projects.user_id=?
""", (user_id,))

for p in c.fetchall():
    st.write(f"{p[0]} (Kunde: {p[1]})")
