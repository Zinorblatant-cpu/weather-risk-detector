from datetime import datetime
from collections import defaultdict

def check_dry_and_hot_weather(weather_data):
    drought_days = 0
    heatwave_days = 0
    high_risk_found = False
    print("\n🌾 DROUGHT FORECAST (next 5 days):")

    daily_data = defaultdict(list)

    for forecast in weather_data['list']:  
        try:
            timestamp = forecast['dt']
            forecast_time = datetime.fromtimestamp(timestamp)
            day_key = forecast_time.strftime('%Y-%m-%d')  # Ex: '2024-07-01'

            pop = forecast['pop']
            temp_max_c = forecast['main']['temp_max']

            daily_data[day_key].append({'pop': pop, 'temp_max': temp_max_c})
        except KeyError as e:
            missing_field = e.args[0]
            print(f"⚠️ Missing field: '{missing_field}' in forecast at {forecast_time}")
            continue

    for day, values in daily_data.items():
        avg_pop = sum(v['pop'] for v in values) / len(values)
        max_temp = max(v['temp_max'] for v in values)

        print(f"📅 Day {day} | Max Temp: {max_temp:.1f}°C | Avg Rain Chance: {avg_pop * 100:.0f}%")

        if avg_pop < 0.1 and max_temp >= 30:  
            drought_days += 1
            print(f"⚠️ DROUGHT RISK: Dry period detected | Temp={max_temp:.1f}°C | POP={avg_pop * 100:.0f}%")
            if drought_days >= 5:
                print(f"🔴 ALERT: Prolonged dry period detected starting from {day}")
                high_risk_found = True
        else:
            drought_days = 0  

        if max_temp >= 30:
            heatwave_days += 1
            print(f"🌡️ HEATWAVE RISK: High temperature of {max_temp:.1f}°C recorded")
            if heatwave_days >= 3:
                print(f"🔴 ALERT: Heatwave detected — temperatures above 30°C for 3+ days")
                high_risk_found = True
        else:
            heatwave_days = 0

    if not high_risk_found:
        print("✅ No significant prolonged heat or drought conditions found.")