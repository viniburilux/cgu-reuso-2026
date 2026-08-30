"""
Mapa estatico via matplotlib (sem dependencia de tiles)
Gera PNG para usar como imagem na demo
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

REG = Path('/home/vinicius/.hermes/cgu_registry')
OUT = REG / 'demo/screenshots/mapa_estatico.png'
OUT.parent.mkdir(exist_ok=True, parents=True)

# Carregar artefatos
focos = json.load(open(REG / 'achados/dataset_derivado_focos_firms_ba.geojson'))
editais = json.load(open(REG / 'achados/dataset_derivado_editais_pncp_bahia.geojson'))
cnes = json.load(open(REG / 'achados/crossdata_cnes_fires.json'))

# Coordenadas da BA
ba_bbox = {'lat_min': -18, 'lat_max': -8, 'lon_min': -47, 'lon_max': -38}

fig, ax = plt.subplots(figsize=(12, 10), dpi=100)
ax.set_facecolor('#0f172a')
fig.patch.set_facecolor('#0f172a')

# Bahia outline simples (box)
rect = plt.Rectangle((ba_bbox['lon_min'], ba_bbox['lat_min']),
                     ba_bbox['lon_max']-ba_bbox['lon_min'],
                     ba_bbox['lat_max']-ba_bbox['lat_min'],
                     facecolor='#1e293b', edgecolor='#475569', linewidth=2)
ax.add_patch(rect)

# Focos FIRMS
foc_lat, foc_lon = [], []
for f in focos['features']:
    g = f['geometry']
    foc_lon.append(g['coordinates'][0])
    foc_lat.append(g['coordinates'][1])
ax.scatter(foc_lon, foc_lat, c='#dc2626', s=3, alpha=0.4, label='Foco FIRMS (24h)', edgecolors='none')

# Editais
edi_lon, edi_lat, edi_col, edi_size = [], [], [], []
for f in editais['features']:
    p = f['properties']
    g = f['geometry']
    edi_lon.append(g['coordinates'][0])
    edi_lat.append(g['coordinates'][1])
    flag = p.get('flag_queimada', 'OK')
    if flag == 'ALERTA':
        edi_col.append('#dc2626'); edi_size.append(200)
    elif flag == 'AVISO':
        edi_col.append('#f59e0b'); edi_size.append(120)
    else:
        edi_col.append('#22c55e'); edi_size.append(60)
ax.scatter(edi_lon, edi_lat, c=edi_col, s=edi_size, alpha=0.85, edgecolors='white', linewidth=1.5, zorder=5)

# Hospitais CNES em risco
hosp_lat, hosp_lon, hosp_col = [], [], []
for h in cnes.get('top_hospitais_risco', []):
    if h.get('focos_5km', 0) + h.get('focos_10km', 0) > 0:
        # Achar lat/lon do crossdata
        # vou pegar do dataset original CNES
        pass

# Carregar CNES
cnes_data = json.load(open(REG / 'raw/cnes_ba_full.json'))
hosp_lat, hosp_lon, hosp_markers = [], [], []
cross_lookup = {(h.get('lat'), h.get('lon')): h for h in cnes.get('top_hospitais_risco', [])}
for e in cnes_data.get('estabelecimentos', []):
    lat = e.get('latitude_estabelecimento_decimo_grau')
    lon = e.get('longitude_estabelecimento_decimo_grau')
    if lat and lon and -18 <= float(lat) <= -8 and -47 <= float(lon) <= -38:
        hosp_lat.append(float(lon))
        hosp_lon.append(float(lat))
ax.scatter(hosp_lat, hosp_lon, c='#0ea5e9', s=80, marker='P', alpha=1.0,
           edgecolors='white', linewidth=1, label='Hospital CNES', zorder=4)

# Estilo
ax.set_xlim(ba_bbox['lon_min'], ba_bbox['lon_max'])
ax.set_ylim(ba_bbox['lat_min'], ba_bbox['lat_max'])
ax.set_xlabel('Longitude', color='#cbd5e1')
ax.set_ylabel('Latitude', color='#cbd5e1')
ax.set_title('Bahia - Cruzamento PNCP x NASA FIRMS x CNES (24h)',
             color='#f8fafc', fontsize=14, fontweight='bold', pad=20)
ax.tick_params(colors='#cbd5e1')
for spine in ax.spines.values():
    spine.set_color('#475569')
ax.grid(True, color='#334155', alpha=0.5)

# Legenda
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#dc2626', markersize=8, label='Foco FIRMS (24h)', alpha=0.7),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#dc2626', markersize=14, label='Edital ALERTA (foco<10km)', alpha=1),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#f59e0b', markersize=11, label='Edital AVISO (foco<50km)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#22c55e', markersize=8, label='Edital OK'),
    Line2D([0], [0], marker='P', color='w', markerfacecolor='#0ea5e9', markersize=12, label='Hospital CNES'),
]
ax.legend(handles=legend_elements, loc='lower left', facecolor='#1e293b', edgecolor='#475569',
          labelcolor='#f1f5f9', fontsize=10)

# Stats
stats = (
    f"Editais BA: {len(editais['features'])}\n"
    f"Focos FIRMS: {len(focos['features'])}\n"
    f"Hospitais BA: 28\n"
    f"Editais ALERTA: {sum(1 for f in editais['features'] if f['properties'].get('flag_queimada')=='ALERTA')}\n"
    f"Editais AVISO: {sum(1 for f in editais['features'] if f['properties'].get('flag_queimada')=='AVISO')}"
)
ax.text(0.99, 0.99, stats, transform=ax.transAxes, color='#f1f5f9',
        verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#1e293b', edgecolor='#475569'),
        fontsize=10, family='monospace')

plt.tight_layout()
plt.savefig(OUT, dpi=100, facecolor=fig.get_facecolor())
plt.close()
print(f"Mapa estatico salvo: {OUT} ({OUT.stat().st_size // 1024}KB)")
