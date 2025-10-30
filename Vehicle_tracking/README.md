# Vehicle Tracking System

A Python-based application for real-time vehicle tracking and monitoring using Snowflake database integration. This tool provides a GUI interface for tracking vehicle production events and status updates.

## Features

- Real-time vehicle tracking using MIX numbers
- Snowflake database integration
- Multi-threaded processing for responsive GUI
- Progress monitoring and status updates
- Production event tracking
- Body event monitoring

## Technical Overview

### Database Integration
- Connects to Volvo Cars Manufacturing Analytics Snowflake instance
- Accesses production control data
- Monitors order and body events
- Real-time data querying and processing

### Data Sources
- `VCC.PROD_CONTROL.ORDER_EVENTS`
  - Mix number tracking
  - Body number correlation
- `VCC.PROD_CONTROL.BODY_EVENTS`
  - Registration point tracking
  - Vehicle specifications
  - Production timestamps
  - Color and type information

## Requirements

- Python 3.x
- PyQt5
- snowflake-snowpark-python
- pandas
- Access to Volvo Cars Snowflake environment

## Installation

1. Install required Python packages:
```powershell
pip install PyQt5 snowflake-snowpark-python pandas
```

2. Ensure Snowflake access credentials are configured

## Usage

1. Launch the application:
```powershell
python intranet_monitor_snowflake.py
```

2. Enter your Snowflake user credentials when prompted

3. Input the MIX number of the vehicle to track

4. Monitor real-time updates in the GUI

## Features

### GUI Components
- Input field for MIX number
- Progress bar for tracking operations
- Status updates display
- Real-time event monitoring

### Tracking Capabilities
- Vehicle location in production line
- Current production stage
- Body event history
- Registration point status
- Vehicle specifications

## Configuration

Default Snowflake connection parameters:
- Account: VOLVOCARS-MANUFACTURINGANALYTICS
- Role: SELF_SERVICE_USER
- Warehouse: REPORTING
- Database: VCC
- Schema: PROD_CONTROL
- Authenticator: externalbrowser

## Threading

The application uses QThread for background processing:
- Main thread handles GUI
- Worker thread manages database operations
- Progress updates via PyQt signals
- Graceful thread termination support

## Notes

- Requires valid Snowflake credentials
- External browser authentication is used for security
- Real-time monitoring depends on network connectivity
- Regular session refresh for long-term monitoring