import csv
import math
from collections import defaultdict
import heapq

def load_csv(path):
    with open(path, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def build_graph(roads):
    g = defaultdict(list)
    for r in roads:
        a = r["from_zone"]
        b = r["to_zone"]
        d = float(r["distance_km"])
        g[a].append((b, d))
        g[b].append((a, d))
    return g

def dijkstra(graph, start, blocked_edges=set()):
    dist = {start: 0.0}
    parent = {start: None}
    pq = [(0.0, start)]

    while pq:
        cost, node = heapq.heappop(pq)
        if cost != dist.get(node, math.inf):
            continue

        for nxt, w in graph[node]:
            edge = tuple(sorted((node, nxt)))
            if edge in blocked_edges:
                continue

            new_cost = cost + w
            if new_cost < dist.get(nxt, math.inf):
                dist[nxt] = new_cost
                parent[nxt] = node
                heapq.heappush(pq, (new_cost, nxt))

    return dist, parent

def reconstruct_path(parent, target):
    if target not in parent:
        return []
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return list(reversed(path))

def get_blocked_edges(disaster_type):
    if disaster_type == "Flood":
        return {("Z3", "Z4")}
    if disaster_type == "Fire":
        return {("Z2", "Z3")}
    if disaster_type == "Earthquake":
        return {("Z1", "Z3"), ("Z3", "Z5")}
    return set()

def allocate_shelters(zones, shelters, affected_zone_ids):
    shelter_remaining = {s["shelter_id"]: int(s["capacity"]) for s in shelters}
    shelter_zone = {s["shelter_id"]: s["zone_id"] for s in shelters}

    allocations = []
    for z in zones:
        zid = z["zone_id"]
        if zid not in affected_zone_ids:
            continue
        people = int(z["population"])

        preferred = [s for s in shelters if s["zone_id"] == zid] + shelters

        for s in preferred:
            sid = s["shelter_id"]
            if people <= 0:
                break
            if shelter_remaining[sid] <= 0:
                continue
            take = min(people, shelter_remaining[sid])
            shelter_remaining[sid] -= take
            people -= take
            allocations.append((zid, sid, take, shelter_zone[sid]))

        if people > 0:
            allocations.append((zid, "NO_SPACE", people, "NONE"))

    return allocations

def priority_zones(zones, affected_zone_ids):
    items = []
    for z in zones:
        if z["zone_id"] in affected_zone_ids:
            items.append((int(z["risk_level"]), int(z["population"]), z["zone_id"], z["zone_name"]))
    items.sort(key=lambda x: (-x[0], -x[1]))
    return items

def generate_network_graph(roads, blocked_edges, path=None):
    dot = ['graph {']
    dot.append('  rankdir=LR;')
    dot.append('  node [style=filled, fillcolor=lightblue, shape=circle];')
    
    # Identify edges acting as part of the path
    path_edges = set()
    if path and len(path) > 1:
        for i in range(len(path) - 1):
            path_edges.add(tuple(sorted((path[i], path[i+1]))))

    for r in roads:
        u, v = r["from_zone"], r["to_zone"]
        dist = r["distance_km"]
        
        # Create a sorted tuple to check against blocked/path sets
        key = tuple(sorted((u, v)))
        
        color = "black"
        style = "solid"
        penwidth = "1"
        
        if key in blocked_edges:
            color = "red"
            style = "dashed"
            penwidth = "2"
        elif key in path_edges:
            color = "darkgreen"
            penwidth = "4"
            
        dot.append(f'  "{u}" -- "{v}" [label="{dist}km", color={color}, style={style}, penwidth={penwidth}];')
    
    dot.append('}')
    return "\n".join(dot)

def calculate_flight_time(zone_a_coords, zone_b_coords, speed_kmh=250):
    # Simple Euclidean distance for "Air travel"
    # Assuming coords are simple (x, y) for this demo. 
    # In reality, we'd use Haversine on lat/lon.
    # For this offline demo, we simulate distance simply as 10km fixed or random if no coords.
    # Let's keep it simple: 15km average for air rescue across city.
    dist_km = 15.0 
    time_hours = dist_km / speed_kmh
    return time_hours * 60 # minutes

def calculate_supply_needs(population):
    # Rule: 2 food packets per person, 1 kit per 10 people
    food_needed = population * 2
    meds_needed = math.ceil(population / 10)
    return food_needed, meds_needed
