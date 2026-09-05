# MAFC — Web Corporativa

Sitio web corporativo de **MAFC · Soluciones Digitales & Software a Medida**.
Estilo *Corporate Blue & White* (navbar/hero/footer en azul marino, resto del
sitio en blanco/celeste claro), construido con **HTML5 semántico + Tailwind
CSS (CDN) + JavaScript Vanilla ES6+**. Sin dependencias de build: se abre
directamente en el navegador.

## Estructura

```
MAFC_Web_Corporativa/
├── index.html          # Página única (landing) con todas las secciones
├── robots.txt          # Indexación para buscadores
├── sitemap.xml         # Mapa del sitio (SEO)
├── css/
│   └── main.css        # Estilos personalizados: tarjetas, bordes reactivos, responsive
├── js/
│   └── main.js         # Navbar, menú móvil, reveal, filtro, modales de video, formulario, analytics
├── public/
│   ├── logo/
│   │   └── logo.png                   # Logo real de MAFC (navbar + footer)
│   ├── img/
│   │   ├── gestion-opticas.png        # Captura real · Óptica Mavie (también fondo difuminado del Hero)
│   │   ├── pos-restaurantes.jpeg      # Captura real · Antojitos al Paso
│   │   ├── control-inventarios.jpeg   # Captura real · Comercializadora T&E S.A.S.
│   │   ├── gestion-fisioterapia.jpeg  # Captura real · Movimiento Koray
│   │   └── ventas-bodegas.jpeg        # Captura real · Comercial Ruiz (también en el Hero)
│   └── video/
│       ├── demo-fisioterapia.mp4      # Demo real · Movimiento Koray
│       └── demo-bodega.mp4            # Demo real · Comercial Ruiz
├── assets/
│   ├── favicon.svg / favicon-32.png / favicon-16.png / apple-touch-icon.png
│   ├── og-image.jpg     # Imagen para Open Graph / Twitter Card (1200x630)
│   └── project-*.svg    # Mockups SVG originales (ya no se usan en el portafolio, quedan de respaldo)
├── gen_assets.py       # (Desarrollo) Generador de los mockups SVG
├── zip_builder.py      # Empaquetador → MAFC_Web_Corporativa.zip
└── README.md
```

Las 5 tarjetas del portafolio (Ópticas, Fisioterapia, Restaurantes,
Inventario y Bodegas) usan capturas y videos **reales** de sistemas en
producción — ya no quedan mockups ilustrativos en el portafolio.

## Cómo verlo

Abre `index.html` en tu navegador. Para evitar restricciones de algunos
navegadores con archivos locales, puedes servirlo:

```bash
python3 -m http.server 8080
# luego visita http://localhost:8080
```

## Empaquetar para entrega

```bash
python3 zip_builder.py
```

Genera `MAFC_Web_Corporativa.zip` con todos los archivos del sitio (incluye `public/`, `robots.txt` y `sitemap.xml`).

## ⚠️ Antes de publicar en producción

Se dejaron **dos marcadores de posición** porque son datos que solo tú tienes:

