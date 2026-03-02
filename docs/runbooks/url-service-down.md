# URL Service – DOWN (Service Unreachable)

## Meaning
Prometheus cannot reach the `url-service` health endpoint.

This indicates the service is not running, not listening on its port, or the host network is unavailable.

Users cannot create or access shortened links while this alert is firing.

---

## Immediate Impact
- Redirects fail
- API requests fail
- Frontend integrations will break
- This is a full outage

---

## Quick Diagnosis

### 1. Check container status
```bash
docker compose ps
```