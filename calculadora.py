# Calculadora Financeira - Capitalização Simples
# Convenção adotada: 1 mês = 30 dias e 1 ano = 360 dias.

DIAS_POR_UNIDADE = {
    "dia": 1,
    "mes": 30,
    "ano": 360
}


def ler_numero(mensagem):
    """Lê um número aceitando vírgula ou ponto como separador decimal."""
    while True:
        try:
            return float(input(mensagem).strip().replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número.")


def ler_unidade(mensagem):
    """Lê a unidade de tempo/taxa."""
    while True:
        unidade = input(mensagem + " [dia/mes/ano]: ").strip().lower()

        # Aceita algumas variações com acento/plural.
        aliases = {
            "dia": "dia", "dias": "dia",
            "mes": "mes", "mês": "mes", "meses": "mes",
            "ano": "ano", "anos": "ano"
        }

        if unidade in aliases:
            return aliases[unidade]

        print("Unidade inválida. Use dia, mes ou ano.")


def percentual_para_decimal(taxa_percentual):
    return taxa_percentual / 100


def decimal_para_percentual(taxa_decimal):
    return taxa_decimal * 100


def converter_tempo(valor, unidade_origem, unidade_destino):
    """Converte tempo usando 1 mês = 30 dias e 1 ano = 360 dias."""
    valor_em_dias = valor * DIAS_POR_UNIDADE[unidade_origem]
    return valor_em_dias / DIAS_POR_UNIDADE[unidade_destino]


def converter_taxa_simples(taxa_decimal, unidade_origem, unidade_destino):
    """
    Em juros simples, as taxas são proporcionais.
    Ex.: 2% a.m. = 24% a.a.
    """
    return taxa_decimal * (
        DIAS_POR_UNIDADE[unidade_destino]
        / DIAS_POR_UNIDADE[unidade_origem]
    )


def tempo_na_unidade_da_taxa(n, unidade_tempo, unidade_taxa):
    """Deixa o tempo na mesma unidade da taxa para aplicar i * n."""
    return converter_tempo(n, unidade_tempo, unidade_taxa)


def calcular_capital(vf, taxa_decimal, unidade_taxa, n, unidade_tempo):
    # VP = VF / (1 + i*n)
    n_ajustado = tempo_na_unidade_da_taxa(n, unidade_tempo, unidade_taxa)
    denominador = 1 + taxa_decimal * n_ajustado

    if denominador == 0:
        raise ValueError("Não é possível calcular: 1 + i*n = 0.")

    return vf / denominador


def calcular_montante(vp, taxa_decimal, unidade_taxa, n, unidade_tempo):
    # VF = VP * (1 + i*n)
    n_ajustado = tempo_na_unidade_da_taxa(n, unidade_tempo, unidade_taxa)
    return vp * (1 + taxa_decimal * n_ajustado)


def calcular_juros(vp, taxa_decimal, unidade_taxa, n, unidade_tempo):
    # J = VP * i * n
    n_ajustado = tempo_na_unidade_da_taxa(n, unidade_tempo, unidade_taxa)
    return vp * taxa_decimal * n_ajustado


def calcular_taxa(vp, vf, n, unidade_tempo, unidade_saida):
    # Primeiro calcula a taxa na mesma unidade informada para o tempo:
    # i = (VF/VP - 1) / n
    if vp == 0:
        raise ValueError("O capital (VP) não pode ser zero.")
    if n == 0:
        raise ValueError("O tempo (n) não pode ser zero.")

    taxa_na_unidade_tempo = (vf / vp - 1) / n

    # Depois converte para a unidade de taxa desejada.
    return converter_taxa_simples(
        taxa_na_unidade_tempo,
        unidade_tempo,
        unidade_saida
    )


def calcular_tempo(vp, vf, taxa_decimal, unidade_taxa, unidade_saida):
    # n = (VF/VP - 1) / i
    if vp == 0:
        raise ValueError("O capital (VP) não pode ser zero.")
    if taxa_decimal == 0:
        raise ValueError("A taxa não pode ser zero.")

    n_na_unidade_taxa = (vf / vp - 1) / taxa_decimal
    return converter_tempo(
        n_na_unidade_taxa,
        unidade_taxa,
        unidade_saida
    )


def comercial_para_efetiva(ic_decimal, n, unidade_tempo, unidade_taxa_ic):
    """
    Desconto comercial simples:
        VP = VF * (1 - ic*n)

    Taxa efetiva simples equivalente:
        i = ic / (1 - ic*n)
    """
    n_ajustado = tempo_na_unidade_da_taxa(
        n, unidade_tempo, unidade_taxa_ic
    )

    denominador = 1 - ic_decimal * n_ajustado

    if denominador <= 0:
        raise ValueError(
            "Dados inválidos: é necessário que 1 - ic*n seja maior que zero."
        )

    return ic_decimal / denominador


def efetiva_para_comercial(i_decimal, n, unidade_tempo, unidade_taxa_i):
    """
    Relação inversa:
        ic = i / (1 + i*n)
    """
    n_ajustado = tempo_na_unidade_da_taxa(
        n, unidade_tempo, unidade_taxa_i
    )

    denominador = 1 + i_decimal * n_ajustado

    if denominador == 0:
        raise ValueError("Não é possível calcular: 1 + i*n = 0.")

    return i_decimal / denominador


def mostrar_menu():
    print("\n" + "=" * 58)
    print(" CALCULADORA FINANCEIRA - CAPITALIZAÇÃO SIMPLES")
    print("=" * 58)
    print("1 - Calcular Capital / Valor Presente (VP)")
    print("2 - Calcular Montante / Valor Futuro (VF)")
    print("3 - Calcular Juros (J)")
    print("4 - Calcular Taxa (i)")
    print("5 - Calcular Tempo (n)")
    print("6 - Converter taxa entre dia, mês e ano")
    print("7 - Desconto comercial (ic) -> Taxa efetiva (i)")
    print("8 - Taxa efetiva (i) -> Desconto comercial (ic)")
    print("0 - Sair")
    print("=" * 58)


def main():
    print("Convenção: 1 mês = 30 dias e 1 ano = 360 dias.")
    print("Digite as taxas em porcentagem. Ex.: 2 para 2%.")

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                print("\n--- Calcular Capital (VP) ---")
                vf = ler_numero("Montante (VF): R$ ")
                taxa = percentual_para_decimal(
                    ler_numero("Taxa (i) em %: ")
                )
                unidade_taxa = ler_unidade("Unidade da taxa")
                n = ler_numero("Tempo (n): ")
                unidade_tempo = ler_unidade("Unidade do tempo")

                vp = calcular_capital(
                    vf, taxa, unidade_taxa, n, unidade_tempo
                )
                print(f"\nCapital (VP) = R$ {vp:,.2f}")

            elif opcao == "2":
                print("\n--- Calcular Montante (VF) ---")
                vp = ler_numero("Capital (VP): R$ ")
                taxa = percentual_para_decimal(
                    ler_numero("Taxa (i) em %: ")
                )
                unidade_taxa = ler_unidade("Unidade da taxa")
                n = ler_numero("Tempo (n): ")
                unidade_tempo = ler_unidade("Unidade do tempo")

                vf = calcular_montante(
                    vp, taxa, unidade_taxa, n, unidade_tempo
                )
                print(f"\nMontante (VF) = R$ {vf:,.2f}")

            elif opcao == "3":
                print("\n--- Calcular Juros (J) ---")
                vp = ler_numero("Capital (VP): R$ ")
                taxa = percentual_para_decimal(
                    ler_numero("Taxa (i) em %: ")
                )
                unidade_taxa = ler_unidade("Unidade da taxa")
                n = ler_numero("Tempo (n): ")
                unidade_tempo = ler_unidade("Unidade do tempo")

                juros = calcular_juros(
                    vp, taxa, unidade_taxa, n, unidade_tempo
                )
                print(f"\nJuros (J) = R$ {juros:,.2f}")

            elif opcao == "4":
                print("\n--- Calcular Taxa (i) ---")
                vp = ler_numero("Capital (VP): R$ ")
                vf = ler_numero("Montante (VF): R$ ")
                n = ler_numero("Tempo (n): ")
                unidade_tempo = ler_unidade("Unidade do tempo")
                unidade_saida = ler_unidade(
                    "Unidade desejada para a taxa"
                )

                taxa = calcular_taxa(
                    vp, vf, n, unidade_tempo, unidade_saida
                )
                print(
                    f"\nTaxa (i) = "
                    f"{decimal_para_percentual(taxa):.6f}% por {unidade_saida}"
                )

            elif opcao == "5":
                print("\n--- Calcular Tempo (n) ---")
                vp = ler_numero("Capital (VP): R$ ")
                vf = ler_numero("Montante (VF): R$ ")
                taxa = percentual_para_decimal(
                    ler_numero("Taxa (i) em %: ")
                )
                unidade_taxa = ler_unidade("Unidade da taxa")
                unidade_saida = ler_unidade(
                    "Unidade desejada para o tempo"
                )

                n = calcular_tempo(
                    vp, vf, taxa, unidade_taxa, unidade_saida
                )
                print(f"\nTempo (n) = {n:.6f} {unidade_saida}(s)")

            elif opcao == "6":
                print("\n--- Converter Taxa ---")
                taxa = percentual_para_decimal(
                    ler_numero("Taxa em %: ")
                )
                origem = ler_unidade("Unidade atual da taxa")
                destino = ler_unidade("Converter para")

                taxa_convertida = converter_taxa_simples(
                    taxa, origem, destino
                )
                print(
                    f"\nTaxa convertida = "
                    f"{decimal_para_percentual(taxa_convertida):.6f}% "
                    f"por {destino}"
                )

            elif opcao == "7":
                print("\n--- Taxa Comercial (ic) -> Taxa Efetiva (i) ---")
                ic = percentual_para_decimal(
                    ler_numero("Taxa de desconto comercial (ic) em %: ")
                )
                unidade_ic = ler_unidade("Unidade da taxa ic")
                n = ler_numero("Tempo (n): ")
                unidade_tempo = ler_unidade("Unidade do tempo")
                unidade_saida = ler_unidade(
                    "Unidade desejada para a taxa efetiva"
                )

                i_mesma_unidade = comercial_para_efetiva(
                    ic, n, unidade_tempo, unidade_ic
                )
                i_saida = converter_taxa_simples(
                    i_mesma_unidade, unidade_ic, unidade_saida
                )

                print(
                    f"\nTaxa efetiva (i) = "
                    f"{decimal_para_percentual(i_saida):.6f}% "
                    f"por {unidade_saida}"
                )

            elif opcao == "8":
                print("\n--- Taxa Efetiva (i) -> Taxa Comercial (ic) ---")
                i = percentual_para_decimal(
                    ler_numero("Taxa efetiva (i) em %: ")
                )
                unidade_i = ler_unidade("Unidade da taxa i")
                n = ler_numero("Tempo (n): ")
                unidade_tempo = ler_unidade("Unidade do tempo")
                unidade_saida = ler_unidade(
                    "Unidade desejada para a taxa comercial"
                )

                ic_mesma_unidade = efetiva_para_comercial(
                    i, n, unidade_tempo, unidade_i
                )
                ic_saida = converter_taxa_simples(
                    ic_mesma_unidade, unidade_i, unidade_saida
                )

                print(
                    f"\nTaxa comercial (ic) = "
                    f"{decimal_para_percentual(ic_saida):.6f}% "
                    f"por {unidade_saida}"
                )

            elif opcao == "0":
                print("\nPrograma encerrado.")
                break

            else:
                print("\nOpção inválida. Escolha uma opção de 0 a 8.")

        except ValueError as erro:
            print(f"\nErro: {erro}")


if __name__ == "__main__":
    main()
