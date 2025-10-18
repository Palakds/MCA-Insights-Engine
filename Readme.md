# MCA Insights Engine

## Project Overview

The MCA Insights Engine is a Python-based data processing and visualization application. It is designed to consolidate, track, and analyze company master data from the Ministry of Corporate Affairs (MCA).

This implementation serves as a functional prototype, demonstrating core logic for data ingestion, change detection, and interactive analysis as required by the assessment. The application features a backend processing script for data normalization and a frontend Streamlit dashboard for search, visualization, and conversational queries.

## Architecture and Workflow

The project's functionality is divided into two primary components:

1.  **Backend Processing (`script/change_log.py`)**
    This script manages all data processing tasks (Tasks A, B, and E1). Its responsibilities include:
    * Loading and parsing the two sample MCA datasets.
    * Data cleansing, which involves standardizing column names, removing duplicate entries, and handling null values.
    * Executing change detection logic by comparing the two datasets to identify new incorporations, deregistrations, and field-level updates (e.g., CompanyStatus, AuthorizedCapital).
    * Generating `daily_change_log.csv` and `daily_summary.txt` in the `Dataset/` directory.

2.  **Frontend Interface (`script/dashboard.py`)**
    This script runs the user-facing application using Streamlit (Tasks D and E2). Its features include:
    * Loading the master dataset, change log, and enriched data file.
    * Displaying the "Daily AI Summary" in the sidebar.
    * Providing interactive data filters (by Company Status and Registration Year) and a search bar (by Company Name or CIN).
    * Presenting enriched company details and a log of their specific change history.
    * A "Chat with MCA Data" interface that uses rule-based logic to respond to natural language queries.

## Setup and Installation

Please follow these steps to set up the project environment locally.

### Prerequisites
* Python 3.9+
* `pip` (Python package installer)

### Installation
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/mca-insights-engine.git](https://github.com/your-username/mca-insights-engine.git)
    cd mca-insights-engine
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
