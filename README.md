# Real-World Path Planning (A* + OSM)


## Overview
Starter project to compute shortest routes between two addresses using OpenStreetMap data and a custom A* implementation.


## Requirements
- Python 3.12 or 3.13
- osmnx
- networkx
- matplotlib
- folium
- pytest

## Setting up virtual environment
- Windows and Linux both have different commands to activate venve
- In windows if the activation script does not work it may require extra permission: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
- Run the below commands in the order provided
- After succefully completing the project exit the venv using "deactivate" command

```bash
python -m venv myenv
./myenv/bin/activate  [Linux]
.\myenv\Scripts\Activate.ps1 [windows]
pip install osmnx networkx matplotlib scikit-learn folium pytest jupyter
jupyter notebook
