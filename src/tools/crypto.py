from datetime import datetime

import httpx
from langchain_core.tools import tool


@tool
def get_crypto_price(symbol: str, date: str) -> str:
    """Obtém o preço de uma criptomoeda em uma data específica usando a API da Binance.

    Args:
        symbol: Par de trading (ex: 'BTCUSDT', 'ETHUSDT', 'SOLUSDT').
                Sempre use pares com USDT para preços em dólar.
        date: Data no formato 'YYYY-MM-DD' (ex: '2024-01-15')

    Returns:
        Informações de preço da criptomoeda na data especificada, se listada na Binance.
    """
    # Print para checagem da chamada da ferramenta
    print(f"\n[TOOL CALL] get_crypto_price('{symbol}', '{date}')")

    try:
        # Converte data para timestamp em milissegundos
        dt = datetime.strptime(date, "%Y-%m-%d")
        start_ts = int(dt.timestamp() * 1000)
        end_ts = start_ts + (24 * 60 * 60 * 1000)

        # Endpoint da API Binance para klines (dados de candlestick)
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol.upper(),
            "interval": "1d",
            "startTime": start_ts,
            "endTime": end_ts,
            "limit": 1,
        }

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()

        data = response.json()

        if not data:
            result = f"Erro: Não foram encontrados dados para {symbol} em {date}."
            print(f"[CRYPTO TOOL RESULT] {result}")
            return result

        # Extrai os preços do dia
        prices = data[0]
        open_price = float(prices[1])
        high_price = float(prices[2])
        low_price = float(prices[3])
        close_price = float(prices[4])
        volume = float(prices[5])

        result = (
            f"Preço de {symbol.upper()} em {date}:\n"
            f"- Abertura: ${open_price:,.2f}\n"
            f"- Máxima: ${high_price:,.2f}\n"
            f"- Mínima: ${low_price:,.2f}\n"
            f"- Fechamento: ${close_price:,.2f}\n"
            f"- Volume: {volume:,.2f}"
        )
        # Print para checagem do resultado da ferramenta
        print(f"[CRYPTO TOOL RESULT] {symbol.upper()} em {date}: ${close_price:,.2f}")
        return result

    # Tratamento de erros
    except ValueError as e:
        result = f"Erro: Formato de data inválido. Use 'YYYY-MM-DD'. Detalhe: {e}"
        print(f"[CRYPTO TOOL RESULT] {result}")
        return result
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            result = f"Erro: Par de trading '{symbol}' não encontrado na Binance."
        else:
            result = f"Erro: Falha na API da Binance - HTTP {e.response.status_code}"
        print(f"[CRYPTO TOOL RESULT] {result}")
        return result
    except Exception as e:
        result = f"Erro: Não foi possível obter o preço de {symbol} - {e}"
        print(f"[CRYPTO TOOL RESULT] {result}")
        return result
