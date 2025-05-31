from datetime import datetime
from collections import defaultdict

def check_wildfire_risk(weather_data):
    """
    Analisa os dados climáticos para identificar dias com risco de incêndio florestal.
    
    Critérios:
    - Temperatura máxima > 35°C
    - Umidade média < 40%
    - Vento máximo > 30 km/h
    - Baixa chance de chuva (pop < 10%)
    
    A função agrupa os dados por dia e calcula um 'risk_score' baseado nas condições acima.
    """

    print("\n🔥 WILDFIRE RISK FORECAST (next 5 days):")

    # Dicionário para agrupar previsões por data (ex: '2024-07-01')
    daily_risk = defaultdict(list)

    # Passo 1: Agrupando previsões por dia
    for forecast in weather_data['list']: 
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        day_key = forecast_time.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD para facilitar leitura

        try:
            # Coleta os principais dados climáticos
            temp_max_c = forecast['main']['temp_max']   # Temperatura máxima em Celsius
            humidity = forecast['main']['humidity']     # Umidade do ar (%)
            wind_speed_mps = forecast['wind']['speed']  # Velocidade do vento em m/s
            pop = forecast['pop']                     # Probabilidade de precipitação (0.0 a 1.0)
        except KeyError as e:
            # Se faltar algum campo essencial, pula esse registro
            continue

        # Converte velocidade do vento de m/s para km/h
        wind_speed_kph = wind_speed_mps * 3.6

        # Armazena os dados no dicionário agrupado por dia
        daily_risk[day_key].append({
            'temp': temp_max_c,
            'humidity': humidity,
            'wind': wind_speed_kph,
            'pop': pop
        })

    wildfire_alert_found = False

    # Passo 2: Analisando cada dia
    for day, values in sorted(daily_risk.items()):
        # Cálculo das métricas diárias
        avg_pop = sum(v['pop'] for v in values) / len(values)
        max_temp = max(v['temp'] for v in values)
        max_wind = max(v['wind'] for v in values)
        avg_humidity = sum(v['humidity'] for v in values) / len(values)

        # Pula dias muito frios (abaixo de 10°C) — sem risco real de incêndio
        if max_temp < 10:
            continue

        # Calcula o score de risco para o dia
        risk_score = 0
        if max_temp > 35:
            risk_score += 1
        if avg_humidity < 40:
            risk_score += 1
        if max_wind > 30:
            risk_score += 1
        if avg_pop < 0.1:
            risk_score += 1

        # Passo 3: Exibe alertas com base no nível de risco
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

    # Caso nenhum alerta tenha sido disparado
    if not wildfire_alert_found:
        print("✅ No significant wildfire risk detected in the next 5 days.")
