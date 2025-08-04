import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
import calendar

# Load CSVs
climbs_df = pd.read_csv("squamish-sendage.csv", on_bad_lines='warn')
weather_df = pd.read_csv("squamish_weather_openmeteo.csv")

# Convert date columns
climbs_df['date'] = pd.to_datetime(climbs_df['date'], errors='coerce')
weather_df['date'] = pd.to_datetime(weather_df['date'], errors='coerce')

# Merge
merged_df = pd.merge(climbs_df, weather_df, on='date', how='inner')

# Normalize grade values
merged_df['grade'] = merged_df['grade'].astype(str).str.strip().str.upper()
merged_df = merged_df[merged_df['grade'].str.match(r'^V([0-9]|1[0-4])$')]
merged_df['grade_num'] = merged_df['grade'].str.extract(r'(\d+)').astype(int)

# Grade grouping
def to_grade_group(g):
    if g <= 4:
        return 'V0–V4'
    elif g <= 9:
        return 'V5–V9'
    else:
        return 'V10–V14'

merged_df['grade_group'] = merged_df['grade_num'].apply(to_grade_group)

# Extract month (1–12) and name
merged_df['month'] = merged_df['date'].dt.month
merged_df['month_name'] = merged_df['month'].apply(lambda x: calendar.month_abbr[x])

# Count sends per month and grade group
counts = (
    merged_df
    .groupby(['grade_group', 'month'])
    .size()
    .unstack(fill_value=0)
)

# Normalize within each grade group (row-wise)
percent = counts.divide(counts.sum(axis=1), axis=0) * 100



# Plot
plt.figure(figsize=(12, 6))
months = [calendar.month_abbr[m] for m in range(1, 13)]

for group in percent.index:
    plt.plot(months, percent.loc[group], marker='o', label=group)

plt.title('Seasonal Climbing Trends by Grade Group')
plt.xlabel('Month')
plt.ylabel('Percentage of Sends (%)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Grade Group')
plt.tight_layout()
plt.savefig('send_distribution_by_month.png')
plt.show()
