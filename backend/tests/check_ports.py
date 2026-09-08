import httpx

for url, name in [
    ("http://127.0.0.1:8000/api/health", "Backend (Port 8000)"),
    ("http://127.0.0.1:3000", "Frontend (Port 3000)"),
    ("http://127.0.0.1:3000/api/health", "Frontend Rewrite Proxy"),
]:
    try:
        r = httpx.get(url, timeout=15.0)
        print(f"[ONLINE]  {name}: status {r.status_code}")
    except Exception as e:
        print(f"[OFFLINE] {name}: {e}")
