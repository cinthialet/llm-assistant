"""LLM Assistant - Agente de IA com capacidades de Tool Calling.

Este assistente pode:
- Responder perguntas de conhecimento geral diretamente
- Usar uma calculadora para operações matemáticas

Uso:
    uv run python main.py           # Modo interativo (padrão)
    uv run python main.py --test    # Executa suite de testes
"""

import argparse
import sys

from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

from src.agent.assistant import create_assistant, run_query


def interactive_mode(assistant) -> None:
    """Executa o assistente em modo interativo."""
    print("Modo interativo. Digite 'sair' para encerrar.\n")

    # Loop do modo interativo até que o usuário digite 'sair'
    while True:
        try:
            question = input("Você: ").strip()
            if question.lower() == "sair":
                print("Até logo!")
                break
            if not question:
                continue

            # Mostra "Assistente: " imediatamente (flush=True) enquanto processa a resposta
            # Não quebra a linha (end="") para mostrar a resposta na mesma linha
            print("Assistente: ", end="", flush=True)
            response = run_query(assistant, question)
            print(response)
            print()
        # Trata Ctrl+C para encerrar o loop
        except KeyboardInterrupt:
            print("\nAté logo!")
            break


def main():
    parser = argparse.ArgumentParser(description="LLM Assistant com Tool Calling")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Executa suite de testes ao invés do modo interativo",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("LLM Assistant - PoC com Tool Calling")
    print("=" * 60)
    print()

    # Cria o assistente
    try:
        assistant = create_assistant()
    except Exception as e:
        print(f"Erro ao criar assistente: {e}")
        print("Verifique se o arquivo .env está configurado corretamente.")
        sys.exit(1)

    if args.test:
        from src.test_demo import run_demo
        run_demo(assistant, run_query)
    else:
        interactive_mode(assistant)


if __name__ == "__main__":
    main()