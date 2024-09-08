# TransitSafety Dashboard

## Overview

The **TransitSafety Dashboard** is a data visualization project designed to analyze and display bus driving data using a dashboard. The project utilizes **Plotly** and **Dash** libraries to create an interactive web-based dashboard that presents key insights into driver behavior and events that occur during bus routes. This tool helps monitor the performance of drivers based on safety metrics and visualize various patterns from the data collected.

## Features

- **Interactive Dashboard**: Allows users to explore data interactively through sliders, dropdowns, and checklists.
- **Plotly Graphs**: Provides visualizations such as bar graphs, scatter plots, line graphs, pie charts (donuts), and Mapbox maps to represent the analyzed data.
- **Safety Metrics**: Includes a calculation of a **Safety Score** for drivers based on key parameters such as event types (harsh braking, acceleration) and speed.
- **Mapbox Integration**: Displays routes and locations traversed by vehicles on an interactive map.
- **Driver Event Analysis**: Compares the events across different drivers and visualizes them using donut charts for comprehensive event analysis.

## Project Structure

```plaintext
├── assets
│   ├── sit.png            # Logo for the dashboard
│   ├── style.css          # Custom CSS styles for the dashboard
├── data
│   ├── data.ipynb         # Jupyter notebook for data processing and analysis
│   ├── juneroute.csv      # Raw data for routes in June
│   ├── data_main.csv      # Main dataset with driving events
│   ├── mini_container.csv # Container with summarized data for visualization
│   ├── avg_speed.csv      # Average speed data per day
│   ├── time_speed.csv     # Speed data based on time
│   ├── summary.csv        # Summary statistics of the data
├── .env                   # Environment file containing sensitive keys (e.g., MAPBOX_TOKEN)
├── app.py                 # Main Python file containing the dashboard application
├── README.md              # This file (project documentation)
```

## Key Dependencies

- **Dash**: For building the web-based dashboard interface.
- **Plotly**: For creating rich and interactive visualizations.
- **Pandas**: For data manipulation and processing.
- **dotenv**: To manage environment variables, such as API tokens (e.g., Mapbox).
- **waitress**: Production deployment

## How to Run

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd TransitSafety_Dashboard
   ```

2. **Install Dependencies**:
   Create a virtual environment and install the required Python packages:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your **MAPBOX_TOKEN**:

   ```bash
   MAPBOX_TOKEN=<Your Mapbox Token>
   ```

4. **Run the App**:
   Start the Dash application:
   ```bash
   python app.py
   ```
   The app will be accessible at `http://localhost:8050`.

## Dashboard Features

1. **Slider and Cards**:

   - The dashboard contains a slider to select a specific day in June. The cards display:
     - Day number
     - Number of events
     - Highest speed
     - Lowest speed

2. **Summary Table**:

   - A summary of key statistics is displayed in a table format with conditional formatting for better readability.

3. **Visualizations**:
   - **Bar Graph**: Shows the number of events per day.
   - **Map**: Interactive map showing the vehicle routes and locations.
   - **Line Graph**: Displays the average speed of a selected driver and compares it with the overall average speed.
   - **Donut Charts**: Visualize the distribution of event types for all drivers and a selected driver.
   - **Scatter Plot**: Displays the average speed against time, with shaded areas to differentiate between peak and non-peak hours.

## Data Sources

- The data in this project represents events such as harsh braking, acceleration, vehicle speeds, and coordinates recorded during bus operations.
- Data files include detailed information on **driver performance**, **bus routes**, and **events** for the month of June.

## Notes

- **MAPBOX_TOKEN**: Make sure to replace the placeholder token with your own valid Mapbox access token in the `.env` file.
- The project includes several callbacks to connect visual components and update them dynamically as the user interacts with the dashboard.
- Any version of app.run_server() should produce this warning, Dash is using a library called Flask 16 and calling the .run() method on the Flask app which by default uses the werkzeug development server 60 which is similar to Python’s http.server 14. While the a great library for quickly running web-server in development it is not tested for security or performance. So what do you use instead? Popular choices are gunicorn 261 and WSGI or waitress

---

For further details, please refer to the code in `app.py` or reach out to the project maintainer.
