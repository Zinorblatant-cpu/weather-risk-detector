import requests
import os
from datetime import datetime
from collections import defaultdict


def clear_screen():   
    os.system('cls' if os.name == 'nt' else 'clear')

def check_thunderstorms(weather_data):
    thunderstorm_alert_found = False
    print("\n⚡ THUNDERSTORM FORECAST (next 24h):")

    for forecast in weather_data['list'][:8]:  # Próximos 8 períodos (24 horas)
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        formatted_time = forecast_time.strftime('%d/%m %H:%M')

        weather_main = forecast['weather'][0]['main']
        weather_description = forecast['weather'][0]['description']
        pop = forecast['pop'] * 100  # Probabilidade de chuva em %

        if 'thunderstorm' in weather_main.lower():
            thunderstorm_alert_found = True
            print(f"⚠️ THUNDERSTORM ALERT: '{weather_description.title()}' expected at {formatted_time}")
            print(f"🌧️ Chance of rain: {pop:.0f}%")
            print("-" * 60)

    if not thunderstorm_alert_found:
        print("✅ No thunderstorms expected in the next 24 hours.")

    while True:
        input("\nPress any key to return to the menu...")
        clear_screen()
        break

def check_strong_wind(weather_data):
    strong_wind_alert_found = False
    print("\n🌬️ STRONG WIND FORECAST (next 24h):")

    for forecast in weather_data['list'][:8]:
        wind_speed_mps = forecast['wind']['speed']
        wind_speed_kph = wind_speed_mps * 3.6
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        formatted_time = forecast_time.strftime('%d/%m %H:%M')

        if wind_speed_kph > 50:
            strong_wind_alert_found = True
            print(f"⚠️ HIGH WIND SPEED: Wind of {wind_speed_kph:.1f} km/h expected at {formatted_time}")

    if not strong_wind_alert_found:
        print("✅ No strong winds expected in the next 24 hours.")

    while True:
        input("\nPress any key to return to the menu...")
        clear_screen()
        break

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

    while True:
        input("\nPress any key to return to the menu...")
        clear_screen()
        break

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

    while True:
            input("\nPress any key to return to the menu...")
            clear_screen()
            break

def check_drought(weather_data):
    drought_days = 0
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

        if avg_pop < 0.1 and max_temp >= 30:  
            drought_days += 1
            print(f"☀️ {day} - High risk of drought: Max Temp={max_temp:.1f}°C | Avg POP={avg_pop * 100:.0f}%")
            if drought_days >= 5:
                print(f"⚠️ ALERT: Prolonged dry period detected starting from {day}")
                high_risk_found = True
                break
        else:
            drought_days = 0  
    if not high_risk_found:
        print("✅ No prolonged dry period detected in the next 5 days.")

    while True:
        input("\nPress any key to return to the menu...")
        clear_screen()
        break

def menu(weather_data):
    while True:
        print("🌦️ Choose the weather risks you want to monitor:")
        print("[1] ⚡ Thunderstorms / Lightning")
        print("[2] 💨 Strong Winds (> 50 km/h)")
        print("[3] ❄️ Frost / Freezing Temperatures")
        print("[4] 💧 Floods / Heavy Rainfall")
        print("[5] 🌾 Drought Conditions")
        print("[6] 🔥 Wildfire Risk (indirect detection)")
        print("[7] 🌡️ Heatwaves / Extreme Heat")
        print("[8] 🌍 Monitor All Risks")
        print("[9] ❌ Finish")

        try:
            choice = int(input("Enter your choice (1-9): "))
            clear_screen()

            if choice == 9:
                print("👋 Exiting program. Have a great day!")
                break

            elif choice == 1:
                check_thunderstorms(weather_data)

            elif choice == 2:
                check_strong_wind(weather_data)

            elif choice == 3:
                check_frost(weather_data)

            elif choice == 4:
                check_floods(weather_data) 

            elif choice == 5:
                check_drought(weather_data)

            else:
                print("🚫 Option not yet implemented.\n")
        except ValueError:
            clear_screen()
            print("❗ Please enter a valid number.\n")



if __name__ == '__main__':
    API_KEY = '512569ff925265363234407e3e1cac15'

    # Coordenadas de Bamaco, Mali
    lat = -30.0346
    lon = -51.2177

    URL = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'

    print("📡 Making request to the API...")
    response = requests.get(URL)

    print(f"📶 Response status code: {response.status_code}")

    if response.status_code != 200:
        print("❌ Error in API response:")
        print(response.json())
    else:
        print("✅ Request successful!")
        weather_data = response.json()

        if 'list' not in weather_data:
            print("⚠️ Expected data not found in API response.")
        else:
            menu(weather_data)
            