import pandas as pd
import matplotlib.pyplot as plt

# Load CSVs
climbs_df = pd.read_csv("squamish-sendage.csv", on_bad_lines='warn')
weather_df = pd.read_csv("squamish_weather_openmeteo.csv")

# Convert 'date' to datetime
climbs_df['date'] = pd.to_datetime(climbs_df['date'], errors='coerce')
weather_df['date'] = pd.to_datetime(weather_df['date'], errors='coerce')

# Merge on date
merged_df = pd.merge(climbs_df, weather_df, on='date', how='inner')

# Clean and normalize grade column
merged_df['grade'] = merged_df['grade'].astype(str).str.strip().str.upper()

# Keep only V0 to V12
merged_df = merged_df[merged_df['grade'].str.match(r'^V([0-9]|1[0-2])$')]

# Compute mean temperature per grade
mean_temp_by_grade = (
    merged_df.groupby('grade')['temperature']
    .mean()
    .reset_index()
    .sort_values(by='grade', key=lambda col: col.str.extract(r'(\d+)').astype(int)[0])
)

# Plot
plt.figure(figsize=(10, 6))
plt.bar(mean_temp_by_grade['grade'], mean_temp_by_grade['temperature'], color='salmon')
plt.ylabel('Mean Temperature (°C)')
plt.xlabel('Climbing Grade (V-scale)')
plt.title('Mean Temperature vs. Climbing Grade (V0–V12)')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
