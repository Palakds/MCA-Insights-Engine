import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os

print("Starting enrichment process...")

# Define file paths
LOG_FILE = os.path.join('Dataset', 'daily_change_log.csv')
OUTPUT_FILE = os.path.join('Dataset', 'enriched_data.csv')

# 1. Load the change log
try:
    change_log_df = pd.read_csv(LOG_FILE)
except FileNotFoundError:
    print(f"Error: '{LOG_FILE}' not found. Please run change_log.py first.")
    exit()

# 2. Get a sample of 50 unique CINs
unique_cins = change_log_df['CIN'].unique()
sample_cins = unique_cins[:50] # Taking the first 50 as a sample

print(f"Found {len(unique_cins)} unique CINs. Taking a sample of {len(sample_cins)}.")

enriched_data = []

# 3. Loop through each CIN and scrape data
for cin in sample_cins:
    url = f"https://www.zaubacorp.com/company/{cin}"
    
    try:
        # Set a robust User-Agent to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.google.com/'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Scrape Company Name
            try:
                company_name = soup.find('h1').text.strip()
            except:
                company_name = 'Not Found'

            # Scrape Director Names
            director_names = []
            try:
                # Find the table with director info
                director_table = soup.find('table', id='table-5') # This ID is often correct for directors
                if director_table:
                    # Find all links to director profiles within that table
                    director_links = director_table.find_all('a', href=lambda href: href and '/director/' in href)
                    for link in director_links:
                        director_names.append(link.text.strip())
            except:
                pass # Fail silently if scraping fails

            enriched_data.append({
                'CIN': cin,
                'COMPANY_NAME': company_name,
                'DIRECTORS': ', '.join(director_names) if director_names else 'Not Found',
                'SOURCE': 'ZaubaCorp',
                'SOURCE_URL': url
            })
            
            print(f"Successfully scraped: {cin}")
        else:
            print(f"Failed to fetch: {cin} (Status code: {response.status_code})")
            
        # Wait 1 second between requests to avoid rate-limiting
        time.sleep(1) 

    except Exception as e:
        print(f"Error processing {cin}: {e}")

# 4. Save the new enriched dataset
if enriched_data:
    enriched_df = pd.DataFrame(enriched_data)
    enriched_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nEnrichment complete. File '{OUTPUT_FILE}' saved.")
else:
    print("\nNo data was enriched.")

print("\nScript Finished.")