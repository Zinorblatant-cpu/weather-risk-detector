# 🌤️ Sistema de Alertas Climáticos

## 📌 Descrição Geral

Este é um **sistema de detecção de riscos climáticos** desenvolvido em Python que consome dados da **OpenWeatherMap API** para identificar condições adversas nos próximos 5 dias. Ele oferece uma interface no terminal com opções interativas para verificar:

- ⚡ Trovoadas
- 💨 Vento forte
- ❄️ Geada / Temperaturas negativas
- 💧 Enchentes ou chuva intensa
- ☀️ Seca prolongada e ondas de calor
- 🔥 Risco indireto de incêndios florestais

O objetivo do projeto é demonstrar como é possível usar previsões climáticas para **prever e alertar sobre eventos climáticos adversos**, usando apenas as informações disponíveis na API OpenWeatherMap (plano gratuito).

---

## 🎯 Objetivo do Projeto

- Entender e consumir dados de uma API pública de clima (OpenWeatherMap)
- Detectar automaticamente condições climáticas adversas
- Apresentar alertas claros ao usuário via terminal
- Mostrar boas práticas de programação modular e organização de código
- Estudar análise de risco com base em condições meteorológicas

Ideal tanto para **projetos acadêmicos** quanto para sistemas simples de apoio à agricultura, segurança ambiental ou planejamento urbano.

---

## 🛠️ Funcionamento Interno

### 🔁 Estrutura Modular

Cada tipo de alerta foi implementado como uma função separada, permitindo futura modularização em arquivos independentes. As principais funções incluem:

| Função | Descrição |
|-------|-----------|
| `check_thunderstorms()` | Verifica se há trovoadas nas próximas 24h |
| `check_strong_wind()` | Detecta vento acima de 50 km/h |
| `check_frost()` | Analisa dias seguidos com geada |
| `check_floods()` | Avalia chuvas fortes (> 50 mm) e alta probabilidade de chuva |
| `check_drought()` | Detecta períodos secos + calor intenso |
| `check_wildfire_risk()` | Calcula risco de incêndio com base em temperatura, umidade, vento e precipitação |

Todas essas funções recebem o objeto `weather_data`, extraído da resposta da API, e analisam os dados conforme critérios específicos.

---

## 🧮 Lógica de Detecção de Riscos

O projeto usa **critérios técnicos** para detectar cada risco. Exemplo:

### 1. **Vento forte**
- Velocidade > 50 km/h
- Baseado no campo `wind.speed` (em m/s)

### 2. **Geada**
- Temperatura mínima < 0°C
- Tempo limpo ou nublado (`clear sky`, `few clouds`, etc.)
- Baseado no campo `main.temp_min`

### 3. **Seca + Onda de Calor**
- Baixa probabilidade de chuva (`pop < 0.1`)
- Alta temperatura máxima (`temp_max >= 30°C`)
- Análise por dias consecutivos

### 4. **Risco de Incêndio (indireto)**
- Temperatura > 35°C
- Umidade média < 40%
- Vento > 30 km/h
- Baixa chance de chuva (`pop < 0.1`)
- Score de risco calculado por dia

---

## 📦 Requisitos Técnicos

- Python 3.x
- Bibliotecas:
  - `requests` – Para requisições HTTP
  - `datetime` – Manipulação de datas
  - `collections.defaultdict` – Agrupamento de dados por dia
  - `os` – Limpeza de tela no terminal

```bash
pip install requests python-dotenv
```

Se você estiver usando `.env` para ocultar sua chave da API, também instale:

```bash
pip install python-dotenv
```

---

## 🧪 Como o Projeto Trabalha com Dados Horários

A OpenWeatherMap retorna dados a cada 3 horas (`list`), totalizando até 40 registros (5 dias × 8 horários/dia). O projeto agrupa esses dados por dia e aplica lógica de análise diária para evitar falso positivo com base em apenas 1 ou 2 períodos.

Exemplo:
```python
for forecast in weather_data['list'][:8]:  # Próximas 24h
    ...
```

---

## 🧩 Arquitetura do Código

O projeto segue uma abordagem **modular e estruturada**, onde cada tipo de alerta tem seu próprio arquivo e pode ser reutilizado ou expandido facilmente.

Estrutura atual:

```
main.py                  # Menu principal e controle
forecast/
    thunderstorms.py     # Alerta de trovoadas
    wind.py              # Alerta de vento forte
    frost.py             # Alerta de geada
    floods.py            # Alerta de enchentes
    drought_heatwave.py  # Alerta de seca e calor
    wildfire.py          # Risco de incêndios
requirements.txt         # Dependências do projeto
README.md                # Este documento
```

---

## 🧪 Exemplo de Saída

```
🌦️ Choose the weather risks you want to monitor:
[1] ⚡ Thunderstorms / Lightning
[2] 💨 Strong Winds (> 50 km/h)
[3] ❄️ Frost / Freezing Temperatures
[4] 💧 Floods / Heavy Rainfall
[5] ☀️ Dry & Hot Weather Risk (Heatwave + Drought)
[6] 🔥 Wildfire Risk (indirect detection)
[7] 🌍 Monitor All Risks
[8] ❌ Finish
```

Ao selecionar uma opção, o programa imprime alertas como:

```
⚠️ HIGH WIND SPEED: Wind of 59.4 km/h expected at 05/06 15:00
```

---

## 📊 Fluxo de Execução

1. O script faz uma requisição para a OpenWeatherMap API
2. Os dados são convertidos de JSON para variáveis manipuláveis
3. Cada função analisa os dados sob um critério específico
4. Alertas são exibidos no terminal com base na previsão
5. O usuário pode navegar entre as opções via menu

---

## 📁 Funções Principais Explicadas

### 1. `check_thunderstorms()`
Detecta trovoadas com base no campo `weather.main`.

### 2. `check_strong_wind()`
Converte `wind.speed` de `m/s` para `km/h` e avisa se > 50 km/h.

### 3. `check_frost()`
Agrupa previsões por dia e verifica temperaturas mínimas com tempo claro/nublado.

### 4. `check_floods()`
Verifica volume de chuva (`rain.3h`) e chance de chuva (`pop`) para alertar sobre enchentes.

### 5. `check_dry_and_hot_weather()`
Combina baixa precipitação e alta temperatura para indicar seca ou onda de calor.

### 6. `check_wildfire_risk()`
Calcula um score de risco com base em:
- Temperatura alta
- Umidade baixa
- Vento forte
- Baixa probabilidade de chuva

---

## 📝 Benefícios do Projeto

- ✅ Uso de **API realista** (OpenWeatherMap)
- ✅ Interface interativa no terminal
- ✅ Fácil expansão para outros tipos de risco
- ✅ Boa prática de tratamento de erros e validação de campos
- ✅ Um otímo alertas de riscos

---

## 👨‍🏫 Integrantes

Integrantes desse projeto:

- **Nome:** Leonardo Lopes rm:565437


---

## 🧾 Créditos

Desenvolvido como parte de um projeto acadêmico pela disciplina Soluções Energeticas, ministrada pelo professor André, na instituição FIAP.

---
