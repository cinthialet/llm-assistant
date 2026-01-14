import re

from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Avalia uma expressão matemática e retorna o resultado.

    Use esta ferramenta para QUALQUER cálculo matemático. Suporta:
    - Aritmética básica: +, -, *, /
    - Potências: ** ou ^
    - Parênteses para agrupamento

    Args:
        expression: Uma expressão matemática como '128 * 46' ou '(10 + 5) / 3'

    Returns:
        O resultado calculado como string, ou mensagem de erro se inválido.
    """
    # Print para checagem da chamada da ferramenta
    print(f"\n[TOOL CALL] calculator('{expression}')")

    try:
        # Sanitiza: substitui caracteres não seguros pelos seguros
        sanitized = expression.replace("^", "**")
        sanitized = sanitized.replace("x", "*").replace("×", "*")
        sanitized = sanitized.replace("÷", "/")

        # Validação: permite apenas caracteres seguros para avaliação matemática
        if not re.match(r"^[\d\s\+\-\*\/\.\(\)\%\*]+$", sanitized):
            result = f"Erro: Caracteres inválidos na expressão '{expression}'"
            print(f"[TOOL RESULT] {result}")
            return result

        result = eval(sanitized)

        # Formatação do resultado
        if isinstance(result, float) and result.is_integer():
            result = str(int(result))
        elif isinstance(result, float):
            result = f"{result:.6f}".rstrip("0").rstrip(".")
        else:
            result = str(result)
        # Print para checagem do resultado da ferramenta
        print(f"[CALCULATOR TOOL RESULT] {result}")
        return result

    # Tratamento de erros
    except ZeroDivisionError:
        result = "Erro: Divisão por zero"
        print(f"[CALCULATOR TOOL RESULT] {result}")
        return result
    except SyntaxError:
        result = f"Erro: Sintaxe inválida na expressão '{expression}'"
        print(f"[CALCULATOR TOOL RESULT] {result}")
        return result
    except Exception as e:
        result = f"Erro: Não foi possível avaliar '{expression}' - {e}"
        print(f"[CALCULATOR TOOL RESULT] {result}")
        return result
