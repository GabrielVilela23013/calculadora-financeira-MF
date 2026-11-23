# Calculadora Financeira — Juros, Amortização e VPL

Projeto em **Python 3**, com menu interativo no terminal, desenvolvido para a disciplina de Matemática Financeira.

## Menu principal

```text
CALCULADORA FINANCEIRA
1 - Juros Simples (1ª Parte)
2 - Juros Compostos (2ª Parte)
3 - Amortização e VPL (3ª Parte)
0 - Sair da Calculadora
```

## Funcionalidades

### Menu 1 — Juros Simples (1ª Parte, preservada)

1. Calcular capital / valor presente (VP).
2. Calcular montante / valor futuro (VF).
3. Calcular juros (J).
4. Calcular taxa (i).
5. Calcular tempo (n).
6. Converter taxas entre dia, mês e ano (**proporcionalmente**).
7. Converter desconto comercial (ic) em taxa efetiva (i).
8. Converter taxa efetiva (i) em desconto comercial (ic).

### Menu 2 — Juros Compostos (2ª Parte)

1. Calcular capital / valor presente (VP).
2. Calcular montante / valor futuro (VF).
3. Calcular juros compostos (J).
4. Calcular taxa efetiva (i).
5. Calcular tempo (n).
6. Converter taxa nominal em taxa proporcional (efetiva por capitalização).
7. Converter taxa proporcional em taxa nominal.
8. Converter **taxas efetivas equivalentes** entre dia, mês, semestre e ano.

Na Parte 2, ao fazer os cálculos de VP, VF, J, taxa e tempo, é possível informar a taxa e o tempo em períodos diferentes: a calculadora converte esses períodos automaticamente.

### Menu 3 — Amortização e VPL (3ª Parte)

1. **Sistema de Amortização Constante (SAC).** Informe o financiamento, a taxa efetiva, a frequência das prestações e o número de parcelas de amortização. A calculadora converte a taxa para a frequência das prestações e exibe amortização, juros pagos, prestação e saldo devedor após cada período, além dos totais.
2. **Valor Presente Líquido (VPL).** Informe o investimento inicial como valor positivo, a taxa de desconto por período e os fluxos de caixa a partir do período 1. Use zero para períodos sem movimento e valores negativos para saídas. Se houver valor residual, informe o valor e seu período, que pode ser posterior ao último fluxo.

No SAC, a amortização teórica é o saldo a amortizar dividido pelo número de prestações. Os juros incidem sobre o saldo anterior e a prestação soma juros e amortização. A tabela distribui as diferenças de arredondamento da amortização ao longo das parcelas para que o saldo final feche em zero.

O número de prestações informado no SAC começa após a carência. Informe a duração da carência na mesma unidade das parcelas. As modalidades seguem os slides de Amortização:

- **Sem carência.** A amortização começa no primeiro período.
- **Juros pagos durante a carência.** Cada pagamento nessa etapa cobre os juros do período.
- **Juros pagos na primeira prestação.** Os juros acumulam durante a carência e são quitados junto com os juros do período e a primeira amortização.
- **Juros incorporados ao saldo.** O saldo atualizado ao fim da carência é dividido pelas parcelas de amortização.

O VPL soma os fluxos descontados pela taxa informada e subtrai o investimento inicial. Se houver valor residual, ele também é descontado pelo seu próprio período.

## Fórmulas — capitalização composta

A taxa `i` é usada em decimal, por exemplo, **8% = 0,08**. O prazo `n` precisa estar na mesma unidade da taxa.

- Montante: `VF = VP × (1 + i)^n`
- Capital: `VP = VF / (1 + i)^n`
- Juros: `J = VP × [(1 + i)^n − 1]`
- Taxa: `i = (VF / VP)^(1/n) − 1`
- Tempo: `n = log(VF / VP) / log(1 + i)`
- Nominal para proporcional: `i_proporcional = i_nominal / k`
- Proporcional para nominal: `i_nominal = i_proporcional × k`
- Taxas equivalentes: `i_destino = (1 + i_origem)^(D_destino / D_origem) − 1`, com `D` em dias convencionais.

**Atenção:** taxa nominal anual de 24%, capitalizada 12 vezes ao ano, corresponde a **2% efetivos por mês**, mas **não** a 24% efetivos ao ano. A taxa anual efetiva equivalente seria `(1,02)^12 − 1` ≈ **26,8242%**.

## Convenções

- 1 mês = 30 dias;
- 1 semestre = 180 dias;
- 1 ano = 360 dias;
- os números podem ser digitados com vírgula ou ponto como separador decimal;
- as taxas são informadas em **porcentagem**: digite `8` para 8%, e não `0,08`.

## Como executar no Windows

1. Abra a pasta do projeto, que contém o arquivo `calculadora.py`.
2. Clique na barra de endereço do Explorador de Arquivos, digite `powershell` e pressione Enter.
3. Execute:

```powershell
py calculadora.py
```

Se o comando `py` não estiver disponível, tente `python calculadora.py` (com Python 3 instalado).

4. Escolha **1 — Juros Simples**, **2 — Juros Compostos** ou **3 — Amortização e VPL**.
5. Selecione a operação no submenu. Use **0** para voltar ao menu principal ou sair da calculadora quando estiver no menu principal.

## Exemplo de teste

No menu principal, escolha `2` (juros compostos); no submenu, escolha `2` (montante). Informe:

- VP = `4000`
- i = `8`, por `mes`
- n = `6`, em `mes`

O resultado esperado é **R$ 6.347,50**.

## Exemplos da Parte 3

- **SAC.** No menu `3 > 1`, informe R$ 8.000,00 a 5% ao mês em 4 prestações mensais, sem carência. A primeira prestação é de **R$ 2.400,00**, a última é de **R$ 2.100,00** e o saldo final é zero.
- **VPL.** No menu `3 > 2`, informe investimento de R$ 1.000,00, taxa de 10% por período, fluxos de R$ 500,00 e R$ 700,00 nos períodos 1 e 2, e residual de R$ 100,00 no período 3. O VPL é **R$ 108,19**.

## Tecnologias

Python 3, Git e GitHub. Nenhuma dependência externa é necessária.

**Arredondamento monetário:** resultados em reais são exibidos com dois centavos, arredondando o meio centavo para cima (por exemplo, R$ 1.050,625 é exibido como R$ 1.050,63).
