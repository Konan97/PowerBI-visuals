# Fault Data Preparation Tools

A collection of Python scripts for processing, analyzing, and preparing fault data from various sources in Volvo Cars manufacturing environment. These tools handle ECU data, project mixing, and QBay data preparation for PowerBI visualization.

## Scripts Overview

### QBay PowerBI Database (`qbay_powerbi_db.py`)
- Processes fault data from QBay First Run
- Merges and filters data from different software releases (REL3.1, REL3.2, etc.)
- Categorizes faults based on predefined processes
- Handles data cleaning and missing value management
- Exports processed data for PowerBI integration

### ECU List Management (`ECU_list.py`)
- Maintains comprehensive ECU (Electronic Control Unit) mappings
- Categorizes ECUs into functional groups:
  - Connectivity (Conx)
  - Platform
  - Propulsion
  - SVA (Safety, Vision, and ADAS)
  - SWEP (Software Platform)
  - Tophat
  - ME (Manufacturing Engineering)
- Provides lookup dictionaries for ECU categorization

### Project Mix Analysis (`project_mix.py`)
- Handles project mixing and software version tracking
- Manages vehicle software release mappings
- Supports multiple software versions:
  - REL3.2/3.3
  - REL10
  - 725B variants (TT1, PP, TT2)

## Requirements

- Python 3.x
- pandas
- numpy
- Virtual environment recommended
- Access to Volvo Cars data sources

## Setup

1. Create and activate virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

2. Install required packages:
```powershell
pip install pandas numpy
```

## Usage

### QBay Data Processing
```python
python qbay_powerbi_db.py
```
- Processes fault data from specified directories
- Applies software version mapping
- Generates cleaned dataset for PowerBI

### ECU Analysis
```python
from ECU_list import Solution, ECUs, ECU_list
```
- Import ECU mappings and categories
- Use dictionaries for ECU lookups and categorization

### VIN-Fault Analysis
```python
python vin_to_faults.py
```
- Merges fault and vehicle data
- Creates comprehensive fault reports

## Data Structure

### Input Data
- Fault data CSVs from various sources
- Vehicle information with VINs
- Software version mappings
- ECU categorization data

### Output Data
- Processed fault data for PowerBI
- Combined VIN-fault reports
- ECU analysis results

## Notes

- Configure file paths before running scripts
- Ensure data source access permissions
- Regular updates may be required for new software releases
- Maintain ECU list updates for new components