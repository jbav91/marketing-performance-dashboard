import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# 1. Load variables from the .env file (we go up one level because the script is in /scripts)
load_dotenv('.env')

# 2. Inject the exact path of the Google Cloud key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_key.json' 

# Initialize the official BigQuery client
client = bigquery.Client()

def run_budget_audit():
    print("🚀 Starting automated audit in Google BigQuery...\n")
    
    # 3. Query the table directly in the cloud
    # Notice we are using your actual project and the 'marketing_kpis' table
    query = """
    SELECT 
        campaign_id, 
        SUM(mark_spent) as total_spend, 
        SUM(revenue) as total_revenue
    FROM `mktng-performance-dashboard.data.marketing_kpis` 
    GROUP BY campaign_id;
    """
    
    # Execute the query in Google and download it as a DataFrame
    df = client.query(query).to_dataframe()
    
    # Calculate the mathematically correct global ROAS (Revenue / Spend)
    # We use fillna(0) to avoid errors if a campaign spent money but generated 0 revenue
    df['average_roas'] = (df['total_revenue'] / df['total_spend']).fillna(0)
    
    # 4. Define the BUSINESS RULES for the alert
    ROAS_THRESHOLD = 0.70
    MIN_SPEND = 1000.0
    
    critical_campaigns = df[(df['average_roas'] < ROAS_THRESHOLD) & (df['total_spend'] > MIN_SPEND)]
    
    # 5. Process and trigger the alerts
    if not critical_campaigns.empty:
        print(f"⚠️ CRITICAL ALERT DETECTED! Found {len(critical_campaigns)} campaigns burning budget:\n")
        print("-" * 65)
        
        for index, row in critical_campaigns.iterrows():
            campaign_id = int(row['campaign_id'])
            spend = row['total_spend']
            roas = row['average_roas']
            
            # Format a professional alert message
            alert_message = (
                f"🚨 ACTION REQUIRED: Pause Campaign ID: {campaign_id}\n"
                f"   • Current performance: ROAS of {roas:.2f} (Minimum threshold: {ROAS_THRESHOLD})\n"
                f"   • Money at risk: Total accumulated spend of ${spend:,.2f}"
            )
            print(alert_message)
            print("-" * 65)
            
        print("\n[INFO] In production, this script would send an automated message to Slack or Teams.")
        
    else:
        print("✅ Audit finished: All campaigns are operating within healthy ROAS ranges.")

if __name__ == "__main__":
    run_budget_audit()