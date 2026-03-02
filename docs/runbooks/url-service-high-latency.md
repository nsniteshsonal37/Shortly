# URL Service – High Latency (p95 > 500ms)

## Meaning
The URL service is responding slowly. Users may experience delayed redirects or API responses.

This alert fires when 5% of requests take longer than 500ms for more than 2 minutes.

---

## Quick Diagnosis

1. Check containers
docker compose ps

2. Check logs
docker compose logs url-service --tail=100

3. Check CPU / memory
docker stats

4. Check database connectivity
docker compose logs auth-service --tail=50

---

## Common Causes
- database slow queries
- container CPU starvation
- host under heavy load
- connection pool exhaustion
- infinite redirect loops

---

## Immediate Mitigation
1. Restart URL service
docker compose restart url-service

2. If still slow:
restart database container

3. If still slow:
restart entire stack
docker compose down
docker compose up -d

---

## Verification
Open Grafana → p95 latency panel

Latency should drop below 300ms within 2 minutes.

---

## Escalation
If unresolved:
- inspect recent code changes
- check network/DNS issues