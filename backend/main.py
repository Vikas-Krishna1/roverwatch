from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="RoverWatch API")


@app.get("/")
def root():
    return {"project": "RoverWatch", "status": "running"}


@app.get("/api/telemetry/sample")
def sample_telemetry():
    return {
        "component_id": "drive_motor",
        "metric": "motor_temperature",
        "value": 65.2,
        "unit": "degC",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }