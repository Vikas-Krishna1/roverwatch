# RoverWatch: Rover Telemetry and Health Monitoring System

**By:** Vikas Krishna  
**Major:** Information Systems + Mechanical Engineering

## Overview

RoverWatch is a software-first engineering project that simulates a planetary rover's telemetry pipeline and monitors operational health.

The system generates and receives simulated sensor readings, validates and stores telemetry in a relational database, evaluates configurable health thresholds, and displays system status through an interactive dashboard.

RoverWatch combines Information Systems concepts such as databases, SQL, APIs, and visualization with Mechanical Engineering concepts such as temperature monitoring, wheel speed, battery behavior, and component operating limits.

## Problem Statement

Engineering sensor readings are useful when they are organized, analyzed, and connected to system conditions.

RoverWatch demonstrates an end-to-end workflow for transforming raw rover measurements into persistent records, visual trends, and actionable health alerts.

## Main Features

- Simulated rover telemetry
  - Battery voltage
  - Motor temperature
  - Wheel speed
  - Distance traveled
- Python telemetry generator
- Data-ingestion API
- Relational database with timestamped readings
- Component information and health status
- Configurable warning and critical thresholds
- Interactive monitoring dashboard
- Historical telemetry charts
- Alert history
- Automated tests for:
  - Normal readings
  - Threshold violations
  - Invalid data
- Future option for physical sensor/microcontroller integration

## Technology Stack

### Frontend

- React
- TypeScript
- Vite
- Plotly

### Backend

- Python
- FastAPI
- Uvicorn
- SQLModel / SQLAlchemy

### Database

- SQLite
- SQL

### Testing

- pytest
- HTTPX

### Development

- Git
- GitHub
- VS Code

## Project Scope

The initial version of RoverWatch uses simulated telemetry and runs locally.

The initial project does **not** include:

- Physical rover hardware
- Specialized electronics
- Cloud infrastructure
- Autonomous navigation
- Machine learning models

Hardware and physical sensors may be considered after the software MVP is complete.

## System Workflow

```text
Simulated Sensors
       ↓
Telemetry Generator
       ↓
FastAPI Ingestion API
       ↓
Validation
       ↓
SQLite Database
       ↓
Health / Threshold Evaluation
       ↓
Alerts + Historical Data
       ↓
React Dashboard
