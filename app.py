import streamlit as st
from logic import (
    load_csv, allocate_shelters, calculate_supply_needs,
    calculate_risk_score, detect_gaps, get_rescue_priority_order, get_zone_status
)

st.set_page_config(page_title="Commander Dashboard", layout="wide", initial_sidebar_state="expanded")

# ========== LOAD DATA ==========
zones = load_csv("data/zones.csv")
shelters = load_csv("data/shelters.csv")
resources = load_csv("data/resources.csv")

zone_ids = [z["zone_id"] for z in zones]

# ========== SESSION STATE (Live Tracking) ==========
if "rescued" not in st.session_state:
    st.session_state.rescued = {z["zone_id"]: 0 for z in zones}
if "approved_missions" not in st.session_state:
    st.session_state.approved_missions = []

# ========== SIDEBAR: MISSION CONTROL ==========
st.sidebar.image("https://img.icons8.com/color/96/emergency.png", width=80)
st.sidebar.title("🕹️ MISSION CONTROL")
disaster = st.sidebar.selectbox("⚠️ Active Disaster", ["Flood", "Earthquake"])
affected = st.sidebar.multiselect("🔥 Affected Zones", zone_ids, default=["Z3", "Z4"])
severity_level = st.sidebar.select_slider("📊 Severity Level", ["Low", "Medium", "High", "Critical"], value="High")

st.sidebar.divider()
st.sidebar.caption("System monitors highest population & disaster severity.")

# ========== HEADER ==========
st.title("🎖️ COMMANDER-LEVEL DISASTER MANAGEMENT")
st.caption("Real-Time • Risk-Based • Population-Priority")

# ========== 1. QUICK ALERTS PANEL ==========
st.markdown("### 🔔 Quick Alerts")
col_a1, col_a2, col_a3, col_a4 = st.columns(4)
col_a1.metric("Disaster Type", disaster, "ACTIVE")
col_a2.metric("Severity", severity_level, "⚠️" if severity_level in ["High", "Critical"] else "")
col_a3.metric("Zones Affected", len(affected), f"of {len(zones)}")
total_pop = sum(int(z["population"]) for z in zones if z["zone_id"] in affected)
col_a4.metric("Population at Risk", f"{total_pop:,}", "Immediate Action")

st.divider()

# ========== 2. CITY MAP VIEW (5 Regions) ==========
st.markdown("### 🗺️ City Zone Status")
st.caption("East | West | North | South | Central")

# Create 5 columns for the 5 regions
cols = st.columns(5)
for i, zone in enumerate(zones):
    with cols[i % 5]:
        status = get_zone_status(zone, set(affected))
        risk = calculate_risk_score(zone)
        
        # Color coding
        if status == "Critical":
            bg = "🔴"
        elif status == "Affected":
            bg = "🟠"
        else:
            bg = "🟢"
        
        remaining = int(zone["population"]) - st.session_state.rescued.get(zone["zone_id"], 0)
        
        st.markdown(f"""
        **{bg} {zone["region"]}**
        - Zone: {zone["zone_id"]}
        - Pop: {remaining:,}
        - Risk: {risk}
        - Status: **{status}**
        """)

st.divider()

# ========== 3. RISK FACTOR CALCULATION ==========
st.markdown("### 📊 Risk Factor Analysis")
st.caption("Risk = Population Score + Severity Score + Vulnerability Score")

# Sort zones by risk (highest first)
risk_data = []
for z in zones:
    if z["zone_id"] in affected:
        risk = calculate_risk_score(z)
        risk_data.append((risk, z))
risk_data.sort(key=lambda x: -x[0])

for risk, z in risk_data:
    st.progress(min(risk / 20, 1.0), text=f"**{z['zone_name']}** — Risk Score: {risk}/20")

st.divider()

