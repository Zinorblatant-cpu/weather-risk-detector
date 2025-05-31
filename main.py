import requests
import os

# Importando funções de alertas climáticos (modulares)
from forecast.thunderstorms import check_thunderstorms
from forecast.wind import check_strong_wind
from forecast.frost import check_frost
from forecast.floods import check_floods
from forecast.drought_heatwave import check_dry_and_hot_weather
from forecast.wildfire import check_wildfire_risk


# Função para limpar a tela do terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Função principal do menu interativo
def menu(weather_data):
    while True:
        print("🌦️ Choose the weather risks you want to monitor:")
        print("[1] ⚡ Thunderstorms / Lightning")
        print("[2] 💨 Strong Winds (> 50 km/h)")
        print("[3] ❄️ Frost / Freezing Temperatures")
        print("[4] 💧 Floods / Heavy Rainfall")
        print("[5] ☀️ Dry & Hot Weather Risk (Heatwave + Drought)")
        print("[6] 🔥 Wildfire Risk (indirect detection)")
        print("[7] 🌍 Monitor All Risks")
        print("[8] ❌ Finish")

        try:
            choice = int(input("Enter your choice (1-8): "))
            clear_screen()

            if choice == 8:
                # Sair do programa
                print("👋 Exiting program. Have a great day!")
                break

            elif choice == 1:
                # Verificar alertas de trovoadas
                check_thunderstorms(weather_data)
                while True:
                    input("\nPress any key to return to the menu...")
                    clear_screen()
                    break

            elif choice == 2:
                # Verificar alertas de vento forte
                check_strong_wind(weather_data)
                while True:
                    input("\nPress any key to return to the menu...")
                    clear_screen()
                    break

            elif choice == 3:
                # Verificar alertas de geada
                check_frost(weather_data)
                while True:
                    input("\nPress any key to return to the menu...")
                    clear_screen()
                    break

            elif choice == 4:
                # Verificar alertas de enchentes
                check_floods(weather_data)
                while True:
                    input("\nPress any key to return to the menu...")
                    clear_screen()
                    break

            elif choice == 5:
                # Verificar risco de seca e calor extremo
                check_dry_and_hot_weather(weather_data)
                while True:
                    input("\nPress any key to return to the menu...")
                    clear_screen()
                    break
            
            elif choice == 6:
                # Verificar risco de incêndios florestais
                check_wildfire_risk(weather_data)
                while True:
                    input("\nPress any key to return to the menu...")
                    clear_screen()
                    break

            elif choice == 7:
                # Executar todas as verificações automaticamente
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
                # Opção inválida
                print("🚫 Option not yet implemented.\n")

        except ValueError:
            # Trata entrada inválida no menu
            clear_screen()
            print("❗ Please enter a valid number.\n")


# Bloco principal que executa a requisição à API
if __name__ == '__main__':
    # Chave da API OpenWeatherMap
    API_KEY = '512569ff925265363234407e3e1cac15'

    # Coordenadas da Antártida
    # Ótima região para testar baixas temperaturas e ventos fortes
    lat = -77.85  # Latitude
    lon = 166.67  # Longitude

    # Monta a URL da OpenWeatherMap API
    URL = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'

    print("📡 Making request to the API...")
    response = requests.get(URL)

    print(f"📶 Response status code: {response.status_code}")

    # Verifica se a resposta foi bem-sucedida 
    if response.status_code != 200:
        print("❌ Error in API response:")
        print(response.json())
    else:
        print("✅ Request successful!")
        weather_data = response.json()  # Converte resposta para JSON

        # Garante que os dados esperados estejam na resposta
        if 'list' not in weather_data:
            print("⚠️ Expected data not found in API response.")
        else:
            clear_screen()
            menu(weather_data)  # Inicia o menu interativo com os dados climáticos