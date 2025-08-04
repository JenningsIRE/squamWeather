import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSVs
climbs_df = pd.read_csv("squamish-sendage.csv", on_bad_lines='warn')
weather_df = pd.read_csv("squamish_weather_openmeteo.csv")

# Convert dates
climbs_df['date'] = pd.to_datetime(climbs_df['date'], errors='coerce')
weather_df['date'] = pd.to_datetime(weather_df['date'], errors='coerce')

# Merge on date
merged_df = pd.merge(climbs_df, weather_df, on='date', how='inner')

# Clean and normalize grades
merged_df['grade'] = merged_df['grade'].astype(str).str.strip().str.upper()
merged_df = merged_df[merged_df['grade'].str.match(r'^V([0-9]|1[0-4])$')]
merged_df['grade_num'] = merged_df['grade'].str.extract(r'(\d+)').astype(int)

# Grade groups
def to_grade_group(g):
    if g <= 4:
        return 'V0–V4'
    elif g <= 9:
        return 'V5–V9'
    else:
        return 'V10–V14'

merged_df['grade_group'] = merged_df['grade_num'].apply(to_grade_group)

# Temp bins
bin_edges = np.arange(0, 45, 5)
bin_labels = [f'{i}–{i+5}' for i in bin_edges[:-1]]
merged_df['temp_bin'] = pd.cut(merged_df['temperature'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# Count sends per (grade group, temp bin)
group_counts = (
    merged_df
    .groupby(['grade_group', 'temp_bin'])
    .size()
    .unstack(fill_value=0)
)

# Normalize within each grade group (row-wise)
percentage = group_counts.divide(group_counts.sum(axis=1), axis=0) * 100

# Plot
plt.figure(figsize=(12, 6))

for group in percentage.index:
    plt.plot(percentage.columns.astype(str), percentage.loc[group], marker='o', label=group)

plt.title('Distribution of Sends by Temperature for Each Grade Group')
plt.xlabel('Temperature Bin (°C)')
plt.ylabel('Percentage of Sends (%)')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Grade Group')
plt.tight_layout()
plt.show()
