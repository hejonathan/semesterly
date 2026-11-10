#!/bin/bash
# Re-import course data. Edit YEAR/TERM each semester.
YEAR=2027
TERM=Spring
cd "$(dirname "$0")"
docker compose exec -T web sh -c "python3 manage.py ingest jhu --years $YEAR --terms $TERM && python3 manage.py digest jhu"
