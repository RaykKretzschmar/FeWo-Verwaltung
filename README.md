# FeWo-Verwaltung (Customer Relationship Management)

Ein leichtgewichtiges, aber leistungsstarkes Kundenverwaltungsprogramm für Vermieter von Ferienwohnungen. Das System ist auf maximale Effizienz und Datensouveränität ausgelegt und läuft auf eigener Hardware.

> **⚠️ STATUS: PRIVATE BETA**
> Dieses Projekt wird aktuell **ausschließlich privat getestet**. Es steht nicht für die öffentliche Nutzung zur Verfügung und ist nicht Open Source. Der Zugriff ist strikt auf autorisierte Nutzer beschränkt.

---

## 📂 Dokumentation

Detaillierte Informationen zu den technologischen Entscheidungen und der Systemarchitektur findest du in den Architecture Decision Records:

📄 **[Architekturentscheidungen (ADR) ansehen](./FeWo_Verwaltung.pdf)**

---

## 🏗️ Systemarchitektur

Das Projekt folgt einer strikten Trennung von Verantwortlichkeiten (Separation of Concerns) und nutzt moderne Tunneling-Technologien, um ohne offene Ports sicher erreichbar zu sein.

### Der Request-Flow
1.  **User Client:** Browser (HTTPS)
2.  **Cloudflare Edge:** Terminierung von SSL & DDoS-Schutz
3.  **Cloudflare Tunnel (cloudflared):** Sichere Verbindung ins Heimnetzwerk
4.  **Raspberry Pi 5:** Host-System
5.  **Nginx:** Reverse Proxy & Auslieferung statischer Dateien (CSS/JS/Images)
6.  **Gunicorn:** WSGI Applikationsserver
7.  **Django:** Backend-Logik & ORM
8.  **SQLite:** Dateibasierte Datenbank

### Tech Stack
* **Hardware:** Raspberry Pi 5 (Active Cooling)
* **OS:** Raspberry Pi OS (Debian Bookworm)
* **Network:** Cloudflare Tunnel (Zero Trust)
* **Web Server:** Nginx
* **App Server:** Gunicorn (verwaltet via Systemd)
* **Backend:** Python 3 / Django
* **Frontend:** Django Templates & Vanilla JavaScript
* **Database:** SQLite

---

## 🛠️ Wartung & Betrieb

Da das System als `systemd`-Service läuft, erfolgen Start und Stopp automatisch. Hier sind die wichtigsten Befehle für die Wartung.

### 1. Updates einspielen (Workflow)
Wenn Änderungen am Code vorgenommen wurden (z.B. via Git Pull):

```bash
# 1. In das Projektverzeichnis wechseln
cd ~/Documents/FeWo-Verwaltung/fewo_web/fewo/

# 2. Virtual Environment aktivieren
source venv/bin/activate

# 3. Datenbank-Migrationen durchführen (falls nötig)
python manage.py migrate

# 4. Statische Dateien sammeln (für Nginx)
python manage.py collectstatic

# 5. Applikationsserver neu starten
sudo systemctl restart fewo
