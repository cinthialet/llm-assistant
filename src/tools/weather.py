import httpx
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Obtém informações climáticas atuais de uma cidade.

    Usa a API gratuita wttr.in para buscar dados do clima.

    Args:
        city: Nome da cidade (ex: 'Paris', 'New York', 'São Paulo')

    Returns:
        Informações do clima incluindo temperatura e condições.
    """
    # Print para checagem da chamada da ferramenta
    print(f"\n[TOOL CALL] get_weather('{city}')")

    try:
        url = f"https://wttr.in/{city}?format=j1"

        with httpx.Client(timeout=15.0) as client:
            response = client.get(url)
            response.raise_for_status()

        data = response.json()

        # Normaliza os nomes para comparação (minúsculo, sem país)
        user_city = city.lower().split(",")[0].strip()
        api_city = data["nearest_area"][0]["areaName"][0]["value"]

        # Verifica se a cidade retornada pela API corresponde à pedida e vice versa
        if user_city not in api_city.lower() and api_city.lower() not in user_city:
            result = f"Erro: Cidade '{city}' não encontrada."
            print(f"[WEATHER TOOL RESULT] {result}")
            return result

        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        condition = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        feels_like = current["FeelsLikeC"]

        result = (
            f"Clima em {api_city}:\n"
            f"- Temperatura: {temp_c}°C\n"
            f"- Sensação térmica: {feels_like}°C\n"
            f"- Condição: {condition}\n"
            f"- Umidade: {humidity}%"
        )
        # Print para checagem do resultado da ferramenta
        print(f"[WEATHER TOOL RESULT] {temp_c}°C, {condition}")
        return result

    # Tratamento de erros
    except Exception as e:
        result = f"Erro: Não foi possível obter o clima para '{city}' - {e}"
        print(f"[WEATHER TOOL RESULT] {result}")
        return result
