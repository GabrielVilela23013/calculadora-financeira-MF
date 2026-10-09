import math
from decimal import Decimal, ROUND_HALF_UP

# Calculadora Financeira - Capitalização Simples e Composta
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



# ---------------------------------------------------------------------------
# Segunda parte: capitalização composta
# Convenção comercial: 1 mês = 30 dias; 1 semestre = 180; 1 ano = 360.
# Os cálculos usam taxas EFETIVAS equivalentes entre períodos.
# ---------------------------------------------------------------------------
DIAS_POR_UNIDADE_COMPOSTA = {
    "dia": 1,
    "mes": 30,
    "semestre": 180,
    "ano": 360,
}


def ler_unidade_composta(mensagem):
    """Aceita períodos para taxas e tempos de capitalização composta."""
    aliases = {
        "dia": "dia", "dias": "dia",
        "mes": "mes", "mês": "mes", "meses": "mes",
        "semestre": "semestre", "semestres": "semestre",
        "ano": "ano", "anos": "ano",
    }
    while True:
        unidade = input(mensagem + " [dia/mes/semestre/ano]: ").strip().lower()
        if unidade in aliases:
            return aliases[unidade]
        print("Unidade inválida. Use dia, mes, semestre ou ano.")


def ler_inteiro_positivo(mensagem):
    while True:
        valor = input(mensagem).strip()
        try:
            numero = int(valor)
            if numero > 0:
                return numero
        except ValueError:
            pass
        print("Digite um número inteiro maior que zero.")


def validar_positivo(numero, nome):
    if not math.isfinite(numero) or numero <= 0:
        raise ValueError(f"{nome} deve ser maior que zero e finito.")


def validar_tempo_composto(n):
    if not math.isfinite(n) or n < 0:
        raise ValueError("O tempo deve ser maior ou igual a zero e finito.")


def validar_taxa_composta(taxa_decimal):
    if not math.isfinite(taxa_decimal) or taxa_decimal <= -1:
        raise ValueError("A taxa deve ser maior que -100% e finita.")


def converter_tempo_composto(n, origem, destino):
    validar_tempo_composto(n)
    return n * DIAS_POR_UNIDADE_COMPOSTA[origem] / DIAS_POR_UNIDADE_COMPOSTA[destino]


def converter_taxa_composta(taxa_decimal, origem, destino):
    """Taxas efetivas equivalentes: i_dest = (1+i_orig)^(dias_dest/dias_orig)-1."""
    validar_taxa_composta(taxa_decimal)
    expoente = DIAS_POR_UNIDADE_COMPOSTA[destino] / DIAS_POR_UNIDADE_COMPOSTA[origem]
    return math.expm1(expoente * math.log1p(taxa_decimal))


def calcular_montante_composto(vp, taxa_decimal, unidade_taxa, n, unidade_tempo):
    """VF = VP*(1+i)^n, com n convertido para a unidade da taxa."""
    validar_positivo(vp, "O capital (VP)")
    validar_taxa_composta(taxa_decimal)
    n_ajustado = converter_tempo_composto(n, unidade_tempo, unidade_taxa)
    return vp * math.exp(n_ajustado * math.log1p(taxa_decimal))


def calcular_capital_composto(vf, taxa_decimal, unidade_taxa, n, unidade_tempo):
    """VP = VF/(1+i)^n."""
    validar_positivo(vf, "O montante (VF)")
    validar_taxa_composta(taxa_decimal)
    n_ajustado = converter_tempo_composto(n, unidade_tempo, unidade_taxa)
    return vf * math.exp(-n_ajustado * math.log1p(taxa_decimal))


def calcular_juros_compostos(vp, taxa_decimal, unidade_taxa, n, unidade_tempo):
    """J = VP*[(1+i)^n - 1]."""
    validar_positivo(vp, "O capital (VP)")
    validar_taxa_composta(taxa_decimal)
    n_ajustado = converter_tempo_composto(n, unidade_tempo, unidade_taxa)
    return vp * math.expm1(n_ajustado * math.log1p(taxa_decimal))


def calcular_taxa_composta(vp, vf, n, unidade_tempo, unidade_saida):
    """i = (VF/VP)^(1/n)-1, depois converte para taxa equivalente."""
    validar_positivo(vp, "O capital (VP)")
    validar_positivo(vf, "O montante (VF)")
    validar_tempo_composto(n)
    if n == 0:
        raise ValueError("Para calcular a taxa, o tempo deve ser maior que zero.")
    i_na_unidade_tempo = math.expm1(math.log(vf / vp) / n)
    return converter_taxa_composta(i_na_unidade_tempo, unidade_tempo, unidade_saida)


