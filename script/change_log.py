import pandas as pd
import numpy as np

## 1. Data Loading and Preprocessing 

print("Attempting to load data...")

# Load the two datasets from the 'Dataset' subfolder
try:
    df_oct10 = pd.read_csv('Dataset/mah_roc_mca_data_1.csv', encoding='latin1', low_memory=False)
    df_oct11 = pd.read_csv('Dataset/mah_roc_mca_data_2.csv', encoding='latin1', low_memory=False)
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Please make sure 'mah_roc_mca_data_1.csv' and 'mah_roc_mca_data_2.csv' are inside the 'Dataset' folder.")
    exit() # Stop the script if files aren't found
except Exception as e:
    print(f"An unexpected error occurred while reading files: {e}")
    exit()

# Remove any leading/trailing spaces from all column names
df_oct10.columns = df_oct10.columns.str.strip()
df_oct11.columns = df_oct11.columns.str.strip()

## Data Cleaning 

print(f"\nOriginal Oct 10 count: {len(df_oct10)}")
print(f"Original Oct 11 count: {len(df_oct11)}")

# Keep the last entry for any duplicate CIN, assuming it's the most recent
df_oct10.drop_duplicates(subset='CIN', keep='last', inplace=True)
df_oct11.drop_duplicates(subset='CIN', keep='last', inplace=True)

print(f"De-duplicated Oct 10 count: {len(df_oct10)}")
print(f"De-duplicated Oct 11 count: {len(df_oct11)}")

# Set the CIN as the index for easier comparison
df_oct10.set_index('CIN', inplace=True)
df_oct11.set_index('CIN', inplace=True)

# Convert capital columns to numeric
cols_to_clean = ['AuthorizedCapital', 'PaidupCapital']
for col in cols_to_clean:
    df_oct10[col] = pd.to_numeric(df_oct10[col], errors='coerce')
    df_oct11[col] = pd.to_numeric(df_oct11[col], errors='coerce')

# Fill missing values in key status columns
df_oct10['CompanyStatus'] = df_oct10['CompanyStatus'].fillna('Unknown')
df_oct11['CompanyStatus'] = df_oct11['CompanyStatus'].fillna('Unknown')

print("\nData for Oct 10th loaded and cleaned.")
print(df_oct10.info())
print("\nData for Oct 11th loaded and cleaned.")
print(df_oct11.info())


##2. Change Detection Logic 

print("\nStarting change detection...")

# Find new incorporations (in Oct 11 but not in Oct 10)
new_cins = df_oct11.index.difference(df_oct10.index)
print(f"Found {len(new_cins)} new incorporations.")

# Find deregistered/removed companies (in Oct 10 but not in Oct 11)
removed_cins = df_oct10.index.difference(df_oct11.index)
print(f"Found {len(removed_cins)} removed companies.")

#Prepare for logging 
change_log = []
change_date = '2025-10-11' 

# Log new incorporations
for cin in new_cins:
    change_log.append({
        'CIN': cin,
        'Change_Type': 'New Incorporation',
        'Field_Changed': 'N/A',
        'Old_Value': 'N/A',
        'New_Value': 'N/A',
        'Date': change_date
    })

# Log removed companies
for cin in removed_cins:
     change_log.append({
        'CIN': cin,
        'Change_Type': 'Deregistered/Removed',
        'Field_Changed': 'N/A',
        'Old_Value': 'N/A',
        'New_Value': 'N/A',
        'Date': change_date
    })

# Find field-level updates (for companies existing in both files)
common_cins = df_oct10.index.intersection(df_oct11.index)
print(f"Checking {len(common_cins)} common companies for updates...")

# Define columns to check for changes
columns_to_track = ['CompanyStatus', 'AuthorizedCapital', 'PaidupCapital']

for cin in common_cins:
    for col in columns_to_track:
        old_val = df_oct10.at[cin, col]
        new_val = df_oct11.at[cin, col]
        
        is_different = False
        # Check numeric fields (handling NaN)
        if pd.api.types.is_numeric_dtype(df_oct10[col]):
            if not np.isclose(old_val, new_val, equal_nan=True):
                is_different = True
        # Check string/object fields
        elif old_val != new_val:
            is_different = True
            
        if is_different:
            change_log.append({
                'CIN': cin,
                'Change_Type': 'Field Update',
                'Field_Changed': col,
                'Old_Value': old_val,
                'New_Value': new_val,
                'Date': change_date
            })

##3. Save Outputs

# Save the Change Log
change_log_df = pd.DataFrame(change_log)
output_log_path = 'Dataset/daily_change_log.csv'
change_log_df.to_csv(output_log_path, index=False)
print(f"\nSuccessfully generated '{output_log_path}' with {len(change_log_df)} total changes.")


# Generate and save the AI Summary
new_count = len(new_cins)
removed_count = len(removed_cins)
# Get unique CINs that had a field update
updated_cins = change_log_df[change_log_df['Change_Type'] == 'Field Update']['CIN'].nunique()

summary_text = (
    f"Daily Summary for {change_date}\n\n"
    f"New incorporations: {new_count:,}\n"
    f"Deregistered/Removed: {removed_count:,}\n"
    f"Updated companies: {updated_cins:,}\n"
)

summary_path = 'Dataset/daily_summary.txt'
with open(summary_path, 'w') as f:
    f.write(summary_text)

print(f"Successfully generated '{summary_path}'.")
print("\n Script Finished")