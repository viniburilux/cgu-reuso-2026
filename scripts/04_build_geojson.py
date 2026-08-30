"""
Ciclo 8: Gerar dataset derivado GeoJSON pronto pra mapa
Cross-data: PNCP Bahia editais + NASA FIRMS focos 24h
"""
import csv, json, math
from pathlib import Path
from datetime import datetime, timezone

REG = Path('/home/vinicius/.hermes/cgu_registry')

# Carregar editais BA
data = json.load(open(REG / 'raw/pncp_editais_br_500.json'))
items = data['items']
ba = [i for i in items if i.get('uf') == 'BA']

# Carregar FIRMS BA
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

# Centróides municipais
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

# GeoJSON 1: Pontos de focos FIRMS
fires_geo = {
    'type': 'FeatureCollection',
    'name': 'focos_firms_bahia_24h',
    'metadata': {
        'source': 'NASA FIRMS - https://firms.modaps.eosdis.nasa.gov',
        'satellite': 'NOAA-20 VIIRS',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'count': len(firms),
        'region': 'Bahia, Brasil',
    },
    'features': [
        {
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [f['lon'], f['lat']]},
            'properties': {
                'date': f['date'],
                'time': f['time'],
                'confidence': f['confidence'],
                'frp': f['frp'],
                'bright_ti4': f['bright_ti4'],
            }
        } for f in firms
    ]
}
out_fires = REG / 'achados/dataset_derivado_focos_firms_ba.geojson'
out_fires.write_text(json.dumps(fires_geo, ensure_ascii=False))
print(f"Focos GeoJSON: {out_fires} ({out_fires.stat().st_size // 1024}KB)")

# GeoJSON 2: Editais BA com flag de proximidade a queimadas
editais_geo = {
    'type': 'FeatureCollection',
    'name': 'editais_pncp_bahia_com_queimadas',
    'metadata': {
        'source_pncp': 'https://pncp.gov.br/api/search/',
        'source_fires': 'NASA FIRMS',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'count': len(ba),
        'note': 'Cada edital mostra quantos focos FIRMS (24h) em 10km e 50km',
    },
    'features': []
}

for e in ba:
    mun = e.get('municipio_nome', '?')
    coords = mun_centroids.get(mun)
    if not coords:
        continue
    lat_m, lon_m = coords
    f10 = sum(1 for f in firms if haversine_km(lat_m, lon_m, f['lat'], f['lon']) <= 10)
    f50 = sum(1 for f in firms if haversine_km(lat_m, lon_m, f['lat'], f['lon']) <= 50)
    # Distância até o foco mais próximo
    if firms:
        dist_min = min(haversine_km(lat_m, lon_m, f['lat'], f['lon']) for f in firms)
    else:
        dist_min = None

    editais_geo['features'].append({
        'type': 'Feature',
        'geometry': {'type': 'Point', 'coordinates': [lon_m, lat_m]},
        'properties': {
            'municipio': mun,
            'uf': 'BA',
            'modalidade': e.get('modalidade_licitacao_nome'),
            'descricao': e.get('description', '')[:200],
            'orgao': e.get('orgao_nome', '')[:80],
            'data_publicacao': e.get('createdAt', ''),
            'focos_10km': f10,
            'focos_50km': f50,
            'distancia_foco_mais_proximo_km': round(dist_min, 1) if dist_min else None,
            'flag_queimada': 'ALERTA' if f10 > 0 else ('AVISO' if f50 > 0 else 'OK'),
        }
    })

out_editais = REG / 'achados/dataset_derivado_editais_pncp_bahia.geojson'
out_editais.write_text(json.dumps(editais_geo, ensure_ascii=False))
print(f"Editais GeoJSON: {out_editais} ({out_editais.stat().st_size // 1024}KB)")

# CSV consolidado
csv_path = REG / 'achados/dataset_derivado_crossdata.csv'
with open(csv_path, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['municipio', 'lat', 'lon', 'data_publicacao', 'modalidade', 'orgao',
                'descricao', 'focos_10km', 'focos_50km', 'distancia_min_km', 'flag'])
    for feat in editais_geo['features']:
        p = feat['properties']
        g = feat['geometry']
        w.writerow([p['municipio'], g['coordinates'][1], g['coordinates'][0],
                    p['data_publicacao'], p['modalidade'], p['orgao'],
                    p['descricao'], p['focos_10km'], p['focos_50km'],
                    p['distancia_foco_mais_proximo_km'], p['flag_queimada']])
print(f"CSV: {csv_path}")

# Summary
print("\n" + "="*60)
print("RESUMO DOS ACHADOS (PROVENIÊNCIA)")
print("="*60)
print(f"  Focos NASA FIRMS BA 24h: {len(firms)}")
print(f"  Editais PNCP BA 7d: {len(ba)}")
print(f"  Editais com ALERTA (foco <10km): {sum(1 for f in editais_geo['features'] if f['properties']['flag_queimada'] == 'ALERTA')}")
print(f"  Editais com AVISO (foco <50km): {sum(1 for f in editais_geo['features'] if f['properties']['flag_queimada'] == 'AVISO')}")
print(f"  Editais sem proximidade: {sum(1 for f in editais_geo['features'] if f['properties']['flag_queimada'] == 'OK')}")
print(f"\nFontes:")
print(f"  - PNCP: https://pncp.gov.br/api/search/?tipos_documento=edital")
print(f"  - FIRMS: https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_South_America_24h.csv")
print(f"  - IBGE: https://servicodados.ibge.gov.br/api/v1/localidades/estados/BA/municipios")
print(f"\nDatasets derivados (3):")
print(f"  1. {out_fires.name}")
print(f"  2. {out_editais.name}")
print(f"  3. {csv_path.name}")
