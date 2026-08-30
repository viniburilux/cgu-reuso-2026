# OPP-003: Concentração de Dispensas por UF

**Estado:** PROVEN  
**Score:** 7/10

## Pergunta pública

> *Que Unidades da Federação têm concentração anormal de dispensas em relação à média nacional?*

## Hipótese

A média nacional de dispensas varia entre 18-25% das compras públicas. UFs com percentual muito acima (≥40%) podem indicar:
- Cultura de não-licitação
- Problemas sistêmicos de governança
- Fraqueza em controle interno

## Fontes

| Fonte | Registros | URL |
|-------|-----------|-----|
| PNCP | 350 editais BR | https://pncp.gov.br |
| IBGE | UFs | https://servicodados.ibge.gov.br |

## Metodologia

1. Coleta de editais PNCP (todas as UFs)
2. Contagem por UF e modalidade
3. Cálculo: `%_dispensa = dispensas / total * 100`
4. Comparação com média nacional
5. Identificação de outliers

## Achados

**Média nacional: 21.7% de editais em modalidade Dispensa**

| UF | Total | Dispensas | % | Anomalia |
|----|-------|-----------|---|----------|
| CE | 8 | 5 | 62% | 🔴 ALTA |
| RJ | 14 | 8 | 57% | 🔴 ALTA |
| GO | 12 | 6 | 50% | 🔴 ALTA |
| PR | 25 | 8 | 32% | ⚠️ Média-alta |
| DF | 16 | 5 | 31% | ⚠️ Média-alta |
| PE | 11 | 3 | 27% | OK |
| MG | 27 | 6 | 22% | OK |
| BA | 51 | 9 | 18% | OK |
| SP | 40 | 6 | 15% | OK |
| RS | 56 | 7 | 12% | OK |

## Por que este reúso é único

- Identifica **anomalias geográficas** em compras públicas
- Lista de UFs com alta concentração pode ser insumo para auditoria
- Pode ser estendido para **concentração por fornecedor** (HHI)

## Limitação crítica

Amostra é pequena (350 editais = snapshot de editais ativos). Para robustez:
- Coletar 12 meses de histórico
- Cruzar com receita orçada (SICONFI — atualmente bloqueado)

## Aderência ao edital

| Critério | Peso | Score |
|----------|------|-------|
| Apresentação | 2 | 7 |
| Inovação | 2 | 7 |
| Fomento à transparência | 2 | 8 |
| Foco em pessoas | 2 | 6 |
| Múltiplas fontes | 1 | 5 |
| Ferramentas | 1 | 7 |
| Inclusividade | 1 | 7 |
| **Total** | | **128 / 210 (61%)** |

## Por que NÃO submeter isoladamente

Tema importante mas mais granular. **Recomendado como parte de portfólio** maior (junto com OPP-001 e OPP-004) ou como material de apoio.
