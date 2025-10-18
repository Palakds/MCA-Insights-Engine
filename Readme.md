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

    ### Step 1: Run the Data Processing Script
```bash
python script/change_log.py
```

Note: This step is only necessary if the source data files are available. As mentioned in the "Data and Enrichment Notes," the pre-processed output files are already included in this repository.

Step 2: Launch the Streamlit Dashboard
Once the log files are available, you can launch the interactive dashboard.

```Bash
streamlit run script/dashboard.py
```
This will automatically open the application in your web browser.

Data and Enrichment Notes
Please be aware of the following two points regarding the project's data:

Source Data File Exclusion: The change_log.py script is designed to run against two source files. However, one source file (mah_roc_mca_data_1.csv, 137 MB) exceeds GitHub's 100 MB file limit and has been excluded from this repository via .gitignore. As such, the change_log.py script cannot be run as-is. The pre-processed output files (daily_change_log.csv, daily_summary.txt) are included in the repository, allowing the dashboard to be run immediately.

Task C: Web Enrichment: The script/enrichment.py was developed to scrape ZaubaCorp for supplementary company data. This script was blocked by the target server's security (HTTP 403: Forbidden). As a representative implementation, a manual sample file, Dataset/enriched_data.csv, was created. The dashboard loads this static file to demonstrate the full enrichment logic.
