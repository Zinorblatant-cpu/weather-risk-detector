from datetime import datetime
from collections import defaultdict

def check_frost(weather_data):
    """
    Detecta períodos consecutivos com risco de geada nos próximos 5 dias.
    
    Critérios:
    - Temperatura mínima do dia < 0°C
    - Tempo limpo ou parcialmente nublado (sem chuva/neve)
    
    A função agrupa os dados horários em dias completos e verifica a tendência climática diária.
    """

    # Contador de dias seguidos com geada
    frost_days = 0
    frost_alert_found = False
    
    print("\n❄️ FROST FORECAST (next 5 days):")

    # Dicionário para agrupar as previsões por data (ex: '2024-07-01')
    daily_forecasts = defaultdict(list)

    # Passo 1: Percorre todas as previsões (até 5 dias)
    for forecast in weather_data['list']:  
        try:
            # Coleta temperatura mínima e descrição do tempo
            temp_min_celsius = forecast['main']['temp_min']
            weather_description = forecast['weather'][0]['description'].lower()
            
            # Converte timestamp Unix para uma data/hora legível
            timestamp = forecast['dt']
            forecast_time = datetime.fromtimestamp(timestamp)
            day_key = forecast_time.strftime('%Y-%m-%d')  # Ex: '2024-07-01'

        except KeyError as e:
            # Caso algum campo esperado esteja ausente
            missing_field = e.args[0]
            print(f"⚠️ Missing field: '{missing_field}' in forecast at {forecast_time}")
            continue

        # Armazena os dados do dia para análise posterior
        daily_forecasts[day_key].append({
            'temp_min': temp_min_celsius,
            'weather_desc': weather_description
        })

    # Passo 2: Analisa cada dia agrupado
    for day, forecasts in daily_forecasts.items():
        # Calcula a menor temperatura do dia
        daily_min = min(f['temp_min'] for f in forecasts)
        
        # Usa a descrição do tempo do primeiro período do dia
        weather_desc = forecasts[0]['weather_desc']

        # Verifica se há condições de geada
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
            # Reinicia o contador se houver um dia sem geada
            frost_days = 0  

    # Mensagem final caso não tenha alertas
    if not frost_alert_found:
        print("✅ No prolonged freezing period detected in the next 5 days.")