# RoverWatch — Project Brief

**Developer:** Vikas Krishna  
**Major:** Information Systems + Mechanical Engineering

## Project Goal

RoverWatch is a software-first rover telemetry and health-monitoring system designed to simulate how engineering sensor data can be collected, validated, stored, analyzed, and visualized.

The initial MVP will use simulated telemetry and run locally.

## Problem

Raw rover sensor measurements are only useful when they can be organized and connected to system health.

RoverWatch demonstrates an end-to-end workflow for:

1. Collecting telemetry
2. Validating measurements
3. Storing telemetry
4. Evaluating component health
5. Detecting threshold violations
6. Generating alerts
7. Visualizing system status and historical data

## Core Telemetry

The initial system will simulate:

- Battery voltage
- Motor temperature
- Wheel speed
- Distance traveled

## Backend

The Python/FastAPI backend will:

- Receive telemetry
- Validate incoming data
- Store telemetry measurements
- Track rover components
- Evaluate configurable health thresholds
- Generate health alerts

## Database

SQLite will be used for the initial database.

The database will store:

- Component information
- Telemetry measurements
- Timestamps
- Threshold information
- Health and alert information

## Frontend

The React dashboard will display:

- Current rover telemetry
- Component health
- Warning and critical conditions
- Historical telemetry
- Alert history
- Interactive charts

## System Architecture

```text
Simulated Sensors
       ↓
Telemetry Generator
       ↓
FastAPI Ingestion API
       ↓
Data Validation
       ↓
SQLite Database
       ↓
Health / Threshold Evaluation
       ↓
Alerts + Historical Data
       ↓
React Dashboard
