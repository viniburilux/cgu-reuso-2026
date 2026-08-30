# OPP-001: Resposta Pública a Queimadas

**Estado:** PROVEN  
**Score:** 9/10  
**Deadline:** 11/09/2026

## Pergunta pública

> *Quanto e como o poder público está comprando em municípios com queimadas ativas?*

## Hipótese

Estados e municípios com queimadas ativas publicam compras públicas emergenciais (via Dispensa) para combate a incêndios, reparos, etc. Cruzando editais PNCP com focos de calor NASA FIRMS em tempo real, identificamos:

- **Editais ALERTA** (a <10km de foco ativo): possíveis contratações emergenciais
- **Editais AVISO** (a <50km): contratações relacionadas a contexto de queimada
- **Editais OK** (sem proximidade): baseline de compra normal

## Fontes

| Fonte | Registros | URL |
|-------|-----------|-----|
| PNCP | 51 editais Bahia | https://pncp.gov.br |
| NASA FIRMS | 1.417 focos BA (24h) | https://firms.modaps.eosdis.nasa.gov |
| IBGE | 417 municípios BA | https://servicodados.ibge.gov.br |

## Metodologia

1. Coleta de editais PNCP Bahia (status `recebendo_proposta`)
2. Coleta de focos NASA FIRMS (24h rolling) — `J1_VIIRS_C2_South_America_24h.csv`
3. Para cada edital, calcular distância ao foco mais próximo (haversine)
4. Classificar:
   - ALERTA: foco < 10km
   - AVISO: foco < 50km
   - OK: sem proximidade
5. Gerar GeoJSON com 51 features (uma por edital)
6. Visualizar em mapa

## Achados quantificados

- **51 editais BA** analisados
- **1.417 focos FIRMS** na Bahia (24h)
- **1 edital em ALERTA**: Catu (1 edital Dispensa + 1 foco a <10km)
- **10 editais em AVISO**: destaque para Juazeiro (13 focos em 50km + 1 edital Dispensa)

## Por que este reúso é único

Nenhum dos reúsos catalogados no dados.gov.br cruza:
- **PNCP** (compras públicas) + 
- **NASA FIRMS** (eventos ambientais em tempo real) + 
- **IBGE** (georreferenciamento municipal)

A maioria dos reúsos faz análise **unidimensional** (tempo OU espaço OU dinheiro). Este cruza as três dimensões com proveniência.

## Demonstração

- `demo/index.html` — visualização interativa
- `achados/editais_pncp_bahia.geojson` — dataset derivado
- `achados/crossdata_pncp_fires.csv` — CSV consolidado
- `demo/screenshots/mapa_estatico.png` — mapa offline

## Limitações conhecidas

- PNCP: API retorna apenas editais ativos com status "recebendo_proposta" (outros status não capturados)
- NASA FIRMS: snapshot 24h, não histórico anual
- Centroides: alguns municípios BA sem coordenada precisa usaram centróide como proxy

## Código reutilizado

- Pipeline `pncp_bahia_intelligence` do Lux-Lab (já existe)
- Raster pipeline do `ghostworks` (TTI Brazil)
- Schemas JSON do Lux-Radar

## Aderência ao edital (2º Concurso CGU)

| Critério | Peso | Score esperado |
|----------|------|----------------|
| Apresentação | 2 | 9 |
| Inovação | 2 | 10 |
| Fomento à transparência | 2 | 8 |
| Foco em pessoas | 2 | 7 |
| Múltiplas fontes | 1 | 10 |
| Ferramentas tecnológicas | 1 | 8 |
| Inclusividade | 1 | 6 |
| **Total ponderado** | | **172 / 210 (82%)** |

## Próximos passos

1. Expandir para histórico (12 meses) — sazonalidade
2. Adicionar INPE Queimadas histórico (vs FIRMS tempo real)
3. Cruzar com Diário Oficial (menções a combate a incêndios)
4. Validar caso Catu manualmente
