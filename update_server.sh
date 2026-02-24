#!/bin/bash
set -e

# 1. In das Projektverzeichnis wechseln
cd ~/Documents/FeWo-Verwaltung/fewo_web/fewo/

# 2. Virtual Environment aktivieren
source fewo/bin/activate

# 3. Produktions-Settings setzen
export DJANGO_SETTINGS_MODULE=fewo.settings_production

# 4. Datenbank-Migrationen durchführen (falls nötig)
python manage.py migrate

# 5. Statische Dateien sammeln (für Nginx)
python manage.py collectstatic --noinput

# 6. Applikationsserver neu starten
sudo systemctl restart fewo

echo "Update erfolgreich abgeschlossen."
