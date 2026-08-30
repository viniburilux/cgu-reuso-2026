"""
Ciclo 7: Cruzamento REAL - Focos NASA FIRMS + PNCP Bahia
Objetivo: detectar resposta pública (contratos emergenciais) a queimadas
"""
import csv, json, math
from pathlib import Path

REG = Path('/home/vinicius/.hermes/cgu_registry')

# 1. Carregar focos FIRMS BA (24h)
firms = []
with open(REG / 'raw/firms/firms_24h_south_america.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        if -18.4 <= lat <= -8.5 and -46.6 <= lon <= -37.4:
            firms.append({
                'lat': lat,
                'lon': lon,
                'date': row['acq_date'],
                'time': row['acq_time'],
                'confidence': row['confidence'],
                'frp': float(row['frp']) if row['frp'] else 0,
                'bright_ti4': float(row['bright_ti4']) if row['bright_ti4'] else 0,
            })

print(f"Focos FIRMS na Bahia (24h): {len(firms)}")

data = json.load(open(REG / 'raw/pncp_editais_br_500.json'))
items = data['items']
ba = [i for i in items if i.get('uf') == 'BA']

mun_centroids = {
    'Salvador': (-12.97, -38.51),
    'Camaçari': (-12.70, -38.32),
    'Feira de Santana': (-12.27, -38.96),
    'Vitória da Conquista': (-14.86, -40.84),
    'Itabuna': (-14.79, -39.28),
    'Juazeiro': (-9.41, -40.50),
    'Teixeira de Freitas': (-17.54, -39.74),
    'Valença': (-13.37, -39.07),
    'Maraú': (-14.10, -39.00),
    'Biritinga': (-11.62, -38.80),
    'Catu': (-12.35, -38.38),
    'Ipiaú': (-14.13, -39.73),
    'Boa Nova': (-14.36, -40.21),
    'Maracás': (-13.44, -40.43),
    'Sobradinho': (-12.50, -39.10),
    'Campo Alegre de Lourdes': (-9.51, -43.01),
    'Bom Jesus da Lapa': (-13.26, -43.42),
    'São Gonçalo dos Campos': (-12.43, -38.95),
}

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

results = []
for e in ba:
    mun = e.get('municipio_nome', '?')
    if mun not in mun_centroids:
        results.append({
            'municipio': mun,
            'descricao': e.get('description', '')[:80],
            'modalidade': e.get('modalidade_licitacao_nome'),
            'data': e.get('createdAt', '')[:10],
            'tem_coords': False,
            'focos_50km': 'N/I',
            'focos_10km': 'N/I',
        })
        continue
    lat_m, lon_m = mun_centroids[mun]
    f50 = sum(1 for f in firms if haversine_km(lat_m, lon_m, f['lat'], f['lon']) <= 50)
    f10 = sum(1 for f in firms if haversine_km(lat_m, lon_m, f['lat'], f['lon']) <= 10)
    results.append({
        'municipio': mun,
        'descricao': e.get('description', '')[:80],
        'modalidade': e.get('modalidade_licitacao_nome'),
        'data': e.get('createdAt', '')[:10],
        'tem_coords': True,
        'focos_50km': f50,
        'focos_10km': f10,
    })

print("\n" + "="*60)
print("CROSS-DATA: Editais BA x Focos NASA FIRMS (24h)")
print("="*60)
print(f"{'municipio':30} {'modalidade':25} {'focos10km':>10} {'focos50km':>10}")
print("-"*80)
for r in sorted(results, key=lambda x: -1 if not isinstance(x['focos_50km'], int) else -x['focos_50km']):
    if r['tem_coords']:
        flag = "ALERTA" if r['focos_10km'] > 0 else ("aviso" if r['focos_50km'] > 0 else "")
        print(f"{flag:6} {r['municipio']:30} {r['modalidade']:25} {r['focos_10km']:>10} {r['focos_50km']:>10}")

out = REG / 'achados/ciclo7_crossdata_pncp_fires.json'
out.write_text(json.dumps({
    'focos_total_bahia_24h': len(firms),
    'editais_bahia_total': len(ba),
    'editais_bahia_com_coordenadas': sum(1 for r in results if r['tem_coords']),
    'editais_bahia_sem_coordenadas': sum(1 for r in results if not r['tem_coords']),
    'top_editais_com_focos_proximos': sorted(
        [r for r in results if r['tem_coords']],
        key=lambda x: -x['focos_50km']
    )[:20],
    'editais_proximos_10km': [r for r in results if r.get('focos_10km', 0) > 0],
}, indent=2, ensure_ascii=False))
print(f"\nSaved: {out}")
