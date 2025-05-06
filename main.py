import tkinter as tk
from tkinter import messagebox, simpledialog
from auth import User
import sqlite3
import os

DB_PATH = "config.db"
user = User("admin", "root")  # Remplace "root" par le mot de passe choisi

# Création de la base de données si elle n'existe pas
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS blocked_sites (id INTEGER PRIMARY KEY, url TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS blocked_apps (id INTEGER PRIMARY KEY, name TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS time_limits (id INTEGER PRIMARY KEY, start TEXT, end TEXT)")
    conn.commit()
    conn.close()

# Interface principale
class ParentalControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contrôle Parental - GuardianLinux")
        self.create_login()

    def create_login(self):
        password = simpledialog.askstring("Authentification", "Entrez le mot de passe :", show='*')
        if not user.auth(password):  # Vérifie si le mot de passe est correct
            messagebox.showerror("Erreur", "Mot de passe incorrect.")
            self.root.destroy()  # Ferme l'application si échec
        else:
            self.create_main_ui()  # Si correct, affiche l'interface principale

    def create_main_ui(self):
        tk.Label(self.root, text="Bienvenue dans GuardianLinux", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="➕ Bloquer un site web", width=30, command=self.add_site).pack(pady=5)
        tk.Button(self.root, text="📛 Bloquer une application", width=30, command=self.add_app).pack(pady=5)
        tk.Button(self.root, text="⏰ Définir des horaires", width=30, command=self.set_time_limit).pack(pady=5)
        tk.Button(self.root, text="📋 Afficher les règles", width=30, command=self.view_rules).pack(pady=5)
        tk.Button(self.root, text="❌ Quitter", width=30, command=self.root.quit).pack(pady=10)

    def add_site(self):
        site = simpledialog.askstring("Nouveau site", "Entrez l'URL à bloquer (ex: facebook.com):")
        if site:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO blocked_sites (url) VALUES (?)", (site,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", f"{site} bloqué.")

    def add_app(self):
        app = simpledialog.askstring("Nouvelle application", "Nom du binaire à bloquer (ex: discord, steam):")
        if app:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO blocked_apps (name) VALUES (?)", (app,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", f"{app} bloqué.")

    def set_time_limit(self):
        start = simpledialog.askstring("Heure de début", "Format 24h (ex: 08:00):")
        end = simpledialog.askstring("Heure de fin", "Format 24h (ex: 20:00):")
        if start and end:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO time_limits (start, end) VALUES (?, ?)", (start, end))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", f"Horaire {start} → {end} enregistré.")

    def view_rules(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        sites = c.execute("SELECT url FROM blocked_sites").fetchall()
        apps = c.execute("SELECT name FROM blocked_apps").fetchall()
        times = c.execute("SELECT start, end FROM time_limits").fetchall()
        conn.close()

        rules = "🔐 Règles actuelles :\n\n"

        rules += "🌐 Sites bloqués:\n" + "\n".join(f" - {s[0]}" for s in sites) + "\n\n"
        rules += "📦 Applications bloquées:\n" + "\n".join(f" - {a[0]}" for a in apps) + "\n\n"
        rules += "⏰ Plages horaires:\n" + "\n".join(f" - {t[0]} à {t[1]}" for t in times)

        messagebox.showinfo("Règles définies", rules)

# Lancement
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = ParentalControlApp(root)
    root.mainloop()
