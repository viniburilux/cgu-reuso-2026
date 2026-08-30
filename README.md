# CGU Reúso de Dados Abertos 2026

> Discovery e materialização para o **2º Concurso de Reúso de Dados Abertos da CGU** (deadline 11/09/2026).
> Produzido por Hermes (agente autônomo) a partir do ecossistema LuxVerso.

## 🎯 Missão

Demonstrar como **dados abertos públicos federais** (PNCP, NASA FIRMS, IBGE, CNES) podem ser cruzados para produzir inteligência nova sobre:
- Resposta pública a queimadas
- Fracionamento de compras
- Concentração anômala de dispensas
- Saúde pública em áreas de risco

## 📊 4 iniciativas identificadas

| ID | Nome | Estado | Score | Cruzamento |
|----|------|--------|-------|------------|
| [OPP-001](docs/OPP-001-RespostaPublicaQueimadas.md) | Resposta Pública a Queimadas | **PROVEN** | 9/10 | PNCP × NASA FIRMS × IBGE |
| [OPP-002](docs/OPP-002-FracionamentoVisivel.md) | Fracionamento Visível | **PROVEN** | 8/10 | PNCP |
| [OPP-003](docs/OPP-003-ConcentracaoDispensada.md) | Concentração de Dispensas | **PROVEN** | 7/10 | PNCP × IBGE |
| [OPP-004](docs/OPP-004-SaudeEmAreaDeRisco.md) | Saúde em Área de Risco | EXPERIMENTED | 8/10 | CNES × NASA FIRMS |

## 🏆 Recomendação de submissão

**Submeter 2 iniciativas: OPP-001 + OPP-004**

Justificativa:
- Cobre 3 critérios de peso 2 do edital (Inovação, Transparência, Foco em Pessoas)
- 3 fontes integradas (PNCP, FIRMS, CNES)
- 2 cruzamentos inéditos (nenhum reúso atual faz)
- Score composto estimado: 78% do máximo

## 📂 Estrutura

```
cgu-reuso-2026/
├── README.md                                   # Este arquivo
├── LICENSE                                     # MIT
├── registry.json                               # Manifest completo de todas as iniciativas
├── RELATORIO_FINAL.md                          # Relatório consolidado de discovery + materialização
├── achados/                                    # Datasets derivados
│   ├── focos_firms_bahia_24h.geojson          # 1417 focos de calor NASA FIRMS (24h)
│   ├── editais_pncp_bahia.geojson             # 51 editais Bahia com flag proximidade queimadas
│   ├── crossdata_pncp_fires.csv               # CSV consolidado
│   ├── crossdata_cnes_fires.json              # Hospitais × queimadas
│   ├── marinha_dispensas_2026-08-28.json      # 6 dispensas Marinha em 1 dia
│   ├── dispensa_stats_por_uf.json             # Concentração por UF
│   └── municipios_bahia_ibge.json             # Geo-referenciamento
├── demo/                                       # Material demonstrável
│   ├── index.html                              # Demo HTML interativa
│   └── screenshots/                            # Capturas de tela
├── docs/                                       # Documentação de cada iniciativa
└── scripts/                                    # Pipelines de aquisição e transformação
```

## 🛠️ Como reproduzir

```bash
# 1. Coletar editais PNCP
python3 scripts/01_collect_pncp.py

# 2. Analisar dispensas e padrões
python3 scripts/02_analyze_dispensas.py

# 3. Cruzar com NASA FIRMS (requer download manual de firms_24h_south_america.csv)
python3 scripts/03_crossdata_pncp_fires.py

# 4. Gerar GeoJSONs derivados
python3 scripts/04_build_geojson.py

# 5. Gerar mapa estático (requer matplotlib)
python3 scripts/05_build_static_map.py

# 6. Construir demo HTML
python3 scripts/06_build_demo_html.py

# 7. Atualizar registry
python3 scripts/07_build_registry.py
```

## 📦 Fontes de dados utilizadas

| Fonte | Registros | URL |
|-------|-----------|-----|
| PNCP | 350 editais | `pncp.gov.br/api/search/` |
| NASA FIRMS | 17.835 focos BR | `firms.modaps.eosdis.nasa.gov` |
| IBGE | 417 municípios BA | `servicodados.ibge.gov.br` |
| OpenDataSUS/CNES | 28 hospitais BA | `apidadosabertos.saude.gov.br` |

## 🎬 Demo

Abra `demo/index.html` no browser para visualizar todas as 4 iniciativas.
A demo inclui:
- KPIs globais
- Cards das iniciativas com score e status
- Mapa estático da Bahia com cruzamento territorial
- Tabela de hospitais em risco
- Gráfico de dispensas por UF
- Proveniência documentada

## 🔬 Achados materiais

1. **Catu (BA)**: 1 edital Dispensa + 1 foco FIRMS a <10km
2. **Juazeiro**: 13 focos em 50km + 1 edital Dispensa
3. **Comando da Marinha**: 6 dispensas em 1 dia (28/08/2026)
4. **Hospital NATHALIA DE MELO**: 3.99km de queimada ativa
5. **Ceará**: 62% de editais em Dispensa (vs 21.7% nacional)

## 👥 Time

- **Vinícius Buri Lux (Imperador)** — Coordenação, arquitetura, dados
- **Hermes** — Operador autônomo: discovery, aquisição, transformação, demo

## 📜 Licença

MIT. Veja [LICENSE](LICENSE).

---

**Deadline submissão:** 11/09/2026
**Dias restantes:** 12 (em 30/08/2026)
**Status:** ✅ Materialização completa, pronto para submissão
