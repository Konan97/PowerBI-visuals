# KDP to BIS Converter

A Python application with GUI for converting KDP (Known Data Points) format files to BIS (Basic Information System) format and performing comparisons between them. This tool is designed to help manage and analyze vehicle software configuration data.

## Features

- GUI interface with drag-and-drop file support
- Converts KDP Excel/CSV files to BIS format
- Connects to Snowflake database for data operations
- Handles SW part number ordering and versioning
- Provides standardized output columns for BIS format

## Requirements

- Python 3.x
- PyQt5 (for GUI)
- snowflake-snowpark-python
- pandas
- numpy

## Installation

1. Ensure you have Python 3.x installed
2. Install required dependencies:
```bash
pip install PyQt5 snowflake-snowpark-python pandas numpy
```

## Configuration

The application requires Snowflake database connection parameters. These can be configured in two ways:

1. Using hardcoded defaults (current implementation)
2. Through a `connections.toml` file (commented implementation available)

Default connection parameters include:
- Account: VOLVOCARS-MANUFACTURINGANALYTICS
- Authenticator: externalbrowser
- Role: SELF_SERVICE_USER
- Warehouse: REPORTING
- Database: MANUFACTURING_ENTERPRISE_DATA_PRODUCTS
- Schema: BIS_ITEMS

## Usage

1. Run the GUI application:
```bash
python app_GUI.py
```

2. The application window will open with a drag-and-drop area

3. Drag and drop an Excel file with the following columns:![alt text](image.png)

4. The application will validate the file format and process it accordingly

## Output Format

The converter standardizes output with the following columns:
- Item
- Item Type
- Version
- Model
- No
- Type
- Text
- Base file
- Rel pos
- Length
- Nr.
- Cd
- Condition
- Descr. PML
- Neg
- Base file condition
- Pop Base file
- Starting position
- Length.1
- Valid from
- Valid to
- Plass.week from
- To plass.week
- Shift in
- Shift out

## Notes

- The application uses Snowflake's external browser authentication
- SW part numbers are handled according to a predefined ordering system
- File validation ensures only .xlsx, .xls, or .csv files are processed