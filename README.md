# RoverWatch: Rover Telemetry and Health Monitoring System

**By:** Vikas Krishna  
**Major:** Information Systems + Mechanical Engineering

## Overview

RoverWatch is a software-first engineering project that simulates a planetary rover's telemetry pipeline and monitors its operational health.

The system will generate or receive sensor readings, validate and store them in a relational database, evaluate configurable health thresholds, and display the results through an interactive dashboard.

The project combines **Information Systems** concepts—including database design, SQL, APIs, and data visualization—with **Mechanical Engineering** concepts such as temperature monitoring, wheel speed, battery behavior, and component operating limits.

## Problem Statement

Engineering sensor readings are most useful when they can be organized, analyzed, and connected to identifiable system conditions.

RoverWatch will demonstrate how a software system can transform raw measurements into:

- Persistent records
- Visual data trends
- Component health information
- Actionable alerts

The goal is to create an end-to-end system that demonstrates how telemetry data can move from simulated sensors to a database and ultimately to a user-facing health monitoring dashboard.

## Main Features

- Simulated telemetry for:
  - Battery voltage
  - Motor temperature
  - Wheel speed
  - Distance traveled
- Python-based telemetry generator and data-ingestion API
- Relational database for storing:
  - Timestamped sensor readings
  - Component information
- Configurable warning and critical thresholds
- Interactive dashboard displaying:
  - Current component status
  - Historical charts
  - Alert history
- Automated tests covering:
  - Normal readings
  - Threshold violations
  - Invalid data
- Optional future extension using one physical sensor or microcontroller

## Technology Stack

### Frontend
- React
- TypeScript

### Backend
- Python
- FastAPI

### Database
- SQLite
- SQL

### Database Modeling
- SQLModel or SQLAlchemy

### Visualization
- Plotly

### Testing
- pytest

### Version Control
- Git
- GitHub

## Project Scope

The initial version of RoverWatch will use **simulated telemetry data** and run locally.

The project will **not** initially require:

- A physical rover
- Specialized electronics
- Cloud infrastructure
- Autonomous navigation
- Machine-learning models

Hardware integration will be considered only after the software MVP is complete.

## System Workflow

The intended telemetry workflow is:

```text
Simulated Sensor Data
        ↓
Telemetry Generator
        ↓
Data-Ingestion API
        ↓
Data Validation
        ↓
Relational Database
        ↓
Health Threshold Evaluation
        ↓
Alerts + Historical Data
        ↓
Interactive Dashboard