def calcular_tempo_composto(vp, vf, taxa_decimal, unidade_taxa, unidade_saida):
    """n = log(VF/VP) / log(1+i), depois converte a unidade de tempo."""
    validar_positivo(vp, "O capital (VP)")
    validar_positivo(vf, "O montante (VF)")
    validar_taxa_composta(taxa_decimal)
    if taxa_decimal == 0:
        raise ValueError("Com taxa zero não há tempo único calculável.")
    n_na_unidade_taxa = math.log(vf / vp) / math.log1p(taxa_decimal)
    if n_na_unidade_taxa < -1e-10:
        raise ValueError("Dados incompatíveis: o tempo calculado seria negativo.")
    return converter_tempo_composto(max(0.0, n_na_unidade_taxa), unidade_taxa, unidade_saida)


def nominal_para_proporcional(taxa_nominal_decimal, k):
    """Taxa nominal do período / k = efetiva por subperíodo de capitalização."""
    if not math.isfinite(taxa_nominal_decimal):
        raise ValueError("A taxa nominal deve ser finita.")
    if not isinstance(k, int) or k <= 0:
        raise ValueError("k deve ser inteiro maior que zero.")
    resultado = taxa_nominal_decimal / k
    validar_taxa_composta(resultado)
    return resultado


def proporcional_para_nominal(taxa_proporcional_decimal, k):
    """Taxa efetiva do subperíodo * k = taxa nominal do período maior."""
    validar_taxa_composta(taxa_proporcional_decimal)
    if not isinstance(k, int) or k <= 0:
        raise ValueError("k deve ser inteiro maior que zero.")
    return taxa_proporcional_decimal * k


