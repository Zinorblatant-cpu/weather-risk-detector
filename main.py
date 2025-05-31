import requests
import os
from forecast.thunderstorms import check_thunderstorms
from forecast.wind import check_strong_wind
from forecast.frost import check_frost
from forecast.floods import check_floods
from forecast.drought_heatwave import check_dry_and_hot_weather
from forecast.wildfire import check_wildfire_risk


def clear_screen():   
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(weather_data):
    while True:
        print("🌦️ Choose the weather risks you want to monitor:")
        print("[1] ⚡ Thunderstorms / Lightning")
        print("[2] 💨 Strong Winds (> 50 km/h)")
        print("[3] ❄️ Frost / Freezing Temperatures")
        print("[4] 💧 Floods / Heavy Rainfall")
        print("[5] ☀️ Dry & Hot Weather Risk (Heatwave + Drought)")
        print("[6] 🌡️ Heatwaves / Extreme Heat")
        print("[7] 🌍 Monitor All Risks")
        print("[8] ❌ Finish")

        try:
            choice = int(input("Enter your choice (1-8): "))
            clear_screen()

            if choice == 8:
                print("👋 Exiting program. Have a great day!")
                break

            elif choice == 1:
                clear_screen()
                check_thunderstorms(weather_data)

            elif choice == 2:
                clear_screen()
                check_strong_wind(weather_data)

            elif choice == 3:
                clear_screen()
                check_frost(weather_data)

            elif choice == 4:
                clear_screen()
                check_floods(weather_data) 

            elif choice == 5:
                clear_screen()
                check_dry_and_hot_weather(weather_data)
            
            elif choice == 6:
                clear_screen()
                check_wildfire_risk(weather_data)

            elif choice == 7:
                clear_screen()
                check_thunderstorms(weather_data)
                print('-' * 60)
                check_strong_wind(weather_data)
                print('-' * 60)
                check_frost(weather_data)
                print('-' * 60)
                check_floods(weather_data) 
                print('-' * 60)
                check_dry_and_hot_weather(weather_data)
                print('-' * 60)
                check_wildfire_risk(weather_data)
                print('-' * 60)
                while True:
                    input("\nPress any key to return to the menu...")
                    clear_screen()
                    break


            else:
                print("🚫 Option not yet implemented.\n")
        except ValueError:
            clear_screen()
            print("❗ Please enter a valid number.\n")

if __name__ == '__main__':
    API_KEY = '512569ff925265363234407e3e1cac15'

    lat = 12.65
    lon = -8.98

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
            clear_screen()
            menu(weather_data)
            