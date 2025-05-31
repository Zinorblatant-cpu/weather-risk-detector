from datetime import datetime

def check_thunderstorms(weather_data):
    thunderstorm_alert_found = False
    print("\n⚡ THUNDERSTORM FORECAST (next 24h):")

    for forecast in weather_data['list'][:8]:  
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        formatted_time = forecast_time.strftime('%d/%m %H:%M')

        weather_main = forecast['weather'][0]['main']
        weather_description = forecast['weather'][0]['description']
        pop = forecast['pop'] * 100  

        if 'thunderstorm' in weather_main.lower():
            thunderstorm_alert_found = True
            print(f"⚠️ THUNDERSTORM ALERT: '{weather_description.title()}' expected at {formatted_time}")
            print(f"🌧️ Chance of rain: {pop:.0f}%")
            print("-" * 60)

    if not thunderstorm_alert_found:
        print("✅ No thunderstorms expected in the next 24 hours.")