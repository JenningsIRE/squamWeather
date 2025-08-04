import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
climbs_df = pd.read_csv("squamish-sendage.csv", on_bad_lines='warn')
weather_df = pd.read_csv("squamish_weather_openmeteo.csv")
climbs_df['date'] = pd.to_datetime(climbs_df['date'], errors='coerce')
weather_df['date'] = pd.to_datetime(weather_df['date'], errors='coerce')

# Merge on date
merged_df = pd.merge(climbs_df, weather_df, on='date', how='inner')

# Extract month
merged_df['month'] = merged_df['date'].dt.month

# Clean grade
merged_df['grade'] = merged_df['grade'].astype(str).str.strip().str.upper()
merged_df = merged_df[merged_df['grade'].str.match(r'^V([0-9]|1[0-5])$')]
merged_df['grade_num'] = merged_df['grade'].str.extract(r'(\d+)').astype(int)
merged_df = merged_df[merged_df['grade_num'] <= 12]

# Average monthly temperature
monthly_avg_temperature = merged_df.groupby('month')['temperature'].mean()

# Calculate difference from average
merged_df['temperature_diff'] = merged_df.apply(
    lambda row: row['temperature'] - monthly_avg_temperature.loc[row['month']],
    axis=1
)

# Bin temperature differences in 3
bin_edges = np.arange(-15, 15, 3)  # Cover wide range just in case
merged_df['temperature_diff_bin'] = pd.cut(merged_df['temperature_diff'], bins=bin_edges)

# Group climbs
def grade_group(g):
    if 0 <= g <= 4:
        return 'V0–V4'
    elif 5 <= g <= 9:
        return 'V5–V9'
    elif 10 <= g <= 12:
        return 'V10–V12'
    else:
        return None

merged_df['grade_group'] = merged_df['grade_num'].apply(grade_group)
merged_df = merged_df[merged_df['grade_group'].notnull()]

# Count and normalize
counts = merged_df.groupby(['grade_group', 'temperature_diff_bin']).size().unstack(fill_value=0)
percent = counts.divide(counts.sum(axis=1), axis=0) * 100

# Plot
plt.figure(figsize=(14, 7))
bin_centers = [interval.mid for interval in percent.columns]

for group in percent.index:
    plt.plot(bin_centers, percent.loc[group], marker='o', label=group)

plt.title('Send % by temperature Deviation from Monthly Average')
plt.xlabel('temperature Deviation from Monthly Avg')
plt.ylabel('Percentage of Sends (%)')
plt.axvline(0, color='gray', linestyle='--', linewidth=1, label='Monthly Average')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Grade Group')
plt.tight_layout()
plt.savefig('temperature_deviation_vs_sends.png')
plt.show()
