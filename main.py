from fastapi import FastAPI
import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

app = FastAPI(title="TERRA X Backend")


@app.get("/")
def root():
    return {
        "project": "TERRA X",
        "status": "online",
        "backend": "FastAPI"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-test")
def db_test():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SECRET_KEY")

    if not supabase_url:
        return {
            "status": "error",
            "message": "SUPABASE_URL is missing"
        }

    if not supabase_key:
        return {
            "status": "error",
            "message": "SUPABASE_SECRET_KEY is missing"
        }

    base_url = supabase_url.rstrip("/")

    if not base_url.endswith("/rest/v1"):
        base_url += "/rest/v1"

    url = base_url + "/targets?select=id,name,latitude,longitude,created_at"

    request = Request(
        url,
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        },
        method="GET"
    )

    try:
        with urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        return {
            "status": "connected",
            "database": "Supabase",
            "table": "targets",
            "rows": len(data),
            "data": data
        }

    except HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")

        return {
            "status": "error",
            "message": "Supabase request failed",
            "http_status": e.code,
            "details": body
        }

    except URLError as e:
        return {
            "status": "error",
            "message": "Could not reach Supabase",
            "details": str(e.reason)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Unexpected error",
            "details": str(e)
        }
