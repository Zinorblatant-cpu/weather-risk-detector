from datetime import datetime
from collections import defaultdict

def check_frost(weather_data):
    frost_days = 0
    frost_alert_found = False
    print("\n❄️ FROST FORECAST (next 5 days):")

    daily_forecasts = defaultdict(list)

    for forecast in weather_data['list']:  
        try:
            temp_min_celsius = forecast['main']['temp_min']
            weather_description = forecast['weather'][0]['description'].lower()
            timestamp = forecast['dt']
            forecast_time = datetime.fromtimestamp(timestamp)
            day_key = forecast_time.strftime('%Y-%m-%d')  
        except KeyError as e:
            missing_field = e.args[0]
            print(f"⚠️ Missing field: '{missing_field}' in forecast at {forecast_time}")
            continue

        daily_forecasts[day_key].append({
            'temp_min': temp_min_celsius,
            'weather_desc': weather_description
        })

    for day, forecasts in daily_forecasts.items():
        daily_min = min(f['temp_min'] for f in forecasts)
        weather_desc = forecasts[0]['weather_desc']

        if daily_min < 0 and ('clear' in weather_desc or 'clouds' in weather_desc):
            frost_days += 1
            print(f"❄️ FROST ALERT: Freezing temperature of {daily_min:.1f}°C expected on {day}")
            print(f"☁️ Weather: {weather_desc.title()}")
            print("-" * 60)

            if frost_days >= 5:  
                frost_alert_found = True
                print(f"⚠️ ALERT: Prolonged freezing period detected starting from {day}")
                break
        else:
            frost_days = 0  

    if not frost_alert_found:
        print("✅ No prolonged freezing period detected in the next 5 days.")