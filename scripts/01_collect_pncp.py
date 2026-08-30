"""
Ciclo 1: Pega editais BR com mais páginas, agrega, filtra BA depois
"""
import os, json, urllib.request, time
from pathlib import Path
from datetime import datetime, timezone

REG = Path('/home/vinicius/.hermes/cgu_registry')
RAW = REG / 'raw'
RAW.mkdir(exist_ok=True)

def fetch(url, retries=2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            if i == retries:
                return {'_error': str(e), '_url': url}
            time.sleep(2)

# Pegar 10 páginas de 50 = 500 editais
all_items = []
for page in range(1, 11):
    url = f"https://pncp.gov.br/api/search/?tipos_documento=edital&ordenacao=-data&pagina={page}&tam_pagina=50&status=recebendo_proposta"
    print(f"Page {page}/10...")
    data = fetch(url)
    if '_error' in data:
        print(f"  ERROR: {data['_error'][:100]}")
        time.sleep(3)
        continue
    items = data.get('items', [])
    all_items.extend(items)
    print(f"  Got {len(items)} (total: {len(all_items)})")
    time.sleep(0.5)

# Save
out = RAW / 'pncp_editais_br_500.json'
out.write_text(json.dumps({'items': all_items}, indent=2, ensure_ascii=False))
print(f"\nTotal saved: {len(all_items)}")
print(f"File: {out} ({out.stat().st_size // 1024}KB)")

# Stats
from collections import Counter
ufs = Counter(i.get('uf') for i in all_items)
mods = Counter(i.get('modalidade_licitacao_nome') for i in all_items)
print("\nTop UFs:")
for uf, c in ufs.most_common(10):
    print(f"  {uf}: {c}")
print("\nTop modalidades:")
for m, c in mods.most_common(10):
    print(f"  {m}: {c}")
