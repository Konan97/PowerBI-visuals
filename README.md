# Volvo_SW — Python tools and visualizations

Collection of Python scripts and small GUI tools used for manufacturing analytics, visualizations and fault-data preparation. Developed and maintained by Yuting Sun. This README summarizes the repository layout, common requirements and how to run each toolset. For more details see the README in each subfolder.

## Repository layout

- `KDP_BIS/` — KDP to BIS conversion GUI and comparison tools. See `KDP_BIS/README.md`.
- `Python_visuals/` — Heatmaps, DPV screens and shop analytics scripts. See `Python_visuals/README.md`.
- `Fault_data_prep/` — Fault data ETL and preparation scripts for PowerBI (ECU lists, QBay processing, VIN correlation). See `Fault_data_prep/README.md`.
- `Vehicle_tracking/` — Intranet vehicle tracking GUI with Snowflake integration. See `Vehicle_tracking/README.md`.
- Top-level scripts: a set of convenience and analysis scripts in the repository root (examples below).

Files at repository root include (not exhaustive):

- `A_shop_tables.py` — Shop analytics tables
- `bcCompare.py` — Binary/code comparison helpers
- `carconfig.txt`, `BC.txt` — configuration/text resources
- `DPV_screen.py`, `EX90_*`, `P519_*`, `S60_HeatMap.py` — visual scripts (also duplicated under `Python_visuals/`)
- `KDP_BIS.py`, `app_GUI.py` — main KDP to BIS converter (under `KDP_BIS/` folder)
- `intranet_monitor_snowflake.py` — vehicle tracking GUI (under `Vehicle_tracking/` folder)

## Quickstart — common requirements

- Python 3.8+ (3.11 tested in places)
- Recommended: create a virtual environment

Install common dependencies (powershell example):

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# or install individual packages
pip install pandas numpy matplotlib seaborn PyQt5 snowflake-snowpark-python
```

Note: Not every script requires all packages. See the subfolder README for per-component requirements.

## Running the tools

- KDP to BIS converter (GUI):

```powershell
cd KDP_BIS
python app_GUI.py
```

- Vehicle tracking (GUI):

```powershell
cd Vehicle_tracking
python intranet_monitor_snowflake.py
```

- Fault data preparation (QBay -> PowerBI):

```powershell
cd Fault_data_prep
python qbay_powerbi_db.py
```

- Visual scripts (examples):

```powershell
cd Python_visuals
python EX90_HeatMap.py
python DPV_screen.py
```

## Configuration and credentials

- Several tools connect to Volvo Cars Snowflake. They use `externalbrowser` authenticator by default and expect valid Snowflake user credentials. Connection parameters are defined in each module; some scripts include an optional `connections.toml` (commented) to override defaults.
- For scripts that read local CSV/Excel files, set absolute or workspace-relative paths before running.

## Contributing & Maintenance notes

- Keep sensitive credentials out of the repo. Use environment variables or a local `connections.toml` that is gitignored.
- Update the ECU lists and project mix files in `Fault_data_prep` when new releases or ECUs are introduced.
- Tests: these are small utility scripts; adding lightweight unit tests for data-processing functions is encouraged.

## Where to find more information

Each subfolder contains a README with component-specific instructions and examples:

- `KDP_BIS/README.md`
- `Python_visuals/README.md`
- `Fault_data_prep/README.md`
- `Vehicle_tracking/README.md`

