from datetime import datetime

def check_floods(weather_data):
    flood_alert_found = False
    print("\n🌊 FLOOD FORECAST (next 24h):") 

    for forecast in weather_data['list'][:8]:
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        formatted_time = forecast_time.strftime('%d/%m %H:%M')

        try:
            rain_volume = forecast.get('rain', {}).get('3h', 0)
            pop = forecast['pop'] * 100
            temp_max_c = forecast['main']['temp_max']

        except KeyError as e:
            missing_field = e.args[0]
            print(f"⚠️ Missing field: '{missing_field}' in forecast at {formatted_time}")
            continue

        if rain_volume >= 50:
            flood_alert_found = True
            print(f"⚠️ HEAVY RAIN ALERT: {rain_volume:.1f} mm of rain in last 3 hours at {formatted_time}")

        elif pop >= 80 and temp_max_c < 30:
            flood_alert_found = True
            print(f"🟡 POSSIBLE FLOOD RISK: High rain probability ({pop:.0f}%) at {formatted_time}")
    
    if not flood_alert_found:
        print("✅ No significant risk of floods in the next 24 hours.")