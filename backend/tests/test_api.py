
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
# --------------------------------------------------
# 1. Root and health
# --------------------------------------------------
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "RoverWatch API is running"
    }
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
# --------------------------------------------------
# 2. Telemetry
# --------------------------------------------------
# Test the /telemetry endpoint to ensure it returns a list of telemetry readings.
def test_read_telemetry():
    response = client.get("/telemetry")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
#Check that the telemetry readings returned have the expected fields.
def test_read_telemetry_with_sensor_filter():
    response = client.get("/telemetry", params={"sensor_id": 7})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for reading in response.json():
        assert reading["sensor_id"] == 7
#Check that the telemetry readings returned have the expected fields., with a limit
#  on the number of readings returned.
def test_read_telemetry_with_limit():
    response = client.get("/telemetry", params={"limit": 5})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 5
# Check that the telemetry readings returned have the expected fields., with a limit
#  on the number of readings returned, and a sensor filter.
def test_read_telemetry_invalid_limit():
    response = client.get("/telemetry", params={"limit": 0})
    assert response.status_code == 422
# Check that the telemetry readings returned have the expected fields., with a limit
#  on the number of readings returned, and a sensor filter.
#Gives the  summary of telemetry readings for all sensors, 
# including the count of readings above a specified threshold.
def test_telemetry_summary():
    response = client.get("/telemetry/summary")
    assert response.status_code == 200

    data = response.json()
    assert "summaries" in data
    assert isinstance(data["summaries"], list)

    if data["summaries"]:
        summary = data["summaries"][0]
        for key in (
            "sensor_id",
            "metric",
            "unit",
            "reading_count",
            "minimum",
            "maximum",
            "average",
        ):
            assert key in summary

#Checks a telemetry reading for a specific sensor and metric, 
# including the count of readings above a specified threshold.
#With a nonsensical sensor ID, the endpoint should return a 404 error.
def test_read_single_telemetry_not_found():
    response = client.get("/telemetry/999999999")
    assert response.status_code == 404

#Gives a report of telemetry readings for a specific sensor and metric, 
# including the count of readings above a specified threshold.
def test_telemetry_report():
    response = client.get(
        "/telemetry/report",
        params={
            "sensor_id": 7,
            "metric": "TB Sensor 1A",
            "threshold": 280,
        },
       
    )
    print("Telemetry report response:", response.json())

    # Sensor 7 and its NASA metric should exist in your current DB.
    assert response.status_code == 200

    data = response.json()
    assert data["sensor_id"] == 7
    assert data["metric"] == "TB Sensor 1A"
    assert data["threshold"] == 280
    assert data["reading_count"] > 0


# --------------------------------------------------
# 3. Sensors
# --------------------------------------------------

def test_read_sensors():
    response = client.get("/sensors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_single_sensor():
    sensors_response = client.get("/sensors")
    assert sensors_response.status_code == 200

    sensors = sensors_response.json()
    if not sensors:
        return

    sensor_id = sensors[0]["id"]
    response = client.get(f"/sensors/{sensor_id}")

    assert response.status_code == 200
    assert response.json()["id"] == sensor_id


def test_read_sensor_not_found():
    response = client.get("/sensors/999999999")
    assert response.status_code == 404


def test_sensor_summary():
    response = client.get(
        "/sensors/summary",
        params={
            "sensor_id": 7,
            "metric": "TB Sensor 1A",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["sensor_id"] == 7
    assert data["metric"] == "TB Sensor 1A"
    assert data["threshold"] == 280.0
    assert "reading_count" in data

def test_sensor_summary_with_parameters():
    response = client.get(
        "/sensors/summary",
        params={
            "sensor_id": 7,
            "metric": "TB Sensor 1A",
            "threshold": 290,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["sensor_id"] == 7
    assert data["metric"] == "TB Sensor 1A"
    assert data["threshold"] == 290
    assert data["reading_count"] >= 0


# --------------------------------------------------
# 4. Rovers
# --------------------------------------------------

def test_read_rovers():
    response = client.get("/rovers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_single_rover():
    rovers_response = client.get("/rovers")
    assert rovers_response.status_code == 200

    rovers = rovers_response.json()
    if not rovers:
        return

    rover_id = rovers[0]["id"]
    response = client.get(f"/rovers/{rover_id}")

    assert response.status_code == 200
    assert response.json()["id"] == rover_id


def test_read_rover_not_found():
    response = client.get("/rovers/999999999")
    assert response.status_code == 404


# --------------------------------------------------
# 5. Components
# --------------------------------------------------

def test_read_components():
    response = client.get("/components")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_single_component():
    components_response = client.get("/components")
    assert components_response.status_code == 200

    components = components_response.json()
    if not components:
        return

    component_id = components[0]["id"]
    response = client.get(f"/components/{component_id}")

    assert response.status_code == 200
    assert response.json()["id"] == component_id


def test_read_component_not_found():
    response = client.get("/components/999999999")
    assert response.status_code == 404


# --------------------------------------------------
# 6. Threshold rules
# --------------------------------------------------

def test_read_threshold_rules():
    response = client.get("/threshold-rules")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# --------------------------------------------------
# 7. Alerts
# --------------------------------------------------

def test_read_alerts():
    response = client.get("/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_single_alert():
    alerts_response = client.get("/alerts")
    assert alerts_response.status_code == 200

    alerts = alerts_response.json()
    if not alerts:
        return

    alert_id = alerts[0]["id"]
    response = client.get(f"/alerts/{alert_id}")

    assert response.status_code == 200
    assert response.json()["id"] == alert_id


def test_read_alert_not_found():
    response = client.get("/alerts/999999999")
    assert response.status_code == 404


# --------------------------------------------------
# 8. Ingestion runs
# --------------------------------------------------

def test_read_ingestion_runs():
    response = client.get("/ingestion/runs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_ingestion_runs_with_limit():
    response = client.get(
        "/ingestion/runs",
        params={"limit": 2},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 2


def test_read_ingestion_runs_invalid_limit():
    response = client.get(
        "/ingestion/runs",
        params={"limit": 0},
    )
    assert response.status_code == 422


def test_read_ingestion_run():
    runs_response = client.get("/ingestion/runs")
    assert runs_response.status_code == 200

    runs = runs_response.json()
    if not runs:
        return

    run_id = runs[0]["id"]
    response = client.get(f"/ingestion/runs/{run_id}")

    assert response.status_code == 200
    assert response.json()["id"] == run_id


def test_read_ingestion_run_not_found():
    response = client.get("/ingestion/runs/999999999")
    assert response.status_code == 404


def test_read_rejected_records_for_run():
    runs_response = client.get("/ingestion/runs")
    assert runs_response.status_code == 200

    runs = runs_response.json()
    if not runs:
        return

    run_id = runs[0]["id"]
    response = client.get(
        f"/ingestion/runs/{run_id}/rejected"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_rejected_records_for_missing_run():
    response = client.get(
        "/ingestion/runs/999999999/rejected"
    )

    assert response.status_code == 200
    assert response.json() == []
