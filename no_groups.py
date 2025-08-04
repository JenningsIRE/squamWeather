import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import calendar

# Load CSVs
climbs_df = pd.read_csv("squamish-sendage.csv", on_bad_lines='warn')
weather_df = pd.read_csv("squamish_weather_openmeteo.csv")

# Convert date columns
climbs_df['date'] = pd.to_datetime(climbs_df['date'], errors='coerce')
weather_df['date'] = pd.to_datetime(weather_df['date'], errors='coerce')

# Merge on date
merged_df = pd.merge(climbs_df, weather_df, on='date', how='inner')

# Clean and extract grades
merged_df['grade'] = merged_df['grade'].astype(str).str.strip().str.upper()
merged_df = merged_df[merged_df['grade'].str.match(r'^V([0-9]|1[0-5])$')]
merged_df['grade_num'] = merged_df['grade'].str.extract(r'(\d+)').astype(int)

# Filter to V0–V12 only
merged_df = merged_df[merged_df['grade_num'] <= 12]

# ----------------------------
# 📈 Plot 1: Sends by Month
# ----------------------------

merged_df['month'] = merged_df['date'].dt.month
months = [calendar.month_abbr[m] for m in range(1, 13)]

# Count sends by grade and month
month_counts = merged_df.groupby(['grade', 'month']).size().unstack(fill_value=0)
month_percent = month_counts.divide(month_counts.sum(axis=1), axis=0) * 100

# Plot
plt.figure(figsize=(14, 7))
for grade in sorted(month_percent.index, key=lambda g: int(g[1:])):
    plt.plot(months, month_percent.loc[grade], marker='o', label=grade)

plt.title('Send Distribution by Month (Grades V0–V12)')
plt.xlabel('Month')
plt.ylabel('Percentage of Sends (%)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Grade', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('send_distribution_by_month_v0_v12.png')
plt.show()

# ----------------------------
# 📈 Plot 2: Sends by Temperature
# ----------------------------

# Bin temperatures into 5°C increments
bin_edges = np.arange(0, 45, 5)
bin_labels = [f'{i}–{i+5}' for i in bin_edges[:-1]]
merged_df['temp_bin'] = pd.cut(merged_df['temperature'], bins=bin_edges, labels=bin_labels, include_lowest=True)

# Count and normalize
temp_counts = merged_df.groupby(['grade', 'temp_bin']).size().unstack(fill_value=0)
temp_percent = temp_counts.divide(temp_counts.sum(axis=1), axis=0) * 100

# Plot
plt.figure(figsize=(14, 7))
for grade in sorted(temp_percent.index, key=lambda g: int(g[1:])):
    plt.plot(bin_labels, temp_percent.loc[grade], marker='o', label=grade)

plt.title('Send Distribution by Temperature (Grades V0–V12)')
plt.xlabel('Temperature Bin (°C)')
plt.ylabel('Percentage of Sends (%)')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(title='Grade', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('send_distribution_by_temperature_v0_v12.png')
plt.show()
