import streamlit as st
import pandas as pd
import os

## Page Configuration
st.set_page_config(layout="wide", page_title="MCA Insights Engine")

## File Paths
MASTER_FILE = os.path.join('Dataset', 'mah_roc_mca_data_2.csv')
CHANGE_LOG_FILE = os.path.join('Dataset', 'daily_change_log.csv')
ENRICHED_FILE = os.path.join('Dataset', 'enriched_data.csv')
SUMMARY_FILE = os.path.join('Dataset', 'daily_summary.txt')

## Data Loading
# Use Streamlit's cache to load data only once
@st.cache_data
def load_data():
    try:
        master_df = pd.read_csv(MASTER_FILE, low_memory=False)
        
        # This ensures the CIN is the unique index for lookup
        master_df.drop_duplicates(subset='CIN', keep='last', inplace=True)
        master_df.set_index('CIN', inplace=True)

        master_df['CompanyRegistrationdate_date'] = pd.to_datetime(master_df['CompanyRegistrationdate_date'], errors='coerce')
        master_df['RegistrationYear'] = master_df['CompanyRegistrationdate_date'].dt.year.fillna(0).astype(int)

        change_log_df = pd.read_csv(CHANGE_LOG_FILE)
        enriched_df = pd.read_csv(ENRICHED_FILE)
        
        # Read the summary text file
        with open(SUMMARY_FILE, 'r') as f:
            summary_content = f.read()
            
        return master_df, change_log_df, enriched_df, summary_content
    except FileNotFoundError as e:
        st.error(f"Error: A data file was not found. Please check your 'Dataset' folder. Details: {e}")
        return None, None, None, None
    except Exception as ex:
        st.error(f"An error occurred during data loading: {ex}")
        return None, None, None, None

# Load all data
master_df, change_log_df, enriched_df, summary_content = load_data()

# Stop the app if data loading failed
if master_df is None:
    st.stop()

## Main Page & Sidebar
st.title("📈 MCA Insights Engine")
st.write("A dashboard to analyze, search, and track changes in MCA company data.")

## 1. AI Summary (Task E)
st.sidebar.header("Daily AI Summary")
if summary_content:
    st.sidebar.text(summary_content)
else:
    st.sidebar.error("daily_summary.txt not found.")

## 2. Filters (Task D)
st.sidebar.header("Company Filters")
# Get unique values for filters
status_options = master_df['CompanyStatus'].unique()
selected_status = st.sidebar.multiselect("Filter by Company Status:", status_options, default=status_options[0])

