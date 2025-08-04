import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d

# Load CSVs
climbs_df = pd.read_csv("squamish-sendage.csv", on_bad_lines='warn')
weather_df = pd.read_csv("squamish_weather_openmeteo.csv")

# Convert dates
climbs_df['date'] = pd.to_datetime(climbs_df['date'], errors='coerce')
weather_df['date'] = pd.to_datetime(weather_df['date'], errors='coerce')

# Merge
merged_df = pd.merge(climbs_df, weather_df, on='date', how='inner')

# Normalize grade
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

# Binning configs for each variable
binning = {
    'temperature': {
        'bin_edges': np.arange(0, 45, 5),
        'xlabel': 'Temperature (°C)',
        'title': 'Send Distribution vs. Temperature',
        'filename': 'send_distribution_temperature.png'
    },
    'humidity': {
        'bin_edges': np.arange(0, 110, 10),
        'xlabel': 'Relative Humidity (%)',
        'title': 'Send Distribution vs. Humidity',
        'filename': 'send_distribution_humidity.png'
    },
    'wind_speed': {
        'bin_edges': np.arange(0, 50, 5),
        'xlabel': 'Wind Speed (km/h)',
        'title': 'Send Distribution vs. Wind Speed',
        'filename': 'send_distribution_wind.png'
    }
}

# Plotting loop
for var, config in binning.items():
    bin_edges = config['bin_edges']
    bin_labels = [f'{int(b)}–{int(b + (bin_edges[1] - bin_edges[0]))}' for b in bin_edges[:-1]]
    
    # Create bins
    merged_df[f'{var}_bin'] = pd.cut(merged_df[var], bins=bin_edges, labels=bin_labels, include_lowest=True)

    # Count sends by grade group and bin
    counts = (
        merged_df
        .groupby(['grade_group', f'{var}_bin'])
        .size()
        .unstack(fill_value=0)
    )

    # Normalize to percent within each grade group
    percent = counts.divide(counts.sum(axis=1), axis=0) * 100

    

    # Plot
    plt.figure(figsize=(12, 6))
    for group in percent.index:
        plt.plot(bin_labels, percent.loc[group], marker='o', label=group)

    plt.title(config['title'])
    plt.xlabel(config['xlabel'])
    plt.ylabel('Percentage of Sends (%)')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(title='Grade Group')
    plt.tight_layout()
    plt.savefig(config['filename'])
    plt.show()
