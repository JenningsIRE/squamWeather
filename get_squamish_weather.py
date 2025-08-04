import pandas as pd
import requests

# Load your CSV and extract dates
df = pd.read_csv("squamish-sendage.csv", on_bad_lines='warn')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
unique_dates = df['date'].dropna().dt.strftime('%Y-%m-%d').unique()

# Squamish coordinates
lat = 49.7016
lon = -123.1558
tz = 'America/Vancouver'

weather_data = []

for date in unique_dates:
    print(f"Fetching weather for {date}...")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={date}&end_date={date}"
        f"&hourly=temperature_2m,relative_humidity_2m,windspeed_10m"
        f"&timezone={tz}"
    )

    try:
        res = requests.get(url)
        data = res.json()

        if 'hourly' in data:
            hourly = data['hourly']
            times = hourly['time']
            temps = hourly['temperature_2m']
            humidity = hourly['relative_humidity_2m']
            wind = hourly['windspeed_10m']

            # Find the entry closest to noon
            for i, time in enumerate(times):
                if "12:00" in time:
                    weather_data.append({
                        "date": date,
                        "temperature": temps[i],
                        "humidity": humidity[i],
                        "wind_speed": wind[i]
                    })
                    break
        else:
            print(f"No hourly data found for {date}")

    except Exception as e:
        print(f"Error fetching {date}: {e}")

# Save to CSV
weather_df = pd.DataFrame(weather_data)
weather_df.to_csv("squamish_weather_openmeteo.csv", index=False)
print("Saved to squamish_weather_openmeteo.csv")
