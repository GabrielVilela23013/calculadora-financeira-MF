# Calculadora Financeira — Capitalização Simples e Composta

Projeto em **Python 3**, com menu interativo no terminal, desenvolvido para a disciplina de Matemática Financeira.

## Menu principal

```text
CALCULADORA FINANCEIRA
1 - Juros Simples (1ª Parte)
2 - Juros Compostos (2ª Parte)
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

4. No menu principal, escolha **1 — Juros Simples (1ª Parte)** ou **2 — Juros Compostos (2ª Parte)**.
5. Dentro de cada modalidade, escolha uma das 8 operações. Use **0** no submenu para voltar ao menu principal, ou **0** no menu principal para sair.

## Exemplo de teste

No menu principal, escolha `2` (juros compostos); no submenu, escolha `2` (montante). Informe:

- VP = `4000`
- i = `8`, por `mes`
- n = `6`, em `mes`

O resultado esperado é **R$ 6.347,50**.

## Testes automáticos

Na pasta do projeto, execute (inclui a verificação das 16 operações pelo menu):

```powershell
py -m unittest -v test_calculadora.py
```

Os testes usam somente bibliotecas padrão do Python, sem instalação de pacotes adicionais.

## Tecnologias

Python 3, Git e GitHub. Nenhuma dependência externa é necessária.

**Arredondamento monetário:** resultados em reais são exibidos com dois centavos, arredondando o meio centavo para cima (por exemplo, R$ 1.050,625 é exibido como R$ 1.050,63).
