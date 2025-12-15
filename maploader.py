"""


maploader.py
utility functions for downloading, caching, and processing openstreetmap road network graphs
uses osmnx to fetch data and networkx for graph operations


"""




from __future__ import annotations
import os
import pickle
import time
from typing import Any


import networkx as nx
import osmnx as ox


#cache directory setup - stores downloaded osm graphs locally to avoid repeated api calls
#structure below is expected by the main routing module
CACHE_DIR = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def get_graph_for_place(place_name: str, network_type: str = "drive", use_cache: bool = True) -> nx.MultiDiGraph:
    """Return a networkx graph for a place. Caches to disk as pickle.




    Args:
    place_name: human readable place, e.g. "Hoboken, New Jersey, USA"
    network_type: osmnx network type (drive, walk, bike etc.)
    use_cache: if True, will read/write from local cache




    Returns:
    networkx MultiDiGraphee
    """
   
    safe_name = place_name.replace(",", "").replace(" ", "_")
    cache_path = os.path.join(CACHE_DIR, f"{safe_name}_{network_type}.pickle")




    #check if cached version exists
    if use_cache and os.path.exists(cache_path):
        with open(cache_path, "rb") as fh:
            graph = pickle.load(fh)
        return graph




    #todo: add error handling for failed downloads
    #download from OSM
    t0 = time.time()
    graph = ox.graph_from_place(place_name, network_type=network_type)
    t1 = time.time()
    print(f"Downloaded graph for {place_name} in {t1-t0:.2f}s — nodes: {len(graph.nodes)} edges: {len(graph.edges)}")




    #save to cache
    if use_cache:
        with open(cache_path, "wb") as fh:
            pickle.dump(graph, fh)
    return graph








def nearest_node(graph: nx.MultiDiGraph, lat: float, lon: float) -> int:
    """Return the nearest node id in the graph to the given lat/lon."""
    #osmnx expects X=lon, Y=lat (not lat/lon order)
    return ox.distance.nearest_nodes(graph, X=lon, Y=lat)




#to do - add graph_to_simple_weighted function for a* pathfinding



