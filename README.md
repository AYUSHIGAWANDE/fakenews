# 🎖️ Commander-Level Disaster Management System

**Real-Time • Risk-Based • Population-Priority**

> _"This system supports disaster commanders by calculating population-based risk, optimizing distance-based resource allocation, and coordinating earthquake and flood rescue operations in real time."_

---

## ⚡ Key Features

| Feature | Description |
|---------|-------------|
| 🗺️ **City Zone Map** | 5-region view (East/West/North/South/Central) with live status |
| 📊 **Risk Engine** | Formula: `Risk = Population + Severity + Vulnerability` |
| 🚨 **Disaster Logic** | Earthquake (Debris → Ambulance) vs Flood (Boats → Shelter) |
| ⚠️ **Gap Detection** | Alerts when `Required > Available` resources |
| 📦 **Supply Calculator** | 2 food packets/person, 1 first aid kit/10 people |
| ✅ **Commander Actions** | Approve missions, track rescued population |

---

## 🛠️ Tech Stack
- **Python** + **Streamlit**
- CSV-based offline data (no database required)

---

## 🚀 Run the App
```bash
pip install -r requirements.txt
python -m streamlit run app.py
```
