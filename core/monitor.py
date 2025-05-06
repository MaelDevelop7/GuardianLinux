import time
import psutil
import sqlite3
import os
from datetime import datetime

# Chemin de la base de données
DB_PATH = "/opt/guardianlinux/config.db"

# Fonction pour vérifier les applications bloquées
def check_blocked_apps():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Récupérer les applications bloquées
    blocked_apps = c.execute("SELECT name FROM blocked_apps").fetchall()
    conn.close()
    
    # Vérifier si des applications bloquées sont en cours d'exécution
    for app in blocked_apps:
        app_name = app[0].lower()
        for proc in psutil.process_iter(['pid', 'name']):
            if app_name in proc.info['name'].lower():
                print(f"Bloquage en cours : {proc.info['name']} (PID {proc.info['pid']})")
                # Log d'un message dans un fichier log
                with open("/var/log/guardianlinux.log", "a") as log_file:
                    log_file.write(f"{datetime.now()} - Application bloquée : {proc.info['name']} (PID {proc.info['pid']})\n")
                proc.terminate()  # Terminée l'application bloquée

# Fonction pour vérifier les sites bloqués dans les navigateurs (ici un exemple pour Firefox)
def check_blocked_sites():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Récupérer les sites bloqués
    blocked_sites = c.execute("SELECT url FROM blocked_sites").fetchall()
    conn.close()

    # Vérification des processus des navigateurs
    for proc in psutil.process_iter(['pid', 'name']):
        if "firefox" in proc.info['name'].lower():
            for site in blocked_sites:
                blocked_url = site[0].lower()
                # Ici tu devrais avoir un moyen de récupérer l'URL de la session de Firefox
                # Cela peut nécessiter un outil comme `webbrowser` ou un script de surveillance de réseau
                print(f"Site bloqué détecté : {blocked_url}")
                # Si tu trouves le site dans l'activité de Firefox, tu pourrais fermer l'onglet ou l'application

# Fonction principale qui gère la surveillance
def monitor():
    while True:
        print("Vérification des applications bloquées...")
        check_blocked_apps()

        print("Vérification des sites bloqués...")
        check_blocked_sites()

        # Attendre un peu avant la prochaine vérification (par exemple, 30 secondes)
        time.sleep(30)

# Lancer le processus de surveillance
if __name__ == "__main__":
    print("Démarrage de GuardianLinux - Surveillance...")
    monitor()
