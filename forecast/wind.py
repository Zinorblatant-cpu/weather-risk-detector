from datetime import datetime

def check_strong_wind(weather_data):
    strong_wind_alert_found = False
    print("\n🌬️ STRONG WIND FORECAST (next 24h):")

    for forecast in weather_data['list'][:8]:
        wind_speed_mps = forecast['wind']['speed']
        #print(wind_speed_mps)
        wind_speed_kph = wind_speed_mps * 3.6
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        formatted_time = forecast_time.strftime('%d/%m %H:%M')

        if wind_speed_kph > 50:
            strong_wind_alert_found = True
            print(f"⚠️ HIGH WIND SPEED: Wind of {wind_speed_kph:.1f} km/h expected at {formatted_time}")

    if not strong_wind_alert_found:
        print("✅ No strong winds expected in the next 24 hours.")