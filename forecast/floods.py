from datetime import datetime

def check_floods(weather_data):
    """
    Analisa os dados da API para detectar risco de enchentes ou alagamentos nas próximas 24h.
    
    Critérios:
    - Volume de chuva >= 50 mm nas últimas 3 horas
    - Alta probabilidade de chuva (pop >= 80%) combinada com baixa temperatura (temp < 30°C)
    
    A função imprime alertas no terminal com base nesses critérios.
    """

    # Variável que indica se algum alerta foi encontrado
    flood_alert_found = False

    print("\n🌊 FLOOD FORECAST (next 24h):")

    # Percorre os primeiros 8 períodos (24 horas) da previsão horária
    for forecast in weather_data['list'][:8]:
        # Carrega o timestamp e converte para formato legível
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        formatted_time = forecast_time.strftime('%d/%m %H:%M')

        try:
            # Chuva acumulada nas últimas 3 horas (em mm)
            rain_volume = forecast.get('rain', {}).get('3h', 0)

            # Probabilidade de chuva (convertida para porcentagem)
            pop = forecast['pop'] * 100

            # Temperatura máxima do período (usado como filtro secundário)
            temp_max_c = forecast['main']['temp_max']

        except KeyError as e:
            # Trata campos ausentes na resposta da API
            missing_field = e.args[0]
            print(f"⚠️ Missing field: '{missing_field}' at {formatted_time}")
            continue

        # Verifica se há chuva forte (> 50 mm nas últimas 3h)
        if rain_volume >= 50:
            flood_alert_found = True
            print(f"⚠️ HEAVY RAIN ALERT: {rain_volume:.1f} mm of rain in last 3 hours at {formatted_time}")

        # Se não, verifica se há alta chance de chuva e tempo frio/moderado
        elif pop >= 80 and temp_max_c < 30:
            flood_alert_found = True
            print(f"🟡 POSSIBLE FLOOD RISK: High rain probability ({pop:.0f}%) at {formatted_time}")
    
    # Mensagem caso nenhum alerta tenha sido disparado
    if not flood_alert_found:
        print("✅ No significant risk of floods in the next 24 hours.")
