""" this is a helper utilities and exceptions"""
from __future__ import annotations
import math
from typing import Tuple

def distance_latlog(lat1: float, lon1: float, lat2: float, lon2: float)->float:
    """This function simply calculates the distance in meters between two latitudes/longitudes points. This uses haversine formula which is used to get distance from two sets of longitude and latitude"""
    R = 637100.0 #this is Earth's radius in meters 
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2-lat1)
    delta_lambda = math.radians(lon2-lon1)
    a = math.sin(delta_phi/2.0)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2.0)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def node_latlon(node_data: dict) -> Tuple[float,float]:
    """this will extract the longitude and latitude from a node attribute dictionary(asmnx/networkx format)"""
    lat = node_data.get("y") or node_data.get("lat") #this is simply to extract the longitude/latitude data from dictionary as mentioned in the docstring
    lon = node_data.get("x") or node_data.get("lon")
    return float(lat), float(lon)
