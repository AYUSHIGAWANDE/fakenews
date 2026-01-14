import streamlit as st
from logic import (
    load_csv, build_graph, dijkstra, reconstruct_path,
    get_blocked_edges, allocate_shelters, priority_zones,
    generate_network_graph
)

st.set_page_config(page_title="City Disaster Management (Offline)", layout="wide")

st.title("🚨 CITY-WIDE DISASTER MANAGEMENT SYSTEM")
st.caption("Offline • Route Planning • Shelter Allocation • Resource Tracking")

zones = load_csv("data/zones.csv")
shelters = load_csv("data/shelters.csv")
roads = load_csv("data/roads.csv")
resources = load_csv("data/resources.csv")

zone_ids = [z["zone_id"] for z in zones]
zone_names = {z["zone_id"]: z["zone_name"] for z in zones}

col1, col2, col3 = st.columns(3)
with col1:
    disaster = st.selectbox("Disaster Type", ["Flood", "Fire", "Earthquake"])
with col2:
    affected = st.multiselect("Affected Zones", zone_ids, default=["Z3", "Z4"])
with col3:
    start_zone = st.selectbox("Command Center Zone (Start)", zone_ids, index=2)

blocked = get_blocked_edges(disaster)

st.subheader("1) Priority Zones")
prio = priority_zones(zones, set(affected))
for r, p, zid, name in prio:
    st.write(f"🔴 {zid} - {name} | Risk: {r} | Population: {p}")

st.subheader("2) Route Planning (Shortest Safe Paths)")
graph = build_graph(roads)
dist, parent = dijkstra(graph, start_zone, blocked_edges=set(tuple(sorted(e)) for e in blocked))

c1, c2 = st.columns(2)
with c1:
    target = st.selectbox("Select Target Zone", zone_ids, index=3)
with c2:
    st.write("Blocked Roads (Rule-based):")
    st.write([f"{a}-{b}" for a, b in blocked] if blocked else "None")

path = reconstruct_path(parent, target)
if path:
    st.success(f"Route: {' → '.join(path)} (Total Distance: {dist[target]:.1f} km)")
else:
    st.error("No safe route found due to blocked roads.")

st.markdown("---")
st.markdown("### 🗺️ Live Network Map")
blocked_set = set(tuple(sorted(e)) for e in blocked)
graph_dot = generate_network_graph(roads, blocked_set, path)
st.graphviz_chart(graph_dot)

st.subheader("3) Shelter Allocation")
alloc = allocate_shelters(zones, shelters, set(affected))
for zid, sid, people, szone in alloc:
    if sid == "NO_SPACE":
        st.error(f"{zid} ({zone_names[zid]}): {people} people have no shelter space!")
    else:
        st.info(f"{zid} → {sid} (Shelter Zone: {szone}) : {people} people")

st.subheader("4) Resource Tracker")
for r in resources:
    st.write(f"🚑 {r['resource_type']} | Zone: {r['zone_id']} | Qty: {r['quantity']}")
