from fastapi import FastAPI

app = FastAPI(title="TERRA X Backend")


@app.get("/")
def root():
    return {
        "project": "TERRA X",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
