from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

app = FastAPI(title="TERRA X Backend")


class Target(BaseModel):
    name: str
    latitude: float
    longitude: float


def supabase_request(method, endpoint, body=None):
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SECRET_KEY")

    if not supabase_url or not supabase_key:
        raise Exception("Supabase environment variables are missing")

    base_url = supabase_url.rstrip("/")

    if not base_url.endswith("/rest/v1"):
        base_url += "/rest/v1"

    url = base_url + endpoint

    data = None

    if body is not None:
        data = json.dumps(body).encode("utf-8")

    request = Request(
        url,
        data=data,
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        },
        method=method
    )

    try:
        with urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8")

            if raw:
                return json.loads(raw)

            return []

    except HTTPError as e:
        details = e.read().decode("utf-8", errors="ignore")
        raise Exception(f"Supabase error {e.code}: {details}")

    except URLError as e:
        raise Exception(f"Connection error: {e.reason}")


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
    try:
        data = supabase_request(
            "GET",
            "/targets?select=id,name,latitude,longitude,created_at"
        )

        return {
            "status": "connected",
            "database": "Supabase",
            "table": "targets",
            "rows": len(data),
            "data": data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/targets")
def get_targets():
    try:
        data = supabase_request(
            "GET",
            "/targets?select=id,name,latitude,longitude,created_at&order=created_at.desc"
        )

        return {
            "status": "success",
            "count": len(data),
            "targets": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/api/targets")
def create_target(target: Target):
    try:
        data = supabase_request(
            "POST",
            "/targets",
            {
                "name": target.name,
                "latitude": target.latitude,
                "longitude": target.longitude
            }
        )

        return {
            "status": "success",
            "message": "Target saved successfully",
            "target": data[0] if data else None
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
