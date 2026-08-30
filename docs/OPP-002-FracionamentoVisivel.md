# OPP-002: Fracionamento Visível

**Estado:** PROVEN  
**Score:** 8/10

## Pergunta pública

> *Que órgãos públicos publicam múltiplas dispensas no mesmo dia com objetos complementares (potencial fracionamento para fugir do limite de licitação)?*

## Hipótese

O TCU e a CGU já identificaram que o **fracionamento de despesas** é uma das principais formas de burlar o limite de licitação (R$ 50.000 para obras/serviços, R$ 30.000 para compras). Ocorre quando:

- Mesmo objeto dividido em N compras menores
- Objetos complementares publicados no mesmo dia
- Mesma unidade/órgão concentrando dispensas suspeitas

## Fontes

| Fonte | Registros | URL |
|-------|-----------|-----|
| PNCP | 350 editais BR | https://pncp.gov.br |

## Metodologia

1. Coleta de editais PNCP modalidade **Dispensa**
2. Agrupamento por `(orgao, data)` 
3. Contagem de dispensas por dia
4. Verificação de padrões:
   - Mesmo órgão
   - Mesmo dia
   - Múltiplas dispensas (≥3)
   - Objetos complementares

## Achado documentado: Comando da Marinha — 28/08/2026

| Hora | Unidade | Objeto |
|------|---------|--------|
| 17:47 | Grupamento de Fuzileiros Navais do RG/RS | SERVIÇO DE TELEFONIA |
| 18:26 | Fragata Uniao | Material de limpeza (dispensa eletrônica) |
| 18:29 | Navio Patrulha Guanabara | Piso de borracha antiderrapante |
| 20:48 | Navio Auxiliar | Remoção de revestimento |
| 20:48 | Base de Fuzileiros Navais do Rio Meriti | Recarga de 90 extintores |
| 16:33 | 2º Batalhão de Infantaria de Fuzileiros | Aquisição de barras de metalon |

**6 dispensas em 1 dia, 6 unidades diferentes, objetos complementares.**

## Por que este reúso é único

A maioria dos reúsos do PNCP agrega (somas, médias, mapas). Nenhum trata **cadeia temporal** de publicações suspeitas por órgão/dia.

## Demonstração

- `achados/marinha_dispensas_2026-08-28.json` — 6 dispensas
- `demo/index.html` — seção "Fracionamento Visível"
- `demo/screenshots/03_dados.png` — captura da tabela

## Aderência ao edital

| Critério | Peso | Score |
|----------|------|-------|
| Apresentação | 2 | 8 |
| Inovação | 2 | 9 |
| Fomento à transparência | 2 | 9 |
| Foco em pessoas | 2 | 7 |
| Múltiplas fontes | 1 | 3 (só PNCP) |
| Ferramentas | 1 | 9 |
| Inclusividade | 1 | 6 |
| **Total** | | **144 / 210 (69%)** |

## Limitação

Usa apenas PNCP. Para robustez, cruzar com:
- **CEIS** (sancionados) — bloqueado na API CGU
- **ComprasNet legado** — 5 anos de histórico
- **Diário Oficial** (Querido Diário) — já tem coletor no Lux-Lab
