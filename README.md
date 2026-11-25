# Python Sales Data Cleaning

## Project Overview
This project demonstrates the use of Python (Pandas) to automate the cleaning and preprocessing of a raw retail sales dataset (9,800 records). The goal was to convert messy text dates into proper datetime objects, calculate shipping times, and export a clean CSV ready for business intelligence tools like Power BI.

## Tools Used
*   **Google Colab** (Python environment)
*   **Pandas** (Data manipulation and cleaning)
*   **Python 3**

## The Data Challenge
The raw dataset (`train.csv`) contained `Order Date` and `Ship Date` columns stored as text strings (objects) in a mixed US/UK format (e.g., `MM/DD/YYYY` and `DD/MM/YYYY`). This caused severe anomalies when trying to calculate shipping times (e.g., reporting 153 days for a Second Class shipment).

## The Python Solution

### 1. Loading the Data
```python
import pandas as pd
```
# Load the raw data
```
df = pd.read_csv('train.csv')
```

### 2. Converting Text to Datetime

To calculate date math, we must force Pandas to recognize the columns as dates. I used errors='coerce' to safely handle any impossible dates without crashing the script.
# Convert text to datetime
```
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')
```
# Drop rows where dates could not be parsed
```
df = df.dropna(subset=['Order Date', 'Ship Date'])
```

### 3. Calculating Shipping Time

With the dates recognized properly, calculating the difference in days takes just one line of code:
```
df['Days_to_Ship'] = (df['Ship Date'] - df['Order Date']).dt.days
```

### 4. Aggregating the Results

I grouped the cleaned data by Ship Mode to find the average shipping time:
```
avg_shipping = df.groupby('Ship Mode')['Days_to_Ship'].mean().round(2)
print(avg_shipping)
```

## The Results & Data Quality Insight

The Python script successfully calculated the average shipping times across the 9,800 records:

*   **Same Day:** 1.96 days
*   **First Class:** 62.84 days
*   **Second Class:** 97.00 days
*   **Standard Class:** 145.77 days

> **Business Insight:** 
> The Python analysis perfectly mirrored my SQL findings. The extreme shipping times (145 days) confirm a severe data quality issue in the raw source where dates were mixed between US (`MM/DD/YYYY`) and UK (`DD/MM/YYYY`) formats.

> **Business Action:** 
> By automating this in Python, a Data Analyst can run this script on any new incoming CSV file. The next step in production would be to add a filter to exclude unrealistic dates (e.g., `Days_to_Ship > 30`) and export the clean data for Power BI visualization.

### 5. Exporting the Clean Data

Finally, the script exports the cleaned dataset to a new CSV file, ready for visualization.
```
df.to_csv('cleaned_sales_data.csv', index=False)
```
