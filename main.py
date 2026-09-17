from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

app = FastAPI(title="TERRA X Backend")

security = HTTPBearer()


class Target(BaseModel):
    name: str
    latitude: float
    longitude: float


class UserLocation(BaseModel):
    latitude: float
    longitude: float
    accuracy: float | None = None


def supabase_request(method, endpoint, body=None, headers_extra=None):
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

    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    if headers_extra:
        headers.update(headers_extra)

    request = Request(
        url,
        data=data,
        headers=headers,
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


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    access_token = credentials.credentials

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SECRET_KEY")

    if not supabase_url or not supabase_key:
        raise HTTPException(
            status_code=500,
            detail="Supabase environment variables are missing"
        )

    url = supabase_url.rstrip("/") + "/auth/v1/user"

    request = Request(
        url,
        headers={
            "apikey": supabase_key,
            "Authorization": f"Bearer {access_token}"
        },
        method="GET"
    )

    try:
        with urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)

    except HTTPError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired login session"
        )

    except URLError:
        raise HTTPException(
            status_code=503,
            detail="Authentication service unavailable"
        )


def is_admin(user_id):
    data = supabase_request(
        "GET",
        f"/user_roles?select=role&user_id=eq.{user_id}&limit=1"
    )

    return bool(data and data[0].get("role") == "admin")


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


# =========================================================
# TERRA X LOCATION SYSTEM
# =========================================================

@app.post("/api/location")
def update_my_location(
    location: UserLocation,
    user=Depends(get_current_user)
):
    user_id = user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="User identity not found"
        )

    try:
        data = supabase_request(
            "POST",
            "/user_locations?on_conflict=auth_user_id",
            {
                "auth_user_id": user_id,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "accuracy": location.accuracy
            },
            {
                "Prefer": "resolution=merge-duplicates,return=representation"
            }
        )

        return {
            "status": "success",
            "message": "Location updated",
            "location": data[0] if data else None
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/api/my-location")
def get_my_location(
    user=Depends(get_current_user)
):
    user_id = user.get("id")

    try:
        data = supabase_request(
            "GET",
            f"/user_locations?select=id,auth_user_id,latitude,longitude,accuracy,updated_at&auth_user_id=eq.{user_id}&limit=1"
        )

        return {
            "status": "success",
            "location": data[0] if data else None
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/api/admin/locations")
def get_all_locations(
    user=Depends(get_current_user)
):
    user_id = user.get("id")

    if not user_id or not is_admin(user_id):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    try:
        data = supabase_request(
            "GET",
            "/user_locations?select=id,auth_user_id,latitude,longitude,accuracy,updated_at&order=updated_at.desc"
        )

        return {
            "status": "success",
            "count": len(data),
            "locations": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
