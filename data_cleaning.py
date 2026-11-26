# ==========================================
# Python Sales Data Cleaning Script
# Author: Irfan Mehmood
# Purpose: Automate the cleaning of raw retail sales data, 
#          handle date format anomalies, and export for Power BI.
# ==========================================

import pandas as pd

def clean_sales_data(input_file, output_file):
    print(f"Loading raw data from {input_file}...")
    
    # 1. Load the data
    df = pd.read_csv(input_file)

    # 2. Convert Text to Datetime
    # Using errors='coerce' to turn invalid dates into NaT (Not a Time) instead of crashing
    print("Converting date columns...")
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

    # 3. Drop rows with invalid dates
    initial_count = len(df)
    df = df.dropna(subset=['Order Date', 'Ship Date'])
    dropped_count = initial_count - len(df)
    print(f"Dropped {dropped_count} rows with invalid dates.")

    # 4. Calculate Shipping Time (Days)
    print("Calculating shipping times...")
    df['Days_to_Ship'] = (df['Ship Date'] - df['Order Date']).dt.days

    # 5. Aggregate Results to find the data anomaly
    print("\n--- Average Shipping Time by Mode ---")
    avg_shipping = df.groupby('Ship Mode')['Days_to_Ship'].mean().round(2)
    print(avg_shipping)
    
    print("\nNOTE: Extreme values (>30 days) indicate raw data quality issues (mixed date formats).")
    
    # 6. Export the cleaned data
    print(f"\nExporting cleaned data to {output_file}...")
    df.to_csv(output_file, index=False)
    print("Process complete!")

# Run the function
if __name__ == "__main__":
    clean_sales_data('train.csv', 'cleaned_sales_data.csv')