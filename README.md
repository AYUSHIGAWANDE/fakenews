# 🚨 City Disaster Management System

**An offline-first decision support system that optimizes emergency response logistics.**

### About the Project
During urban disasters like floods or earthquakes, rapid decision-making saves lives. This application acts as a digital command center for incident commanders. It processes real-time data to identify safe routes and allocate resources efficiently, eliminating the guesswork from emergency logistics.

### ⚡ Key Features
*   **🚁 Rescue Operations (New):** Auto-switches between **Ambulance** (Road) and **Helicopter** (Air) based on road accessibility.
*   **📦 Supply Chain (New):** Tracks Food & First Aid deficits for every shelter based on population data.
*   **🕹️ Dynamic Situation Room:** Sidebar controls allow commanders to blocking roads in real-time to simulate floods/collapses.
*   **Smart Pathfinding:** Uses **Dijkstra’s Algorithm** to calculate the safeset routes avoiding user-defined danger zones.
*   **Interactive Network Map:** Visualizes the city grid, highlighting safe roads in green and blocked danger zones in red.

### 🛠️ Tech Stack
*   **Python:** Core logic and data processing.
*   **Streamlit:** Interactive web-based user interface.
*   **Graph Theory:** Mathematical foundation for route optimization.
*   **CSV:** Lightweight, offline-capable data storage.

### 🚀 Getting Started
1.  Clone the repository.
2.  Install requirements: `pip install streamlit`
3.  Run the application: `python -m streamlit run app.py`
