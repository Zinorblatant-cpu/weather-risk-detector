from datetime import datetime

def check_strong_wind(weather_data):
    """
    Verifica se há previsão de vento forte (> 50 km/h) nas próximas 24 horas.
    
    A função analisa os primeiros 8 períodos (cada um com 3h de intervalo),
    convertendo a velocidade do vento de m/s para km/h, e imprime alertas caso
    condições de vento forte sejam encontradas.
    """

    # Variável que controla se algum alerta foi acionado
    strong_wind_alert_found = False
    
    # Cabeçalho da análise de vento forte
    print("\n💨 STRONG WIND FORECAST (next 24h):")

    # Percorre os primeiros 8 registros (24 horas)
    for forecast in weather_data['list'][:8]:
        # Velocidade do vento em metros por segundo (m/s)
        wind_speed_mps = forecast['wind']['speed']

        # Converte para quilômetros por hora (km/h)
        wind_speed_kph = wind_speed_mps * 3.6

        # Timestamp Unix → data/hora formatada para mostrar ao usuário
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        formatted_time = forecast_time.strftime('%d/%m %H:%M')

        # Critério: vento > 50 km/h
        if wind_speed_kph > 50:
            strong_wind_alert_found = True
            print(f"⚠️ HIGH WIND SPEED: Wind of {wind_speed_kph:.1f} km/h expected at {formatted_time}")

    # Mensagem final caso não haja vento forte detectado
    if not strong_wind_alert_found:
        print("✅ No strong winds expected in the next 24 hours.")