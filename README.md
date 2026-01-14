# 🚨 City Disaster Management System

**An offline-first decision support system that optimizes emergency response logistics.**

### About the Project
During urban disasters like floods or earthquakes, rapid decision-making saves lives. This application acts as a digital command center for incident commanders. It processes real-time data to identify safe routes and allocate resources efficiently, eliminating the guesswork from emergency logistics.

### ⚡ Key Features
*   **Smart Pathfinding:** Uses **Dijkstra’s Algorithm** to calculate the safest, shortest routes for emergency vehicles, automatically rerouting around blocked or hazardous zones.
*   **Interactive Network Map:** Visualizes the entire city grid, highlighting open roads in green and danger zones in red for instant situational awareness.
*   **Shelter Allocation:** Instantly matches displaced populations to the nearest available shelters, tracking capacity to prevent overcrowding.
*   **Resource Tracking:** Monitors the real-time status and location of ambulances, fire trucks, and personnel.

### 🛠️ Tech Stack
*   **Python:** Core logic and data processing.
*   **Streamlit:** Interactive web-based user interface.
*   **Graph Theory:** Mathematical foundation for route optimization.
*   **CSV:** Lightweight, offline-capable data storage.

### 🚀 Getting Started
1.  Clone the repository.
2.  Install requirements: `pip install streamlit`
3.  Run the application: `python -m streamlit run app.py`
