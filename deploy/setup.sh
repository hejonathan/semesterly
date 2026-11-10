#!/bin/bash
# One-time server setup. Run from the deploy/ folder on an Ubuntu server:
#   bash setup.sh
set -euo pipefail
cd "$(dirname "$0")"

# 1. Docker
if ! command -v docker >/dev/null; then
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker "$USER"
fi

# 2. Oracle's Ubuntu images block ports with iptables; open 80/443.
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo apt-get install -y iptables-persistent >/dev/null 2>&1 || true
sudo netfilter-persistent save || true

# 3. Config (.env)
if [ ! -f .env ]; then
  IP=$(curl -s https://api.ipify.org)
  read -rp "JHU SIS API key: " JHU_KEY
  cat > .env <<ENV
SITE_DOMAIN=jhu.${IP//./-}.sslip.io
DB_PASSWORD=$(openssl rand -hex 16)
SECRET_KEY=$(openssl rand -hex 32)
JHU_API_KEY=$JHU_KEY
ENV
  chmod 600 .env
fi
source .env

# 4. Build and start
sudo docker compose up -d --build

# 5. Make Spring 2027 the newest semester in the picker
sudo docker compose exec -T web python3 manage.py shell -c "
from parsing.models import DataUpdateSettings as D
s = D.load(); s.max_allowed_year = 2027; s.max_allowed_term = 'Spring'
s.year = 2027; s.term = 'Spring'; s.active = True; s.save()"

# 6. Nightly course refresh at 3am, plus the first import now (~30 min)
chmod +x update_courses.sh
( crontab -l 2>/dev/null | grep -v update_courses.sh; echo "0 3 * * * sudo $(pwd)/update_courses.sh >> $(pwd)/update.log 2>&1" ) | crontab -
nohup sudo ./update_courses.sh > update.log 2>&1 &

echo
echo "Site: https://$SITE_DOMAIN"
echo "Courses are importing in the background (~30 min). Progress: tail -f $(pwd)/update.log"
