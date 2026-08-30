# OPP-004: Saúde em Área de Risco

**Estado:** EXPERIMENTED  
**Score:** 8/10

## Pergunta pública

> *Hospitais públicos da Bahia estão em áreas com queimadas ativas?*

## Hipótese

A capacidade de saúde pública (hospitais, UPAs, UBS) pode ser comprometida por eventos ambientais extremos como queimadas. Identificar hospitais próximos a focos ativos é fundamental para:
- Preparação de emergência
- Logística de pacientes respiratórios
- Acionamento de planos de contingência

## Fontes

| Fonte | Registros | URL |
|-------|-----------|-----|
| OpenDataSUS/CNES | 28 hospitais BA com coord | https://apidadosabertos.saude.gov.br |
| NASA FIRMS | 1.417 focos BA (24h) | https://firms.modaps.eosdis.nasa.gov |

## Metodologia

1. Coleta de hospitais CNES com coordenadas (BA, 28 registros)
2. Coleta de focos NASA FIRMS (24h)
3. Para cada hospital, calcular:
   - Focos em 5km
   - Focos em 10km
   - Distância ao foco mais próximo
4. Classificar:
   - **ALERTA** (focos <5km)
   - **AVISO** (focos <10km)
   - **OK**

## Achado

| Hospital | Tipo | Focos 5km | Focos 10km | Flag |
|----------|------|-----------|------------|------|
| NATHALIA DE MELO GUIMARAES | 22 | 1 | 1 | **ALERTA** |
| USF DO JARDIM VALERIA III | 22 | 0 | 3 | AVISO |
| IGO MEDICINA ESPECIALIZADA | 22 | 0 | 2 | AVISO |

**Caso crítico:** Hospital NATHALIA DE MELO GUIMARAES, município 316935, está a **3.99 km de um foco de calor ativo**.

## Por que este reúso é único

Cruza **saúde pública** com **eventos ambientais em tempo real**. Nenhum reúso do CNES faz esse cruzamento.

## Limitação crítica

API do OpenDataSUS está com bug de paginação (retorna apenas 20-300 registros por UF). Para robustez, seria necessário:
- Coletar via DATASUS direto (FTP mensal)
- Ou esperar correção da API
- **Hoje a base é 28 hospitais — amostra pequena mas válida como prova de conceito**

## Próximos passos

1. Coletar via DATASUS CSV (rodar mensalmente)
2. Cruzar com SESAB (Secretaria Saúde BA) para validar
3. Adicionar tipo de atendimento (urgência, internação)
4. Gerar alerta em tempo real

## Aderência ao edital

| Critério | Peso | Score |
|----------|------|-------|
| Apresentação | 2 | 8 |
| Inovação | 2 | 9 |
| Fomento à transparência | 2 | 7 |
| **Foco em pessoas** | 2 | **10** |
| Múltiplas fontes | 1 | 9 |
| Ferramentas | 1 | 8 |
| Inclusividade | 1 | 7 |
| **Total** | | **170 / 210 (81%)** |

## Destaque

**Esta é a iniciativa que cobre o critério "Foco em pessoas" (peso 2)** que as outras não cobrem diretamente. Por isso, **é recomendada para submissão junto com OPP-001**.
