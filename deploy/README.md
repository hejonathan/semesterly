# Self-hosting on one server

Runs Postgres + Django (gunicorn) + Caddy (automatic HTTPS) with Docker Compose.

1. Create an Ubuntu VM (Oracle Cloud "Always Free" Ampere A1 works well) and open
   TCP 80 and 443 in its network security list.
2. On the VM:
   ```bash
   git clone <this repo> semesterly && cd semesterly/deploy
   bash setup.sh
   ```
   It asks for your JHU SIS API key, then prints the site URL
   (`https://jhu.<ip-with-dashes>.sslip.io`). Courses take ~30 min to import the first time.

- Each semester: edit `YEAR`/`TERM` in `update_courses.sh` and update the
  Data Update Settings row (see setup.sh step 5).
- Logs: `docker compose logs -f web`
- Update code: `git pull && sudo docker compose up -d --build`
- Login (JHU SSO) is not configured; browsing and building schedules work without it.
