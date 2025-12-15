#planner
"""In this program I will make a base class named planner and subclass pathplanner with A* implementation."""

from __future__ import annotations
import heapq
import time
from typing import Dict, List, Tuple, Optional
import networkx as nx
from utils import distance_latlog, node_latlon

class Planner:
    """Base planner class that stores a directed graph. Other planners (e.g.,A*) can extend this class."""
    def __init__(self, graph: nx.DiGraph):
        #stores the graph that will be used for planning
        self.graph = graph

    def __str__(self) -> str:
        #helful string representation for debugging and logging
        return f"planner(graph_nodes = {self.graph.number_of_nodes()}, graph_edges = {self.graph.number_of_edges()})"

class PathPlanner(Planner):
    """Planner that implements A* search to find the shortest path between two nodes in a directed graph."""
    def __init__(self, graph: nx.DiGraph):
        super().__init__(graph)
    
    def heuristic(self, node_a: int, node_b: int)->float:
        """Heuristic function for A*. Estimates the remaining distance between two nodes using thier geographic coordinates (using the haversine formula)."""
        a = self.graph.nodes[node_a] #Extract latitude/longitude form node attributes
        b = self.graph.nodes[node_b]
        lat1, lon1 = node_latlon(a)
        lat2, lon2 = node_latlon(b)
        return distance_latlog(lat1,lon1,lat2,lon2)
    
    def reconstruct_path(self,came_from:Dict[int,int],current:int):
        """Reconstruct the path from the start node to the current node by following parent pointers stored in came_form."""
        path= [current]
        while current in came_from: #walk backwards from the goal to the start
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def plan(self,start:int,goal:int)->Tuple[List[int],float,float]:
        """A* search from  start node id to goal node id. This is an important function with A* implementation."""
        t0= time.time() #start timer for performance measurement
        open_set = [] #heap of(f_score, node)
        heapq.heappush(open_set,(0.0,start))

        came_from: Dict[int,int] = {} #stores best parent for each visited node
        gscore: Dict[int,float] = {start:0.0} #cost from start to each node

        fscore: Dict[int,float] = {start: self.heuristic(start, goal)} #estimated total cost. In A* function resembles f(n)=g(n)+h(n)
        visited = set()#keeps track of the nodes already expanded

        while open_set:
            current_f, current = heapq.heappop(open_set)#always expand the node with the lowest estimated tot cost
            if current == goal:#stop if you reach the goal and calculate the cost
                path = self.reconstruct_path(came_from,current)
                total = gscore[current]
                return path,total,time.time()-t0
            
            if current in visited:#continue if the node is already visited
                continue
            visited.add(current)

            for nbr in self.graph.succesors(current):#if the node is not visited then default here and explore all outgoing edges from the current node
                edge_data = self.graph.get_edge_data(current,nbr)
                #take length attribute(if multi-edge, edge_data might be dict of keys)
                length = None
                if isinstance(edge_data,dict) and "length" in edge_data:
                    length = edge_data["length"]
                else:
                    #if it's MultiEdge-like, pick a minimal length
                    try:
                        length = min((d.get("length", float("inf")) for d in edge_data.values()))
                    except Exception:
                        length = 0.0
                
                tentative_g = gscore[current] + float(length)#compute tentative cost to neighbor current node
                if tentative_g < gscore.get(nbr, float("inf")):#if a better path to the neighbor is found, then update scores
                    came_from[nbr] = current
                    gscore[nbr] = tentative_g
                    f = tentative_g + self.heuristic(nbr,goal)
                    fscore[nbr] = f
                    heapq.heappush(open_set,(f,nbr))
        raise Exception(f"No path found from {start} to {goal}") #no path exists between start and goal
                
            