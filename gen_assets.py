#!/usr/bin/env python3
"""Generador de mockups SVG para el portafolio MAFC.
Produce 5 imágenes de sistema (estilo dashboard) coherentes con la marca.
Ejecutar:  python3 gen_assets.py
"""
import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS, exist_ok=True)

# ---------------------------------------------------------------------------
# Utilidades de dibujo
# ---------------------------------------------------------------------------

def bars(x, y, w, h, values, color, gap=10):
    n = len(values)
    bw = (w - gap * (n - 1)) / n
    mx = max(values)
    out = []
    for i, v in enumerate(values):
        bh = h * (v / mx)
        bx = x + i * (bw + gap)
        by = y + (h - bh)
        out.append(
            f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
            f'rx="3" fill="{color}" opacity="{0.45 + 0.55*(v/mx):.2f}"/>'
        )
    return "\n".join(out)


def line_chart(x, y, w, h, values, color):
    n = len(values)
    mx, mn = max(values), min(values)
    span = (mx - mn) or 1
    pts = []
    for i, v in enumerate(values):
        px = x + w * (i / (n - 1))
        py = y + h - h * ((v - mn) / span)
        pts.append((px, py))
    d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    area = d + f" L {pts[-1][0]:.1f} {y+h:.1f} L {pts[0][0]:.1f} {y+h:.1f} Z"
    dots = "\n".join(
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="{color}"/>' for px, py in pts
    )
    return (
        f'<path d="{area}" fill="{color}" opacity="0.12"/>'
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" '
        f'stroke-linecap="round" stroke-linejoin="round"/>{dots}'
    )


def donut(cx, cy, r, frac, color):
    import math
    circ = 2 * math.pi * r
    dash = circ * frac
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#2b3444" stroke-width="12"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="12" '
        f'stroke-linecap="round" stroke-dasharray="{dash:.1f} {circ:.1f}" '
        f'transform="rotate(-90 {cx} {cy})"/>'
        f'<text x="{cx}" y="{cy+5}" font-family="Space Grotesk, sans-serif" font-size="20" '
        f'font-weight="700" fill="#fff" text-anchor="middle">{int(frac*100)}%</text>'
    )


def rows(x, y, w, rowh, count, accent):
    out = []
    for i in range(count):
        ry = y + i * (rowh + 8)
        out.append(f'<rect x="{x}" y="{ry}" width="{w}" height="{rowh}" rx="6" fill="#1c2331"/>')
        out.append(f'<circle cx="{x+18}" cy="{ry+rowh/2}" r="8" fill="{accent}" opacity="0.8"/>')
        out.append(f'<rect x="{x+36}" y="{ry+rowh/2-9}" width="{w*0.35:.0f}" height="7" rx="3.5" fill="#3a475a"/>')
        out.append(f'<rect x="{x+36}" y="{ry+rowh/2+2}" width="{w*0.22:.0f}" height="6" rx="3" fill="#2a3342"/>')
        tag_w = 54
        out.append(f'<rect x="{x+w-tag_w-14}" y="{ry+rowh/2-9}" width="{tag_w}" height="18" rx="9" fill="{accent}" opacity="0.18"/>')
    return "\n".join(out)


