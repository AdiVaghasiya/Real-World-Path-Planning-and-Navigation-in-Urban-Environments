## Real-World-Path-Planning-and-Navigation-in-Urban-Environments
This project aims to solve a real-world engineering problem: finding the shortest and most efficient path between two locations in a city using real map data. Path planning and routing are fundamental challenges in robotics, transportation, logistics, and urban planning. Systems like Google Maps rely on solving these types of problems at scale.

## Team Members:
Aditya Vaghasiya
avaghasi1@stevens.edu

Antony Langley
alangley@stevens.edu


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