1. **Google Analytics 4** — en `index.html` (dentro de `<head>`) busca
   `G-XXXXXXXXXX` (aparece 2 veces) y reemplázalo por tu Measurement ID real.
   Lo obtienes en [analytics.google.com](https://analytics.google.com) →
   Administrar → Flujos de datos → tu flujo web. El código ya está integrado
   y funcionando (incluye eventos personalizados `whatsapp_click` en todos los
   botones de WhatsApp y `generate_lead` al enviar el formulario de contacto).

2. **Dominio final** — se usó `https://www.mafcsoluciones.pe/` como
   marcador en: el `<link rel="canonical">`, las etiquetas `og:url` /
   `og:image` / `twitter:image`, los datos estructurados (JSON-LD),
   `robots.txt` y `sitemap.xml`. Reemplázalo por tu dominio real con
   buscar-y-reemplazar en esos archivos antes de publicar.

**Redes sociales:** Facebook ya apunta a tu página real
(`facebook.com/profile.php?id=61591894984374`) en el footer, la sección de
contacto y los datos estructurados. Instagram y TikTok todavía apuntan a los
dominios genéricos (`instagram.com`, `tiktok.com`) — reemplázalos por tus
perfiles reales cuando los tengas, o quita esos íconos mientras tanto.

## Personalización rápida

- **WhatsApp / Celular:** `+51 924996961`. Está en los CTAs, el botón
  flotante y el formulario. Para cambiarlo, reemplaza `51924996961` en
  `index.html` y la constante `WA_PHONE` en `js/main.js`.
- **Colores de marca:** editables en `:root` de `css/main.css` (tokens
  `--accent`, `--accent-2`, `--navy`, etc.) y en `tailwind.config` dentro de
  `index.html`. El esquema actual es azul (`#2563EB` / `#3B82F6`) y blanco,
  sin colores neón.
- **Logo:** `public/logo/logo.png`. Se usa en el navbar, el footer y para
  generar los favicons (`assets/favicon-*.png`, `apple-touch-icon.png`).
  Si cambias el logo, vuelve a generar esos PNG a partir del nuevo archivo.
- **Fondo del Hero:** el fondo de la portada usa `public/img/gestion-opticas.png`
  muy difuminado y oscurecido (ver `#inicio::before` en `css/main.css`). Si
  más adelante tienes una foto propia (equipo, oficina, etc.), reemplaza esa
  ruta por la nueva imagen.
- **Imágenes y videos del portafolio:** todas en `public/img/` y
  `public/video/`, ya con capturas y demos reales de cada cliente.

## SEO y Analytics ya integrados

- Meta description, `robots`, `canonical`, Open Graph completo (con imagen
  real 1200×630) y Twitter Card.
- Datos estructurados JSON-LD (`ProfessionalService`) con nombre, teléfono,
  Facebook real y servicios ofrecidos.
- `robots.txt` + `sitemap.xml`.
- Favicons en SVG + PNG (16/32/180px) generados desde el logo real.
- Google Analytics 4 (`gtag.js`) con seguimiento de clics en WhatsApp y envíos
  del formulario de contacto como eventos personalizados.

## Secciones agregadas en la segunda ronda de mejoras

- **Clientes** (después del Hero): franja con los nombres reales de los
  negocios que ya usan un sistema de MAFC — sin testimonios inventados.
- **Badges de confianza** (en Portafolio): "Sistemas reales en producción",
  "Código propio, sin plantillas", "Soporte directo con quien lo construye".
- **Planes** (`#planes`, en el menú): 3 tarjetas por alcance (Llave en Mano /
  Desarrollo a Medida / Multi-sucursal) con checklist de qué incluye cada
  una. Sin precios inventados — cada botón "Cotizar este plan" abre WhatsApp
  con el nombre del plan precargado.
- **Preguntas Frecuentes** (`#faq`, enlazada desde el footer): acordeón
  hecho con `<details>`/`<summary>` nativo de HTML (cero JavaScript, cero
  riesgo de bugs de animación).
- **Lightbox del portafolio**: al hacer clic en las capturas de Ópticas,
  Restaurantes o Inventario (las que no tienen video), se abren en grande
  en un modal con la ficha del proyecto. Fisioterapia y Bodegas siguen
  abriendo su demo en video como antes.

## Lo que NO se implementó (y por qué)

- **Testimonios con cita textual de clientes**: no tengo frases reales que
  esos negocios hayan autorizado a publicar. Inventar una cita atribuida a
  "Antojitos al Paso" o "Comercial Ruiz" sería una reseña falsa a nombre de
  un tercero real — no lo voy a hacer. Si consigues 2-3 frases cortas
  autorizadas por tus clientes, con gusto arma la sección con citas reales.
- **Precios exactos en Planes**: no conozco tus tarifas reales, así que el
  plan se vende por alcance/checklist en vez de un número inventado.
- **Blog / casos de estudio con métricas** ("aumentó ventas 30%"): no tengo
  esos datos verificados; en su lugar se reforzó el Portafolio y se agregó
  el FAQ, que cubren gran parte del mismo objetivo de SEO y confianza.
- **Chat en vivo**: requiere una cuenta en un servicio externo (Tawk.to,
  Crisp, WhatsApp Business API, etc.) que debes crear tú — dime cuál
  prefieres y agrego el snippet.
- **Versión en inglés**: es un cambio grande (duplicar todo el contenido +
  selector de idioma) que preferí no apurar para no introducir bugs;
  puedo hacerlo en una siguiente iteración dedicada si lo necesitas.
- **Core Web Vitals**: no es algo que se "implemente" en el código, se mide
  después de publicar en [PageSpeed Insights](https://pagespeed.web.dev).