# ========== 4. DISASTER-SPECIFIC RESCUE OPERATIONS ==========
st.markdown(f"### 🚨 {disaster.upper()} RESCUE OPERATIONS")
priority_order = get_rescue_priority_order(disaster)
st.caption(f"Priority Order: {' → '.join(priority_order)}")

# Show rescue cards for each affected zone (sorted by risk)
for risk, z in risk_data:
    zid = z["zone_id"]
    remaining = int(z["population"]) - st.session_state.rescued.get(zid, 0)
    
    with st.expander(f"📍 **{z['zone_name']}** | Risk: {risk} | Stranded: {remaining:,}", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            if disaster == "Earthquake":
                st.write("🧱 Deploy Debris Rescue Team")
                st.write("🚑 Dispatch Ambulances")
            else:
                st.write("🛟 Deploy Water Rescue (Boats)")
                st.write("🚁 Dispatch Helicopter")
        
        with col2:
            st.write("🏕️ Assign to Shelter")
            st.write("📦 Food & First Aid")
        
        with col3:
            if st.button(f"✅ APPROVE RESCUE", key=f"approve_{zid}"):
                # Simulate rescuing 500 people per click
                st.session_state.rescued[zid] = st.session_state.rescued.get(zid, 0) + 500
                st.session_state.approved_missions.append({
                    "zone": zid,
                    "disaster": disaster,
                    "status": "In Progress"
                })
                st.rerun()

st.divider()

# ========== 5. RESOURCE ALLOCATION & GAP DETECTION ==========
st.markdown("### ⚠️ Resource Gap Analysis")
st.caption("Required > Available = GAP")

gaps = detect_gaps(zones, resources, set(affected), disaster)

if gaps:
    for g in gaps:
        st.error(f"🚨 **{g['resource_type']}** — Needed: {g['required']} | Available: {g['available']} | **GAP: {g['gap']}**")
else:
    st.success("✅ All resource requirements met!")

st.divider()

# ========== 6. SUPPLY LOGISTICS ==========
st.markdown("### 📦 Supply Requirements")

for z in zones:
    if z["zone_id"] in affected:
        pop = int(z["population"])
        food, meds = calculate_supply_needs(pop)
        
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.write(f"**{z['zone_name']}**")
        col_s2.metric("Food Packets", f"{food:,}")
        col_s3.metric("First Aid Kits", f"{meds:,}")

st.divider()

# ========== 7. SHELTER ALLOCATION ==========
st.markdown("### 🏠 Shelter Allocation")

alloc = allocate_shelters(zones, shelters, set(affected))
for zid, sid, people, szone in alloc:
    if sid == "NO_SPACE":
        st.error(f"❌ **{zid}**: {people:,} people — NO SHELTER AVAILABLE")
    else:
        st.write(f"✅ **{zid}** → {sid} ({szone}) — {people:,} people")

st.divider()

# ========== 8. COMMANDER ACTION LOG ==========
st.markdown("### 📋 Approved Missions")

if st.session_state.approved_missions:
    for m in st.session_state.approved_missions[-5:]:  # Show last 5
        st.write(f"✅ Zone **{m['zone']}** — {m['disaster']} Rescue — {m['status']}")
else:
    st.info("No missions approved yet. Use the APPROVE button above.")

st.divider()

# ========== 9. POST-RESCUE REPORT ==========
st.markdown("### 📈 Response Summary")

total_rescued = sum(st.session_state.rescued.values())
col_r1, col_r2, col_r3 = st.columns(3)
col_r1.metric("People Rescued", f"{total_rescued:,}")
col_r2.metric("Missions Approved", len(st.session_state.approved_missions))
col_r3.metric("Zones Stabilized", sum(1 for z in zones if get_zone_status(z, set(affected)) == "Safe"))

# ========== FOOTER ==========
st.divider()
st.caption("💡 _This system supports disaster commanders by calculating population-based risk, optimizing distance-based resource allocation, and coordinating earthquake and flood rescue operations in real time._")
