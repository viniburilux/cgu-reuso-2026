# 🎯 RELATÓRIO FINAL — Discovery + Materialização CGU 2026

**Data:** 2026-08-30 22:20 UTC
**Duração total:** ~3 horas de execução autônoma
**Status:** ✅ MATERIALIZAÇÃO COMPLETA

---

## 📊 RESUMO EXECUTIVO

A máquina descobriu e materializou **4 iniciativas** baseadas em dados abertos, com **3 em estado PROVEN** e **1 em EXPERIMENTED**, totalizando:
- 350 editais PNCP coletados
- 1417 focos NASA FIRMS (Bahia 24h)
- 28 hospitais CNES Bahia georreferenciados
- 5 datasets derivados reais (2 GeoJSON + CSV + JSON + 1 HTML)
- 1 demo HTML interativa + mapa estático PNG

**Recomendação:** Submeter 2 iniciativas — **OPP-001 (RespostaPublicaQueimadas)** + **OPP-004 (SaudeEmAreaDeRisco)** — por cobrirem os 3 critérios de maior peso do edital e terem material demonstrável.

---

## 🔧 FONTES UTILIZADAS

| Fonte | Status | Registros | URL |
|-------|--------|-----------|-----|
| **PNCP** | ✅ OK | 350 | `pncp.gov.br/api/search/` |
| **NASA FIRMS** | ✅ OK | 17.835 (BR) / 1.417 (BA) | `firms.modaps.eosdis.nasa.gov` |
| **IBGE** | ✅ OK | 417 municípios BA | `servicodados.ibge.gov.br` |
| **OpenDataSUS/CNES** | ⚠️ Parcial | 28 hospitais BA | `apidadosabertos.saude.gov.br` |
| **CEIS (CGU)** | ❌ Bloqueado | — | `portaldatransparencia.gov.br` (requer auth) |
| **SICONFI (Tesouro)** | ❌ Bloqueado | — | `apidatalake.tesouro.gov.br` (404 endpoints) |

---

## 🎯 INICIATIVAS DO PORTFÓLIO

### 🏆 OPP-001 — RespostaPublicaQueimadas (PROVEN, score 9/10)
- **Pergunta pública:** "Quanto e como o poder público está comprando em municípios com queimadas ativas?"
- **Fontes:** PNCP × NASA FIRMS × IBGE
- **Achados quantificados:**
  - 51 editais BA + 1.417 focos FIRMS
  - 1 edital em ALERTA (Catu, a <10km de queimada ativa)
  - 10 editais em AVISO (Juazeiro com 13 focos em 50km)
- **Demo:** Mapa da Bahia com pontos coloridos
- **Reuso de código:** Pipeline Lux-Lab/pncp_bahia_intelligence + raster pipeline GhostWorks
- **Por que submeter:** Diferencial único (nenhum reúso cruza PNCP + FIRMS)

### 🥈 OPP-002 — FracionamentoVisivel (PROVEN, score 8/10)
- **Pergunta pública:** "Que órgãos publicam múltiplas dispensas no mesmo dia com objetos similares?"
- **Fontes:** PNCP
- **Achados quantificados:** Comando da Marinha — 6 dispensas em 1 dia (28/08/2026)
- **Por que submeter:** Caso concreto de auditoria, padrão de fracionamento

### 🥉 OPP-003 — ConcentracaoDispensada (PROVEN, score 7/10)
- **Pergunta pública:** "Que UFs têm concentração anormal de dispensas?"
- **Fontes:** PNCP × IBGE
- **Achados:** CE 62%, RJ 57%, GO 50% vs média 21.7%
- **Por que NÃO submeter isoladamente:** Tema específico, menor novidade

### 🏅 OPP-004 — SaudeEmAreaDeRisco (EXPERIMENTED, score 8/10)
- **Pergunta pública:** "Hospitais públicos estão em áreas de queimada ativa?"
- **Fontes:** CNES × NASA FIRMS
- **Achados:** 1 hospital a 3.99km de queimada ativa (NATHALIA DE MELO GUIMARAES), 2 a 6-7km
- **Por que submeter:** Cruza saúde + ambiente (cobre critério "foco em pessoas")
- **Limitação:** Amostra CNES = 28 hospitais (API limitada); vale ampliar antes de submeter

---

## 🛠️ O QUE FOI EXECUTADO

### Trilha 1 — Materialização (✅ completa)
- 4 iniciativas estruturadas com pergunta, fontes, achados, código reutilizável
- Demo HTML (8KB) com KPIs, portfólio, mapa estático, tabela de hospitais, gráfico
- Screenshots capturados (4 PNGs da demo + 1 mapa estático)
- Mapa estático gerado via matplotlib (funciona offline)

### Trilha 2 — Exploração adicional
- **CNES × FIRMS** ✅ — produziu OPP-004 (caso material: hospital a 3.99km de queimada)
- **CEIS/CNEP** ❌ — URLs bloqueadas (requer autenticação/JS)
- **SICONFI** ❌ — endpoints 404 (URLs erradas ou desativadas)
- **Bras.IO CNES expandido** ❌ — 401 Unauthorized

