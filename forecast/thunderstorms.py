from datetime import datetime

def check_thunderstorms(weather_data):
    """
    Verifica se há previsão de trovoadas nas próximas 24 horas.
    Utiliza os dados da API para identificar risco de tempestades.
    """

    # Variável que controla se algum alerta foi encontrado
    thunderstorm_alert_found = False
    
    # Cabeçalho do relatório
    print("\n⚡ THUNDERSTORM FORECAST (next 24h):")

    # Percorre as previsões dos próximos 24h (8 períodos de 3h)
    for forecast in weather_data['list'][:8]:  
        # Carrega o timestamp do período atual e converte para hora legível
        timestamp = forecast['dt']
        forecast_time = datetime.fromtimestamp(timestamp)
        formatted_time = forecast_time.strftime('%d/%m %H:%M')

        # Descrição geral do tempo (ex: 'Thunderstorm', 'Clear')
        weather_main = forecast['weather'][0]['main']

        # Descrição detalhada (ex: 'thunderstorm with light rain')
        weather_description = forecast['weather'][0]['description']

        # Probabilidade de chuva (convertida para porcentagem)
        pop = forecast['pop'] * 100  

        # Se houver palavra-chave 'thunderstorm' no clima, aciona alerta
        if 'thunderstorm' in weather_main.lower():
            thunderstorm_alert_found = True
            
            # Mostra alerta ao usuário
            print(f"⚠️ THUNDERSTORM ALERT: '{weather_description.title()}' expected at {formatted_time}")
            print(f"🌧️ Chance of rain: {pop:.0f}%")
            print("-" * 60)

    # Mensagem caso NENHUMA trovoadas tenha sido encontrada
    if not thunderstorm_alert_found:
        print("✅ No thunderstorms expected in the next 24 hours.")