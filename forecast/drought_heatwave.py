from datetime import datetime
from collections import defaultdict

def check_dry_and_hot_weather(weather_data):
    """
    Detecta condições de seca prolongada e ondas de calor nos próximos 5 dias.
    
    Critérios:
    - Seca: Baixa probabilidade de chuva (pop < 10%) + alta temperatura (temp_max >= 30°C) por 5 dias seguidos
    - Onda de calor: Temperatura máxima acima de 30°C por pelo menos 3 dias consecutivos
    
    A função agrupa os dados por dia e imprime alertas caso algum risco seja encontrado.
    """

    # Contadores de dias seguidos com condições climáticas adversas
    drought_days = 0
    heatwave_days = 0
    high_risk_found = False

    print("\n☀️ DRY & HOT WEATHER FORECAST (next 5 days):")

    # Agrupa previsões por data (ex: '2024-07-01')
    daily_data = defaultdict(list)

    # Passo 1: Percorre todas as previsões horárias
    for forecast in weather_data['list']:  
        try:
            # Coleta timestamp e converte para formato legível
            timestamp = forecast['dt']
            forecast_time = datetime.fromtimestamp(timestamp)
            day_key = forecast_time.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD

            # Probabilidade de chuva e temperatura máxima do período
            pop = forecast['pop']
            temp_max_c = forecast['main']['temp_max']

            # Armazena os dados no dicionário agrupado por dia
            daily_data[day_key].append({
                'pop': pop,
                'temp_max': temp_max_c
            })

        except KeyError as e:
            missing_field = e.args[0]
            print(f"⚠️ Missing field: '{missing_field}' in forecast at {forecast_time}")
            continue

    # Passo 2: Analisa cada dia agrupado
    for day, values in daily_data.items():
        # Calcula média da probabilidade de chuva e máxima da temperatura do dia
        avg_pop = sum(v['pop'] for v in values) / len(values)
        max_temp = max(v['temp_max'] for v in values)

        # Exibe informações do dia para depuração ou análise
        print(f"📅 Day {day} | Max Temp: {max_temp:.1f}°C | Avg Rain Chance: {avg_pop * 100:.0f}%")

        # Verifica condição de seca: baixa chuva + calor
        if avg_pop < 0.1 and max_temp >= 30:  
            drought_days += 1
            print(f"⚠️ DROUGHT RISK: Dry period detected | Temp={max_temp:.1f}°C | POP={avg_pop * 100:.0f}%")
            if drought_days >= 5:
                print(f"🔴 ALERT: Prolonged dry period detected starting from {day}")
                high_risk_found = True
        else:
            drought_days = 0  # Reinicia contador se um dia não estiver seco

        # Verifica condição de onda de calor: calor intenso por 3+ dias seguidos
        if max_temp >= 30:
            heatwave_days += 1
            print(f"🌡️ HEATWAVE RISK: High temperature of {max_temp:.1f}°C recorded")
            if heatwave_days >= 3:
                print(f"🔴 ALERT: Heatwave detected — temperatures above 30°C for 3+ days")
                high_risk_found = True
        else:
            heatwave_days = 0  # Reinicia contador se houver um dia frio

    # Mensagem final caso nenhum alerta tenha sido disparado
    if not high_risk_found:
        print("✅ No significant prolonged heat or drought conditions found.")