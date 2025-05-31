from datetime import datetime
from collections import defaultdict

def check_wildfire_risk(weather_data):
    print("\n🔥 WILDFIRE RISK FORECAST (next 5 days):")

    daily_risk = defaultdict(list)

    # Agrupa os dados por dia
    for forecast in weather_data['list']: 
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        day_key = forecast_time.strftime('%Y-%m-%d')  # Ex: '2024-07-01'

        try:
            temp_max_c = forecast['main']['temp_max']
            humidity = forecast['main']['humidity']
            wind_speed_mps = forecast['wind']['speed']
            pop = forecast['pop']
        except KeyError as e:
            continue  # Pula se faltar campo

        wind_speed_kph = wind_speed_mps * 3.6

        daily_risk[day_key].append({
            'temp': temp_max_c,
            'humidity': humidity,
            'wind': wind_speed_kph,
            'pop': pop
        })

    wildfire_alert_found = False

    # Analisa cada dia
    for day, values in sorted(daily_risk.items()):
        # Média da chuva e umidade; máxima da temperatura e vento
        avg_pop = sum(v['pop'] for v in values) / len(values)
        max_temp = max(v['temp'] for v in values)
        max_wind = max(v['wind'] for v in values)
        avg_humidity = sum(v['humidity'] for v in values) / len(values)

        # Cálculo do risco por dia
        risk_score = 0
        if max_temp > 35:
            risk_score += 1
        if avg_humidity < 40:
            risk_score += 1
        if max_wind > 30:
            risk_score += 1
        if avg_pop < 0.1:
            risk_score += 1

        # Alertas por nível de risco
        if risk_score >= 3:
            wildfire_alert_found = True
            print(f"🔴 HIGH RISK OF WILDFIRE on {day}")
            print(f"🌡️ Max Temp: {max_temp:.1f}°C | 💧 Avg Humidity: {avg_humidity:.0f}%")
            print(f"🌬️ Max Wind: {max_wind:.1f} km/h | 🌦️ Rain Chance: {avg_pop * 100:.0f}%")
            print("-" * 60)

        elif risk_score == 2:
            wildfire_alert_found = True
            print(f"⚠️ MEDIUM RISK OF FIRE on {day}")
            print(f"🌡️ Max Temp: {max_temp:.1f}°C | 💧 Humidity: {avg_humidity:.0f}%")
            print("-" * 60)

        elif risk_score == 1:
            print(f"🟡 LOW RISK OF FIRE on {day}")
            print(f"🌡️ Max Temp: {max_temp:.1f}°C | 💧 Humidity: {avg_humidity:.0f}%")
            print("-" * 60)

    if not wildfire_alert_found:
        print("✅ No significant wildfire risk detected in the next 5 days.")