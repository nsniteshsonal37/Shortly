# URL Service — High Error Rate

## Alert Meaning

More than 5% of URL service requests are failing for at least 2 minutes.

User impact:
Users cannot create or open short links.

---

## Immediate Checks

### 1. Verify service is responding

```
curl http://localhost:8001/
```

If HTTP 200 → service alive, continue.
If connection refused → container likely crashed.

---

### 2. Inspect logs

```
docker compose logs url-service --tail=50
```

Look for:

* database connection errors
* stack traces
* migration failures

---

## Common Causes

### Database not ready

Symptoms:
`connection refused` to postgres

Fix:

```
docker compose restart url-service
```

### Broken migration

Symptoms:
SQLAlchemy errors

Fix:

```
docker compose exec url-service alembic upgrade head
```

---

## Recovery Verification

The alert will auto-resolve once error rate drops below 5%.

No manual Grafana action is required.
