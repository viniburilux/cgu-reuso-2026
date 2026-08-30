"""
Ciclo 4: Achado não trivial - Marinha com 8 dispensas
Investigar se há padrão suspeito (mesmo objeto, valores fracionados)
"""
import json, re
from pathlib import Path
from collections import Counter
from pathlib import Path

REG = Path('/home/vinicius/.hermes/cgu_registry')
data = json.load(open(REG / 'raw/pncp_editais_br_500.json'))
items = data['items']

# 1. Todas dispensas da Marinha
mar = [i for i in items if i.get('orgao_nome') == 'COMANDO DA MARINHA' and i.get('modalidade_licitacao_nome') == 'Dispensa']
print(f"COMANDO DA MARINHA — Dispensas: {len(mar)}")
for i in mar:
    print(f"  {i.get('createdAt', '?')[:19]} | {i.get('unidade_nome', '?')[:50]}")
    print(f"    {i.get('description', '?')[:100]}")
    print()

# 2. Todas dispensas do Estado do Ceará
ce = [i for i in items if i.get('orgao_nome') == 'ESTADO DO CEARA' and i.get('modalidade_licitacao_nome') == 'Dispensa']
print(f"\nESTADO DO CEARÁ — Dispensas: {len(ce)}")
for i in ce:
    print(f"  {i.get('createdAt', '?')[:19]} | {i.get('municipio_nome', '?')}")
    print(f"    {i.get('description', '?')[:100]}")

# 3. Detectar potencial fracionamento
# Mesma raiz de palavras, mesmo órgão, mesmo dia
print("\n" + "="*60)
print("POSSÍVEL FRACIONAMENTO (mesmo órgão, mesmo dia, objetos similares)")
print("="*60)

# Agrupar por (orgao, data) e ver se há múltiplos
from collections import defaultdict
groups = defaultdict(list)
for i in items:
    if i.get('modalidade_licitacao_nome') == 'Dispensa':
        key = (i.get('orgao_nome'), i.get('createdAt', '')[:10])
        groups[key].append(i)

# Filtrar grupos com > 2 dispensas no mesmo dia
for (org, dia), lst in groups.items():
    if len(lst) >= 3:
        print(f"\n  📅 {dia} | {org[:50]}")
        for i in lst:
            print(f"      - {i.get('description', '?')[:80]}")

# Salvar achado
out = REG / 'achados/ciclo4_achados_marinha_ceara.json'
out.write_text(json.dumps({
    'marinha_dispensas': [{'data': i.get('createdAt'), 'unidade': i.get('unidade_nome'), 'desc': i.get('description')} for i in mar],
    'ceara_dispensas': [{'data': i.get('createdAt'), 'municipio': i.get('municipio_nome'), 'desc': i.get('description')} for i in ce],
    'grupos_suspeitos': [
        {'orgao': k[0], 'data': k[1], 'count': len(v),
         'descricoes': [i.get('description') for i in v]}
        for k, v in groups.items() if len(v) >= 3
    ],
}, indent=2, ensure_ascii=False))
print(f"\nSaved: {out}")
