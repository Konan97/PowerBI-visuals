# Python Visualization Tools

A collection of Python scripts for generating visualizations and analytics for Volvo Cars manufacturing data, including heat maps, fault area analysis, and DPV (Digital Process Verification) monitoring.

## Scripts Overview

### Heat Maps
- `EX90_HeatMap.py` - Generates heat map visualizations for EX90 model
- `P519_HeatMap.py` - Creates heat map visualizations for P519 model
- `S60_HeatMap.py` - Produces heat map visualizations for S60 model

### Fault Analysis
- `EX90_FaultAreaCount.py` - Analyzes and counts fault areas for EX90 model
- `P519_FaultAreaCount.py` - Analyzes and counts fault areas for P519 model

### Process Monitoring
- `DPV_screen.py` - Digital Process Verification monitoring dashboard
  - Displays DPV scores with color-coded indicators
  - Compares scores against targets
  - Real-time updates based on latest timestamps

### Shop Analytics
- `A_shop_tables.py` - Generates analytical tables for A-shop data
  - ATACQ item analysis
  - Workstation linking statistics
  - Model-specific counts (Polestar 3 and EX90)
  - DPV calculations per model

## Requirements

- Python 3.x
- pandas
- matplotlib
- seaborn
- urllib
- io
- base64

## Features

- Real-time data visualization
- Automated DPV score tracking
- Color-coded performance indicators
- Multiple vehicle model support
- Customizable visualization parameters
- Background image support for heat maps

## Usage

Each script can be run independently based on the specific visualization needs:

1. For Heat Maps:
```python
python [model]_HeatMap.py  # where model is EX90, P519, or S60
```

2. For Fault Analysis:
```python
python [model]_FaultAreaCount.py  # where model is EX90 or P519
```

3. For DPV Monitoring:
```python
python DPV_screen.py
```

4. For Shop Analytics:
```python
python A_shop_tables.py
```

## Data Processing

- Automated data cleaning and preprocessing
- Handling of missing values
- Duplicate entry management
- Timestamp-based filtering
- Model-specific data segregation

## Output Formats

- Heat maps with optional background images
- Statistical tables with performance metrics
- Color-coded DPV score displays
- Fault area distribution visualizations

## Notes

- Scripts are configured for Volvo Cars manufacturing environment
- Data source connections need to be configured before use
- Some visualizations support interactive features
- Regular updates may be required for new model support