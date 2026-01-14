"""Suite de testes de demonstração para capacidades do assistente e proteção contra hallucination."""

DEMO_QUESTIONS = [
    # =====================================================
    # TESTES DE FUNCIONAMENTO NORMAL
    # =====================================================
    {
        "question": "Quem foi Albert Einstein?",
        "expected_tool": None,
        "description": "Conhecimento geral - deve responder diretamente sem usar ferramentas",
    },
    {
        "question": "Quanto é 128 vezes 46?",
        "expected_tool": "calculator",
        "description": "Cálculo matemático - deve usar a ferramenta calculator",
    },
    {
        "question": "Qual a raiz quadrada de 144 mais 25?",
        "expected_tool": "calculator",
        "description": "Matemática com raiz quadrada - deve usar a ferramenta calculator",
    },
    {
        "question": "Como está o clima em Londres?",
        "expected_tool": "get_weather",
        "description": "Consulta de clima - deve usar a ferramenta get_weather",
    },
    {
        "question": "Qual era o preço do Bitcoin em 15 de janeiro de 2024?",
        "expected_tool": "get_crypto_price",
        "description": "Preço histórico de criptomoeda - deve usar a ferramenta get_crypto_price",
    },
    # =====================================================
    # TESTES DE HALLUCINATION - Casos inválidos/inventados
    # =====================================================
    {
        "question": "Quem foi Joãozinho da Silva Sauro, o famoso cientista brasileiro que inventou a teletransportação em 1823?",
        "expected_tool": None,
        "description": "[HALLUCINATION] Pessoa fictícia - deve reconhecer que não existe",
    },
    {
        "question": "Como está o clima em Huskavarita?",
        "expected_tool": "get_weather",
        "description": "[HALLUCINATION] Cidade completamente inventada - deve informar que não encontrou",
    },
    {
        "question": "Qual era o preço do INVALIDCOIN123USDT em 20 de março de 2024?",
        "expected_tool": "get_crypto_price",
        "description": "[HALLUCINATION] Criptomoeda inventada com ticker explícito - deve informar erro da API",
    },
    {
        "question": "Quanto é 10 dividido por 0?",
        "expected_tool": "calculator",
        "description": "[HALLUCINATION] Divisão por zero - deve explicar que é impossível",
    },
]


def run_demo(assistant, run_query_fn) -> None:
    """Executa a suite de testes de demonstração.

    Args:
        assistant: Instância do agente LangGraph.
        run_query_fn: Função para executar consultas no agente.
    """
    total = len(DEMO_QUESTIONS)
    hallucination_tests = sum(1 for t in DEMO_QUESTIONS if "[HALLUCINATION]" in t["description"])
    normal_tests = total - hallucination_tests

    print("Executando suite de testes de demonstração...\n")
    print(f"Total de testes: {total}")
    print(f"  - Testes normais: {normal_tests}")
    print(f"  - Testes de hallucination: {hallucination_tests}")
    print("\n" + "=" * 60)

    for i, test in enumerate(DEMO_QUESTIONS, 1):
        is_hallucination = "[HALLUCINATION]" in test["description"]
        test_type = "HALLUCINATION" if is_hallucination else "NORMAL"

        print(f"\nTeste {i}/{total} [{test_type}]: {test['description']}")
        print("-" * 60)
        print(f"Pergunta: {test['question']}")

        if test["expected_tool"]:
            print(f"Ferramenta esperada: {test['expected_tool']}")
        else:
            print("Ferramenta esperada: Nenhuma (resposta direta)")

        print()

        try:
            response = run_query_fn(assistant, test["question"])
            print(f"\nAssistente: {response}")
        except Exception as e:
            print(f"\nErro: {e}")

        print("\n" + "=" * 60)

    print("\nDemonstração concluída!")
    print(f"\nResumo: {total} testes executados ({normal_tests} normais, {hallucination_tests} de hallucination)")
