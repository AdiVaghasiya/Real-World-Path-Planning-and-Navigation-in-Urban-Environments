"""


maploader.py
utility functions for downloading, caching, and processing openstreetmap road network graphs
uses osmnx to fetch data and networkx for graph operations


"""


from __future__ import annotations
import os
import pickle 
from typing import Any
import time

import networkx as nx
import osmnx as ox
from osmnx import distance, geocode
from utils import MappingError, GraphNavigationError

CACHE_DIR = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_graph_for_place(place_name: str, network_type: str = "drive", use_cache: bool = True) -> nx.MultiDiGraph:
    """return a networkx graph for a place. Caches to disk as pickle.


    args:
    place_name: human readable place, e.g. "Hoboken, New Jersey, USA"
    network_type: osmnx network type (drive, walk, bike etc.)
    use_cache: if True, will read/write from local cache


    returns:
    networkx MultiDiGraph
    """
    safe_name = place_name.replace(",", "").replace(" ", "_")
    cache_path = os.path.join(CACHE_DIR, f"{safe_name}_{network_type}.pickle")


    if use_cache and os.path.exists(cache_path):
        with open(cache_path, "rb") as fh:
            graph = pickle.load(fh)
        return graph


    #download from OSM
    t0 = time.time()
    graph = ox.graph_from_place(place_name, network_type=network_type)
    t1 = time.time()
    print(f"Downloaded graph for {place_name} in {t1-t0:.2f}s — nodes: {len(graph.nodes)} edges: {len(graph.edges)}")


    if use_cache:
        with open(cache_path, "wb") as fh:
            pickle.dump(graph, fh)
    return graph

def geocode_address(address: str):
    #convert a human readable address to (latitude, longitute) using built in osmnx geocode.
    try:
        lat, lon = geocode(address)
        return lat, lon
    except Exception as e:
        raise MappingError(f"Geocoding failed for address '{address}': {e}") from e


def nearest_node(graph: nx.MultiDiGraph, lat: float, lon: float) -> int:
    #eturn the nearest node id in the graph to the given lat/lon
    return ox.distance.nearest_nodes(graph, X=lon, Y=lat)

def get_nearest_node(graph: nx.MultiDiGraph, lat: float, lon: float):
    #find the nearest node in the road graph to the given coordinates.
    try:
        node_id = distance.nearest_nodes(graph, X=lon, Y=lat)
        return node_id
    except Exception as e:
        raise GraphNavigationError("Unable to find nearest node in graph.") from e



def graph_to_simple_weighted(graph: nx.MultiDiGraph) -> nx.DiGraph:
    #convert osmnx MultiDiGraph to a simple DiGraph with 'length' weights, this keeps minimal info needed for A* and visualization.
    
    G = nx.DiGraph()
    for u, v, k, data in graph.edges(keys=True, data=True):
        length = data.get("length")
        if length is None:
            #fallback: estimate from geometry if present
            length = data.get("distance") or 0.0
        if G.has_edge(u, v):
            #keep smallest
            if length < G[u][v]["length"]:
                G[u][v]["length"] = length
        else:
            G.add_edge(u, v, length=length)
    #copy node attributes (lat/lon)
    for n, data in graph.nodes(data=True):
        G.add_node(n, **data)
    return G