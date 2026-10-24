# MAFC Software E.I.R.L. — Web Corporativa

Sitio web corporativo de **MAFC Software E.I.R.L.** (antes "MAFC Soluciones").
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
├── vercel.json         # Config de despliegue (ver sección "Despliegue en Vercel")
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

## Despliegue en Vercel

El sitio está desplegado en **https://mafcsoftwareeirl.vercel.app**
(proyecto `mafcsoftwareeirl` en Vercel, antes `mafcsoluciones`; conectado al repo de
GitHub `ALEXCHUYE14/MAFC_Web_Corporativa`).

⚠️ **`vercel.json` es obligatorio** en este proyecto: por convención, Vercel
sirve el contenido de la carpeta `public/` como raíz del sitio *si esa
carpeta existe* — pero aquí `public/` solo contiene el logo y las capturas
del portafolio, no el `index.html`. `vercel.json` fuerza
`"outputDirectory": "."` para que Vercel sirva la raíz real del proyecto.
Si borras ese archivo, el sitio dejará de funcionar (mostrará 404).

Para volver a desplegar manualmente:

```bash
vercel --prod
```

Como el repo de GitHub quedó conectado al proyecto, cualquier `git push` a
la rama principal también puede disparar un despliegue automático desde
Vercel.

## Empaquetar para entrega

```bash
python3 zip_builder.py
```

Genera `MAFC_Web_Corporativa.zip` con todos los archivos del sitio (incluye `public/`, `robots.txt` y `sitemap.xml`).

## ⚠️ Antes de publicar en producción

Se dejaron **dos marcadores de posición** porque son datos que solo tú tienes:

1. **Google Analytics 4** — en `index.html` (dentro de `<head>`) busca
   ✅ Configurado con el ID `G-BWZBS346LN` (variable `GA_ID`, único lugar).
   Para cambiarlo, edita solo el valor de `GA_ID` — no uses "reemplazar
   todo", la línea de abajo valida el formato. Eventos que se registran:
   `whatsapp_click`, `generate_lead`, `portfolio_image_view`,
   `video_play` (con `video_mode` = `inline` o `modal`) y `youtube_click`.
   Lo obtienes en [analytics.google.com](https://analytics.google.com) →
   Administrar → Flujos de datos → tu flujo web. El código ya está integrado
   y funcionando (incluye eventos personalizados `whatsapp_click` en todos los
   botones de WhatsApp y `generate_lead` al enviar el formulario de contacto).

2. **Dominio** — el sitio está desplegado en
   `https://mafcsoftwareeirl.vercel.app/`, y ese es el dominio usado en el
   `<link rel="canonical">`, las etiquetas `og:url` / `og:image` /
   `twitter:image`, los datos estructurados (JSON-LD), `robots.txt` y
   `sitemap.xml`. Si más adelante conectas un dominio propio (ej.
   `mafcsoluciones.pe`) en Vercel, reemplaza esta URL por la nueva con
   buscar-y-reemplazar en esos mismos archivos.

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
- **Planes** (`#planes`, en el menú): 3 tarjetas por alcance (Llave en Mano
  S/400 · Desarrollo a Medida S/500 · Multi-sucursal S/600, precios "desde")
  con checklist de qué incluye cada una. Cada botón "Cotizar este plan" abre
  WhatsApp con el nombre del plan precargado.
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

## Tercera ronda: MAFC Software E.I.R.L.

- **Nueva marca** en todo el sitio: título, navbar, hero, footer, mensajes de
  WhatsApp precargados y datos estructurados ("MAFC Software EIRL",
  "MAFC Software E.I.R.L.", "MAFC Software").
- **Sección Videos** (`#videos`): video destacado + 6 videos reales del canal
  [@MiguelfloresDev](https://www.youtube.com/@MiguelfloresDev). Cada video se
  puede *Reproducir* dentro de la tarjeta, abrir en *Pantalla grande* (modal
  con botón de pantalla completa) o ir a *YouTube*. Solo se carga la
  miniatura hasta que el usuario hace clic (página rápida). Para cambiar
  videos: edita los `data-yt-id` en `index.html` (y sus `VideoObject` en el
  JSON-LD y `sitemap.xml`).
- **Sección Nosotros** (`#nosotros`) con la foto del fundador en
  `public/img/equipo/miguel-flores.jpg`.
- **SEO**: JSON-LD `@graph` (Organization, Person, WebSite, WebPage,
  VideoObject, FAQPage), robots avanzados, `site.webmanifest`, sitemap con
  imágenes y videos.
- **Íconos de Instagram/TikTok** (que apuntaban a páginas genéricas) se
  reemplazaron por el canal de YouTube real.

### Para aparecer en Google al buscar "MAFC Software"

1. Crea la propiedad en [Google Search Console](https://search.google.com/search-console),
   pega tu código en la meta `google-site-verification` (comentada en el
   `<head>`), despliega y envía `sitemap.xml`. Luego usa "Inspeccionar URL →
   Solicitar indexación".
2. Recomendado: un dominio propio con la marca (ej. `mafcsoftware.com` o
   `mafcsoftware.pe`). Al conectarlo, reemplaza `mafcsoftwareeirl.vercel.app`
   en `index.html`, `robots.txt` y `sitemap.xml`.
3. Crea un **Perfil de Empresa en Google** (Google Business Profile) con el
   nombre "MAFC Software EIRL" y enlaza esta web y el canal de YouTube.
4. En la descripción de cada video de YouTube, agrega el enlace a la web.

> Nota: abrir `index.html` con doble clic (`file://`) puede mostrar error en
> los videos de YouTube; pruébalo con `python -m http.server 8080` o ya
> desplegado en Vercel.