def mockup(accent, title, kpis, chart_svg, list_rows, badge):
    """Devuelve un SVG de dashboard 900x560."""
    W, H = 900, 560
    accent_dim = accent
    kpi_svg = []
    kx, ky, kw, kh = 250, 96, 190, 92
    for i, (label, val) in enumerate(kpis):
        x = kx + i * (kw + 16)
        kpi_svg.append(f'''
        <rect x="{x}" y="{ky}" width="{kw}" height="{kh}" rx="14" fill="#161d2b" stroke="#28313f"/>
        <rect x="{x+16}" y="{ky+16}" width="34" height="34" rx="9" fill="{accent}" opacity="0.16"/>
        <circle cx="{x+33}" cy="{ky+33}" r="7" fill="{accent}"/>
        <text x="{x+16}" y="{ky+70}" font-family="Plus Jakarta Sans, sans-serif" font-size="12" fill="#8a95a6">{label}</text>
        <text x="{x+16}" y="{ky+52}" font-family="Space Grotesk, sans-serif" font-size="24" font-weight="700" fill="#ffffff">{val}</text>''')
    kpi_svg = "\n".join(kpi_svg)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b1017"/>
      <stop offset="1" stop-color="#10151f"/>
    </linearGradient>
    <linearGradient id="glow" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0.35"/>
    </linearGradient>
    <radialGradient id="halo" cx="0.8" cy="0" r="1">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.20"/>
      <stop offset="0.6" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" rx="18" fill="url(#halo)"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="#232c3a"/>

  <!-- Sidebar -->
  <rect x="20" y="20" width="200" height="{H-40}" rx="14" fill="#0f1622"/>
  <circle cx="48" cy="52" r="12" fill="url(#glow)"/>
  <text x="70" y="57" font-family="Space Grotesk, sans-serif" font-size="16" font-weight="700" fill="#fff">MAFC</text>
  <text x="70" y="72" font-family="Plus Jakarta Sans, sans-serif" font-size="9" letter-spacing="1" fill="{accent}">SOFTWARE</text>
  {''.join(f'<rect x="40" y="{104+i*40}" width="{160 if i else 160}" height="26" rx="8" fill="{accent+"22" if i==0 else "#151d29"}"/><rect x="52" y="{113+i*40}" width="{90-i*8}" height="8" rx="4" fill="{accent if i==0 else "#33404f"}" opacity="{0.9 if i==0 else 0.7}"/>' for i in range(6))}

  <!-- Topbar -->
  <text x="250" y="52" font-family="Space Grotesk, sans-serif" font-size="22" font-weight="700" fill="#fff">{title}</text>
  <rect x="250" y="64" width="{len(badge)*7+34}" height="22" rx="11" fill="{accent}" opacity="0.16"/>
  <circle cx="266" cy="75" r="4" fill="{accent}"/>
  <text x="278" y="79" font-family="Plus Jakarta Sans, sans-serif" font-size="11" fill="{accent}">{badge}</text>
  <circle cx="{W-52}" cy="52" r="18" fill="#182130"/>
  <circle cx="{W-52}" cy="52" r="18" fill="none" stroke="{accent}" stroke-opacity="0.5"/>
  <circle cx="{W-52}" cy="52" r="8" fill="{accent}" opacity="0.7"/>

  <!-- KPIs -->
  {kpi_svg}

  <!-- Panel chart -->
  <rect x="250" y="204" width="380" height="336" rx="16" fill="#131a26" stroke="#232c3a"/>
  <text x="272" y="236" font-family="Plus Jakarta Sans, sans-serif" font-size="13" fill="#c3ccd9" font-weight="600">Rendimiento</text>
  <g transform="translate(272,262)">{chart_svg}</g>

  <!-- Panel lista -->
  <rect x="646" y="204" width="234" height="336" rx="16" fill="#131a26" stroke="#232c3a"/>
  <text x="666" y="236" font-family="Plus Jakarta Sans, sans-serif" font-size="13" fill="#c3ccd9" font-weight="600">Actividad</text>
  <g transform="translate(666,252)">{list_rows}</g>
</svg>'''
    return svg


# ---------------------------------------------------------------------------
# Definición de los 5 proyectos
# ---------------------------------------------------------------------------
BLUE = "#2563EB"
EMERALD = "#10B981"
VIOLET = "#7C5CFC"
AMBER = "#F59E0B"
CYAN = "#06B6D4"

projects = {
    "project-optica.svg": dict(
        accent=BLUE, title="Óptica CRM", badge="Historias Clínicas",
        kpis=[("Pacientes", "1,284"), ("Citas hoy", "37"), ("Ventas", "S/ 8.9k")],
        chart=lambda a: bars(0, 20, 336, 210, [40, 65, 52, 80, 60, 95, 74], a),
        rows=lambda a: rows(0, 0, 200, 40, 6, a),
    ),
    "project-fisio.svg": dict(
        accent=EMERALD, title="Fisioterapia CRM", badge="Gestión de Citas",
        kpis=[("Sesiones", "642"), ("Terapeutas", "12"), ("Ocupación", "88%")],
        chart=lambda a: line_chart(0, 20, 336, 210, [30, 45, 40, 62, 58, 80, 72, 95], a),
        rows=lambda a: rows(0, 0, 200, 40, 6, a),
    ),
    "project-restaurante.svg": dict(
        accent=AMBER, title="Restaurante POS", badge="Control de Pedidos",
        kpis=[("Mesas", "24/30"), ("Pedidos", "156"), ("Ticket", "S/ 42")],
        chart=lambda a: bars(0, 20, 336, 210, [70, 88, 60, 95, 78, 66, 90], a),
        rows=lambda a: rows(0, 0, 200, 40, 6, a),
    ),
    "project-inventario.svg": dict(
        accent=CYAN, title="Inventario ERP", badge="Multi-sucursal",
        kpis=[("SKU", "5,120"), ("Sucursales", "4"), ("Stock", "97%")],
        chart=lambda a: line_chart(0, 20, 336, 210, [80, 60, 72, 55, 68, 50, 62, 48], a),
        rows=lambda a: rows(0, 0, 200, 40, 6, a),
    ),
    "project-bodega.svg": dict(
        accent=VIOLET, title="Bodega POS", badge="Inventario Rápido",
        kpis=[("Ventas", "312"), ("Productos", "2,340"), ("Margen", "31%")],
        chart=lambda a: bars(0, 20, 336, 210, [55, 72, 48, 85, 66, 92, 70], a),
        rows=lambda a: rows(0, 0, 200, 40, 6, a),
    ),
}

for fname, p in projects.items():
    chart_svg = p["chart"](p["accent"])
    list_rows = p["rows"](p["accent"])
    svg = mockup(p["accent"], p["title"], p["kpis"], chart_svg, list_rows, p["badge"])
    with open(os.path.join(ASSETS, fname), "w", encoding="utf-8") as f:
        f.write(svg)
    print("escrito", fname)

print("Mockups generados en", ASSETS)