### Tentativas que falharam (registradas)
- OpenDataSUS paginação (limitado a 20)
- INPE Queimadas direto (SSL fail)
- Brasil.IO CNES (autenticação)
- Leaflet com tiles OpenStreetMap (sem internet)

---

## 📂 ESTRUTURA DE ARQUIVOS

```
/home/vinicius/.hermes/cgu_registry/
├── registry.json                 # Manifest completo (1.5KB)
├── raw/                          # Dados brutos
│   ├── pncp_editais_br_500.json  # 350 editais (779KB)
│   ├── cnes_ba_full.json         # 300 hospitais (475KB)
│   ├── firms/firms_24h_south_america.csv  # 17.835 focos BR
│   ├── eonet/eonet_wildfires_brasil.json
│   └── ...
├── achados/                      # Datasets derivados
│   ├── dataset_derivado_focos_firms_ba.geojson     (282KB, 1417 features)
│   ├── dataset_derivado_editais_pncp_bahia.geojson (27KB, 51 features)
│   ├── dataset_derivado_crossdata.csv              (CSV pronto)
│   ├── crossdata_cnes_fires.json                   (28 hospitais)
│   ├── ciclo4_achados_marinha_ceara.json
│   └── ...
├── demo/                         # Material demonstrável
│   ├── index.html                # 8KB - demo interativa
│   ├── screenshots/
│   │   ├── 01_topo.png           # 234KB
│   │   ├── 02_mapa.png           # 130KB
│   │   ├── 03_dados.png          # 94KB
│   │   ├── 04_proveniencia.png   # 116KB
│   │   └── mapa_estatico.png     # 87KB (matplotlib, offline)
│   ├── build_demo_final.py       # Script de geração
│   └── mapa_estatico.py          # Gerador de mapa
└── scripts/                      # Pipelines de aquisição
    ├── ciclo1_500_brasil.py
    ├── ciclo4_marinha.py
    ├── ciclo7_crossdata.py
    └── ...
```

---

## 🎯 RECOMENDAÇÃO FINAL DE SUBMISSÃO

**Submeter 2 iniciativas: OPP-001 + OPP-004**

**Justificativa:**
1. **OPP-001** tem o **maior diferencial competitivo** — cruza PNCP + FIRMS (nenhum reúso atual faz)
2. **OPP-004** cobre o critério "foco em pessoas" (peso 2) que OPP-001 não cobre
3. Juntas: 3 fontes (PNCP, FIRMS, CNES) + 2 cruzamentos únicos
4. Cobertura dos critérios do edital:
   - Apresentação (×2): 8-9/10
   - Inovação (×2): 9-10/10 (cruzamentos novos)
   - Transparência (×2): 8-9/10
   - Foco em pessoas (×2): 7-9/10
   - Múltiplas fontes (×1): 9-10/10
   - Ferramentas (×1): 8-9/10
   - Inclusividade (×1): 6-7/10

**Score composto estimado: 78% do máximo** (conservador)

**Alternativa:** Submeter 3 (incluindo OPP-002 — caso Marina como inovação metodológica).

---

## 🛠️ O QUE FALTA PARA SUBMETER

1. **README de cada iniciativa** com:
   - Pergunta pública
   - Fontes e URLs
   - Metodologia de transformação
   - Limitações conhecidas
2. **Validação manual** dos achados (ex: confirmar caso Marinha 28/08)
3. **Expansão CNES** — buscar mais hospitais BA para fortalecer OPP-004
4. **Submissão Form Etapa 1** (até 09/09)
5. **Submissão dados.gov.br Etapa 2** (até 11/09)
6. **Hospedar demo** (GitHub Pages ou similar)

---

## 📌 PRÓXIMOS CICLOS POSSÍVEIS

1. **Expandir coleta PNCP** — pegar histórico de 12 meses (não só editais ativos)
2. **Cruzar com CEIS via outra rota** — tentar basedosdados.org, kaggle.com
3. **CNES via DATASUS direto** — FTP ou CSV mensal
4. **Visualização temporal** — animação de queimadas 7 dias × editais publicados
5. **Adicionar mapa do Brasil** — não só Bahia

---

## 💡 O QUE FUNCIONOU vs FALHOU

### ✅ Funcionou
- Discovery autônomo em ~3h
- Identificação de 4 oportunidades materializáveis
- 3 com dados reais confirmados
- Cruzamento PNCP × FIRMS × CNES (inédito)
- Demo HTML funcional + mapa estático (offline-capable)
- Screenshots automáticos via Playwright

### ❌ Falhou
- API OpenDataSUS (limitada a 20-300 registros por UF)
- URLs do CEIS (autenticação/JS)
- SICONFI (endpoints 404)
- INPE Queimadas direto (SSL)
- Google Drive upload (token expirado)

---

**FIM DO RELATÓRIO. AGUARDANDO DECISÃO SOBRE SUBMISSÃO.** 🫡
