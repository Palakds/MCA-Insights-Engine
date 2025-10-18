# MCA Insights Engine

This project is a Python application built for the "MCA Insights Engine" assessment. It consolidates company data, detects daily changes, and provides an interactive Streamlit dashboard to search, analyze, and chat with the data.

This implementation serves as a functional prototype demonstrating the core logic, as per the assignment guidelines.

---

## Architecture & Workflow

The project is built around two main Python scripts:

1.  **`script/change_log.py`**: This script handles all the backend data processing (Tasks A, B, and E1).
    * It loads the two sample datasets (`mah_roc_mca_data_1.csv` and `mah_roc_mca_data_2.csv`).
    * It cleans the data: strips column names, removes duplicates, and handles missing values.
    * It performs **change detection** by comparing the two files to find:
        * New Incorporations
        * Deregistered/Removed Companies
        * Field-level updates (e.g., CompanyStatus, AuthorizedCapital).
    * It generates two output files in the `Dataset/` folder: `daily_change_log.csv` and `daily_summary.txt`.

2.  **`script/dashboard.py`**: This script runs the frontend user interface using Streamlit (Tasks D and E2).
    * It loads the master dataset, the change log, and the enriched data.
    * It displays the "Daily AI Summary" on the sidebar.
    * It provides filters (by Company Status) and a search bar (by Company Name or CIN).
    * It displays enriched company details and their specific change history.
    * It includes a "Chat with MCA Data" section that uses rule-based logic to answer natural language questions.

---

## Setup & Installation

To run this project locally, please follow these steps.

### Prerequisites
* Python 3.9
* `pip` (Python package installer)

### Installation
1.  **Clone the repository (or download the ZIP):**
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

---

## Running the Application

The application is run in two stages:

### Step 1: Run the Data Processing Script
First, you must generate the change log and summary files.

```bash
python script/change_log.py