def formatar_reais(valor):
    """Arredonda centavos pelo critério financeiro (meio centavo para cima)."""
    if not math.isfinite(valor):
        raise ValueError("O resultado financeiro deve ser um número finito.")
    arredondado = Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{arredondado:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")


def ler_taxa_composta():
    i = percentual_para_decimal(ler_numero("Taxa efetiva (i) em %: "))
    unidade_taxa = ler_unidade_composta("Unidade da taxa")
    return i, unidade_taxa


def ler_tempo_composto():
    n = ler_numero("Tempo (n): ")
    unidade_tempo = ler_unidade_composta("Unidade do tempo")
    return n, unidade_tempo


def mostrar_menu_composto():
    print("\n" + "=" * 58)
    print(" JUROS COMPOSTOS - 2ª PARTE")
    print("=" * 58)
    print("1 - Calcular Capital / Valor Presente (VP)")
    print("2 - Calcular Montante / Valor Futuro (VF)")
    print("3 - Calcular Juros Compostos (J)")
    print("4 - Calcular Taxa Efetiva (i)")
    print("5 - Calcular Tempo (n)")
    print("6 - Taxa Nominal -> Proporcional (por capitalização)")
    print("7 - Taxa Proporcional -> Nominal")
    print("8 - Converter Taxas Efetivas Equivalentes")
    print("0 - Voltar ao menu principal")
    print("=" * 58)


def menu_composto():
    print("\nJuros compostos: 1 mês = 30 dias; 1 semestre = 180 dias; 1 ano = 360 dias.")
    print("Digite taxas como porcentagem: 2 significa 2% (não 0,02%).")
    while True:
        mostrar_menu_composto()
        opcao = input("Escolha uma opção: ").strip()
        try:
            if opcao == "0":
                return

            elif opcao == "1":
                print("\n--- Capital (VP) - Juros Compostos ---")
                vf = ler_numero("Montante (VF): R$ ")
                taxa, unidade_taxa = ler_taxa_composta()
                n, unidade_tempo = ler_tempo_composto()
                vp = calcular_capital_composto(vf, taxa, unidade_taxa, n, unidade_tempo)
                print(f"\nCapital (VP) = R$ {formatar_reais(vp)}")

            elif opcao == "2":
                print("\n--- Montante (VF) - Juros Compostos ---")
                vp = ler_numero("Capital (VP): R$ ")
                taxa, unidade_taxa = ler_taxa_composta()
                n, unidade_tempo = ler_tempo_composto()
                vf = calcular_montante_composto(vp, taxa, unidade_taxa, n, unidade_tempo)
                print(f"\nMontante (VF) = R$ {formatar_reais(vf)}")

            elif opcao == "3":
                print("\n--- Juros (J) - Capitalização Composta ---")
                vp = ler_numero("Capital (VP): R$ ")
                taxa, unidade_taxa = ler_taxa_composta()
                n, unidade_tempo = ler_tempo_composto()
                juros = calcular_juros_compostos(vp, taxa, unidade_taxa, n, unidade_tempo)
                print(f"\nJuros (J) = R$ {formatar_reais(juros)}")

            elif opcao == "4":
                print("\n--- Taxa (i) - Juros Compostos ---")
                vp = ler_numero("Capital (VP): R$ ")
                vf = ler_numero("Montante (VF): R$ ")
                n, unidade_tempo = ler_tempo_composto()
                unidade_saida = ler_unidade_composta("Período da taxa desejada")
                taxa = calcular_taxa_composta(vp, vf, n, unidade_tempo, unidade_saida)
                print(f"\nTaxa efetiva (i) = {decimal_para_percentual(taxa):.6f}% por {unidade_saida}")

            elif opcao == "5":
                print("\n--- Tempo (n) - Juros Compostos ---")
                vp = ler_numero("Capital (VP): R$ ")
                vf = ler_numero("Montante (VF): R$ ")
                taxa, unidade_taxa = ler_taxa_composta()
                unidade_saida = ler_unidade_composta("Unidade desejada para o tempo")
                n = calcular_tempo_composto(vp, vf, taxa, unidade_taxa, unidade_saida)
                print(f"\nTempo (n) = {n:.6f} {unidade_saida}(s)")

            elif opcao == "6":
                print("\n--- Taxa Nominal -> Proporcional (Efetiva por Capitalização) ---")
                nominal = percentual_para_decimal(ler_numero("Taxa nominal (ik) em %: "))
                k = ler_inteiro_positivo("Número de capitalizações no período nominal (k): ")
                taxa = nominal_para_proporcional(nominal, k)
                print(f"\nTaxa por capitalização = {decimal_para_percentual(taxa):.6f}%")
                print("Exemplo: nominal anual e k=12 -> taxa efetiva mensal.")

            elif opcao == "7":
                print("\n--- Taxa Proporcional (por Capitalização) -> Nominal ---")
                prop = percentual_para_decimal(ler_numero("Taxa efetiva por capitalização em %: "))
                k = ler_inteiro_positivo("Número de capitalizações no período nominal (k): ")
                taxa = proporcional_para_nominal(prop, k)
                print(f"\nTaxa nominal do período = {decimal_para_percentual(taxa):.6f}%")

            elif opcao == "8":
                print("\n--- Taxas Efetivas Equivalentes ---")
                taxa = percentual_para_decimal(ler_numero("Taxa efetiva inicial em %: "))
                origem = ler_unidade_composta("Período da taxa atual")
                destino = ler_unidade_composta("Período da taxa desejada")
                taxa_convertida = converter_taxa_composta(taxa, origem, destino)
                print(f"\nTaxa equivalente = {decimal_para_percentual(taxa_convertida):.6f}% por {destino}")

            else:
                print("\nOpção inválida. Escolha uma opção de 0 a 8.")

        except (ValueError, OverflowError, ZeroDivisionError) as erro:
            print(f"\nErro: {erro}")


def mostrar_menu_simples():
    print("\n" + "=" * 58)
    print(" JUROS SIMPLES - 1ª PARTE")
    print("=" * 58)
    print("1 - Calcular Capital / Valor Presente (VP)")
    print("2 - Calcular Montante / Valor Futuro (VF)")
    print("3 - Calcular Juros (J)")
    print("4 - Calcular Taxa (i)")
    print("5 - Calcular Tempo (n)")
    print("6 - Converter taxa entre dia, mês e ano")
    print("7 - Desconto comercial (ic) -> Taxa efetiva (i)")
    print("8 - Taxa efetiva (i) -> Desconto comercial (ic)")
    print("0 - Voltar ao menu principal")
    print("=" * 58)


def menu_simples():
    print("\nJuros simples: 1 mês = 30 dias e 1 ano = 360 dias.")
    print("Digite as taxas em porcentagem. Ex.: 2 para 2%.")

    while True:
        mostrar_menu_simples()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "0":
                return

            elif opcao == "1":
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
                print(f"\nCapital (VP) = R$ {formatar_reais(vp)}")

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
                print(f"\nMontante (VF) = R$ {formatar_reais(vf)}")

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
                print(f"\nJuros (J) = R$ {formatar_reais(juros)}")

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

            else:
                print("\nOpção inválida. Escolha uma opção de 0 a 8.")

        except ValueError as erro:
            print(f"\nErro: {erro}")


def mostrar_menu_principal():
    print("\n" + "=" * 58)
    print(" CALCULADORA FINANCEIRA")
    print("=" * 58)
    print("1 - Juros Simples (1ª Parte)")
    print("2 - Juros Compostos (2ª Parte)")
    print("0 - Sair da Calculadora")
    print("=" * 58)


def main():
    """Seleciona a modalidade; cada submenu permite voltar para cá."""
    while True:
        mostrar_menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_simples()
        elif opcao == "2":
            menu_composto()
        elif opcao == "0":
            print("\nPrograma encerrado.")
            return
        else:
            print("\nOpção inválida. Escolha 0, 1 ou 2.")


if __name__ == "__main__":
    main()
