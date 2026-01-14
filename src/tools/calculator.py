from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Realiza cálculos matemáticos a partir de uma expressão.

    Args:
        expression: Expressão matemática para calcular (ex: "2 + 2", "10 * 5", "2 ** 8")

    Returns:
        Resultado do cálculo ou mensagem de erro
    """
    print(f"\n[TOOL CALL] calculator({expression})")

    # Valida se a expressão contém apenas caracteres permitidos
    allowed = set("0123456789+-*/().% ")
    if not all(c in allowed for c in expression):
        result = "Erro: Expressão contém caracteres inválidos."
        print(f"[CALCULATOR TOOL RESULT] {result}")
        return result

    try:
        result = eval(expression)
        print(f"[CALCULATOR TOOL RESULT] {result}")
        return str(result)
    except Exception as e:
        result = f"Erro ao calcular: {e}"
        print(f"[CALCULATOR TOOL RESULT] {result}")
        return result