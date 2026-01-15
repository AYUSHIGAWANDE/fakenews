import streamlit as st
from logic import (
    load_csv, build_graph, dijkstra, reconstruct_path,
    allocate_shelters, priority_zones,
    generate_network_graph, calculate_flight_time, calculate_supply_needs
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


# Validating static configurations and removing hardcoded logic
# Sidebar for Dynamic Controls
st.sidebar.header("🕹️ Situation Control")
st.sidebar.warning("Report Road Incidents Here")

# Generate unique road keys for the sidebar
all_roads_options = []
for r in roads:
    edge_label = f"{r['from_zone']} ↔ {r['to_zone']}"
    # Use a sorted tuple as the value to ensure direction doesn't matter
    val = tuple(sorted((r['from_zone'], r['to_zone'])))
    all_roads_options.append((edge_label, val))

# Interactive Blocked Road Selection
selected_blocks = []
st.sidebar.write("Select Collapsed/Blocked Roads:")
for label, val in all_roads_options:
    if st.sidebar.checkbox(f"🚫 Block {label}", key=label):
        selected_blocks.append(val)

blocked = set(selected_blocks)

col1, col2, col3 = st.columns(3)
with col1:
    disaster = st.selectbox("Disaster Type", ["Flood", "Earthquake"])
with col2:
    affected = st.multiselect("Affected Zones", zone_ids, default=["Z3", "Z4"])
with col3:
    start_zone = st.selectbox("Command Center Zone (Start)", zone_ids, index=2)

st.subheader("1) Priority Zones")
prio = priority_zones(zones, set(affected))
for r, p, zid, name in prio:
    st.write(f"🔴 {zid} - {name} | Risk: {r} | Population: {p}")

st.subheader("2) Route Planning (Shortest Safe Paths)")
graph = build_graph(roads)
# Pass the dynamic set of blocked edges
dist, parent = dijkstra(graph, start_zone, blocked_edges=blocked)

c1, c2 = st.columns(2)
with c1:
    target = st.selectbox("Select Target Zone", zone_ids, index=3)
with c2:
    st.write("Current Road Status:")
    if blocked:
        for b in blocked:
            st.error(f"⚠️ Road {b[0]}-{b[1]} is BLOCKED")
    else:
        st.success("✅ All Roads Open")

path = reconstruct_path(parent, target)
is_cut_off = False

if path:
    st.success(f"Route: {' → '.join(path)} (Total Distance: {dist[target]:.1f} km)")
else:
    is_cut_off = True
    st.error("⛔ NO ROAD ACCESS! ZONE IS CUT OFF.")

st.markdown("---")
st.markdown("### 🗺️ Live Network Map")
graph_dot = generate_network_graph(roads, blocked, path)
st.graphviz_chart(graph_dot)

st.subheader("3) Rescue Operations (Extraction)")
if is_cut_off:
    st.warning(f"🚨 ZONE {target} IS ISOLATED. DEPLOYING AIR RESCUE.")
    flight_time = calculate_flight_time(None, None) # Placeholder coords
    st.write(f"🚁 Helicopter Dispatch: Command Center → {target}")
    st.write(f"⏱️ Est. Flight Time: {flight_time:.0f} mins (Direct Path)")
else:
    st.success(f"🚑 Ground Ambulance Dispatch: Command Center → {target}")
    st.write(f"⏱️ Est. Drive Time: {dist[target] * 2:.0f} mins (at 30km/h)")

st.subheader("4) Supply Operations (Food & Meds)")
# Calculate needs for affected zones
st.write("Daily Supply Requirements for Affected Zones:")
for z in zones:
    if z["zone_id"] in affected:
        pop = int(z["population"])
        food, meds = calculate_supply_needs(pop)
        
        # Check against fake stock for demo
        stock_food = 500 # Simulated stock
        deficit = food - stock_food
        
        expander = st.expander(f"📦 Needs for {z['zone_name']} (Pop: {pop})", expanded=True)
        with expander:
            c1, c2 = st.columns(2)
            c1.metric("🍚 Food Packets", f"{food}", delta=f"-{deficit}" if deficit > 0 else "OK", delta_color="inverse")
            c2.metric("💊 First Aid Kits", f"{meds}", "Urgent" if meds > 50 else "Standard")
            
            if deficit > 0:
                st.error(f"CRITICAL SHORTAGE: Need {deficit} more packets!")
                st.button(f"🚀 Dispatch Supply Drop to {z['zone_id']}", key=f"btn_{z['zone_id']}")

st.subheader("5) Shelter Allocation")
alloc = allocate_shelters(zones, shelters, set(affected))
for zid, sid, people, szone in alloc:
    if sid == "NO_SPACE":
        st.error(f"{zid} ({zone_names[zid]}): {people} people have no shelter space!")
    else:
        st.info(f"{zid} → {sid} (Shelter Zone: {szone}) : {people} people")

st.subheader("6) Resource Tracker")
for r in resources:
    st.write(f"🚑 {r['resource_type']} | Zone: {r['zone_id']} | Qty: {r['quantity']}")