# Get unique values for year filter
year_options = sorted(master_df['RegistrationYear'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Filter by Registration Year:", options=year_options, index=None)

## 3. Main Search & Display (Task D)
st.header("Search and Explore Companies")

# Get search term *before* filtering
search_term = st.text_input("Search by Company Name or CIN (e.g., 'SANJIVEENI INVENTURES PRIVATE LIMITED' or 'U74110MH2019PTC333452')")

# 1. Apply search first
if search_term:
    # Search the entire master_df
    search_results_df = master_df[
        master_df['CompanyName'].str.contains(search_term, case=False, na=False) |
        master_df.index.str.contains(search_term, case=False, na=False)
    ]
else:
    # If no search, start with the full dataframe
    search_results_df = master_df
    
# 2. Then, apply sidebar filters to the search results
if selected_status:
    # Filter the search results (or the full list) by status
    final_filtered_df = search_results_df[search_results_df['CompanyStatus'].isin(selected_status)]
if selected_year:
    # Filter by year
    final_filtered_df = final_filtered_df[final_filtered_df['RegistrationYear'] == selected_year]
else:
    # If no status is selected, show all search results
    final_filtered_df = search_results_df.copy()

st.dataframe(final_filtered_df.head(20)) # Show top 20 results
st.write(f"Showing {len(final_filtered_df)} companies.")

## 4. Enriched Data & Change History (Task D)
st.header("Enriched Details & Change History")
st.write("Select a company from the search results to see more details.")

# Create a dropdown from the *final* search results
if not final_filtered_df.empty:
    # Get a list of Company Names from the search results to feed the selectbox
    company_name_list = final_filtered_df['CompanyName'].tolist()
    selected_company_name = st.selectbox("Select Company:", options=company_name_list)
    
    if selected_company_name:
        # Get the details for the selected company
        # Use .loc to be safe with potential duplicate company names
        company_details_series = final_filtered_df[final_filtered_df['CompanyName'] == selected_company_name]
        
        if not company_details_series.empty:
            company_details = company_details_series.iloc[0]
            # .name gets the index value, which is our CIN
            selected_cin = company_details.name 
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Enriched Data")
                # Find matching data in the enriched file
                enriched_info = enriched_df[enriched_df['CIN'] == selected_cin]
                if not enriched_info.empty:
                    st.dataframe(enriched_info)
                else:
                    st.info("No enriched data found for this CIN.")
            
            with col2:
                st.subheader("Recent Change History")
                # Find matching data in the change log
                change_history = change_log_df[change_log_df['CIN'] == selected_cin]
                if not change_history.empty:
                    st.dataframe(change_history)
                else:
                    st.info("No change history found for this CIN.")
        else:
            st.warning("Could not retrieve company details.")
else:
    # This handles the case where the search/filter yields 0 results
    st.info("No companies match the current search and filter criteria.")

## 5. Chatbot (Task E, Part 2)
st.header("💬 Chat with MCA Data")
st.write("Ask simple questions about the dataset.")

# We already have the data loaded in these DataFrames:
# master_df, change_log_df, enriched_df

chat_input = st.text_input("Your question:", placeholder="e.g., How many active companies are there?")

if chat_input:
    # Convert input to lowercase to make it easy to check
    query = chat_input.lower()
    
    ## Rule-Based Logic
    
    if "how many" in query and "active" in query:
        # 1. Answer: "How many active companies are there?"
        active_count = master_df[master_df['CompanyStatus'] == 'Active'].shape[0]
        st.success(f"Answer: There are {active_count:,} 'Active' companies in the Maharashtra dataset.")
    
    elif "how many" in query and "new incorporations" in query:
        # 2. Answer: "How many new incorporations?"
        new_count = change_log_df[change_log_df['Change_Type'] == 'New Incorporation'].shape[0]
        st.success(f"Answer: There were {new_count:,} new incorporations in the last update.")
        
    elif "how many" in query and "struck off" in query:
        # 3. Answer: "How many companies were struck off?"
        struck_off_count = master_df[master_df['CompanyStatus'] == 'Strike Off'].shape[0]
        st.success(f"Answer: There are {struck_off_count:,} 'Strike Off' companies in the dataset.")
        
    elif "how many" in query and "public" in query:
        # 4. Answer: "How many public companies?"
        public_count = master_df[master_df['CompanyClass'] == 'Public'].shape[0]
        st.success(f"Answer: There are {public_count:,} 'Public' companies.")

    elif "how many" in query and "private" in query:
        # 5. Answer: "How many private companies?"
        private_count = master_df[master_df['CompanyClass'] == 'Private'].shape[0]
        st.success(f"Answer: There are {private_count:,} 'Private' companies.")

    elif "how many" in query and ("updated" in query or "changed" in query) and "capital" in query:
        # 6. Answer: "How many companies updated their capital?"
        capital_updates = change_log_df[
            (change_log_df['Field_Changed'] == 'AuthorizedCapital') |
            (change_log_df['Field_Changed'] == 'PaidupCapital')
        ]['CIN'].nunique() # .nunique() counts unique companies
        st.success(f"Answer: {capital_updates:,} companies updated their capital in the last update.")

    elif "list" in query and "capital over 1 crore" in query:
        # 7. Answer: "List companies with authorized capital over 1 crore."
        # 1 Crore = 10,000,000
        high_value_companies = master_df[master_df['AuthorizedCapital'] > 10000000]
        st.success(f"Answer: Found {len(high_value_companies):,} companies with Authorized Capital > 1 Crore. Showing top 20:")
        st.dataframe(high_value_companies.head(20))

    elif "list" in query and "enriched companies" in query:
        # 8. Answer: "List the enriched companies."
        st.success("Answer: Here are the 10 sample enriched companies:")
        st.dataframe(enriched_df)
        
    else:
        # Default answer if no rule matches
        st.warning("Sorry, I can only answer simple, pre-defined questions, such as:\n"
                   "- 'How many active companies are there?'\n"
                   "- 'How many new incorporations?'\n"
                   "- 'How many companies were struck off?'\n"
                   "- 'How many companies are Public?'\n"
                   "- 'How many companies are Private?'\n"
                   "- 'How many companies updated their capital?'\n"
                   "- 'List companies with authorized capital over 1 crore.'\n"
                   "- 'List the enriched companies.'")