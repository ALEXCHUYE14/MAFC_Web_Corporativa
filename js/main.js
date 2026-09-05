/* =====================================================================
   MAFC — main.js · JavaScript Vanilla ES6+
   Navbar inteligente · Menú móvil · Reveal on scroll · Bordes reactivos
   Filtro de portafolio · Modales de video · Formulario + WhatsApp
   ===================================================================== */
(() => {
  'use strict';

  const WA_PHONE = '51924996961';
  const $  = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));

  document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initMobileMenu();
    initReveal();
    initReactiveCards();
    initPortfolioFilter();
    initVideoModal();
    initImageLightbox();
    initContactForm();
    initFooterYear();
    initAnalyticsEvents();
  });

  /* -------------------------------------------------------------------
     0. Analytics: envía eventos a Google Analytics 4 (gtag) sin romper
        nada si GA está bloqueado o aún no cargó (ad-blockers, etc.)
  ------------------------------------------------------------------- */
  function trackEvent(name, params) {
    if (typeof window.gtag === 'function') {
      try { window.gtag('event', name, params || {}); } catch (_) { /* noop */ }
    }
  }

  function initAnalyticsEvents() {
    $$('a[href*="wa.me"]').forEach(link => {
      link.addEventListener('click', () => {
        const host = link.closest('section, header, footer');
        trackEvent('whatsapp_click', {
          link_location: link.dataset.section || (host && host.id) || 'page'
        });
      });
    });
  }

  /* -------------------------------------------------------------------
     1. Navbar: fondo al hacer scroll + link activo por sección
  ------------------------------------------------------------------- */
  function initNavbar() {
    const nav = $('#nav');
    if (!nav) return;

    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    const links = $$('.nav-link[data-section]');
    const sections = links
      .map(l => document.getElementById(l.dataset.section))
      .filter(Boolean);

    if (!sections.length || !('IntersectionObserver' in window)) return;

    const spy = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          const id = e.target.id;
          links.forEach(l => l.classList.toggle('active', l.dataset.section === id));
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });

    sections.forEach(s => spy.observe(s));
  }

  /* -------------------------------------------------------------------
     2. Menú móvil (hamburguesa) con overlay y bloqueo de scroll
  ------------------------------------------------------------------- */
  function initMobileMenu() {
    const burger  = $('#burger');
    const panel   = $('#mobilePanel');
    const overlay = $('#mobileOverlay');
    if (!burger || !panel || !overlay) return;

    const open  = () => setMenu(true);
    const close = () => setMenu(false);

    function setMenu(state) {
      burger.classList.toggle('active', state);
      panel.classList.toggle('open', state);
      overlay.classList.toggle('open', state);
      burger.setAttribute('aria-expanded', String(state));
      document.body.style.overflow = state ? 'hidden' : '';
    }

    burger.addEventListener('click', () =>
      panel.classList.contains('open') ? close() : open()
    );
    overlay.addEventListener('click', close);
    $$('.mobile-link', panel).forEach(l => l.addEventListener('click', close));
    $$('[data-close-menu]', panel).forEach(b => b.addEventListener('click', close));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  /* -------------------------------------------------------------------
     3. Reveal on scroll (IntersectionObserver)
  ------------------------------------------------------------------- */
  function initReveal() {
    const els = $$('.reveal');
    if (!els.length) return;

    if (!('IntersectionObserver' in window)) {
      els.forEach(el => el.classList.add('in'));
      return;
    }
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('in'); obs.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    els.forEach(el => io.observe(el));
  }

  /* -------------------------------------------------------------------
     4. Bordes/brillo reactivos al cursor sobre las tarjetas
  ------------------------------------------------------------------- */
  function initReactiveCards() {
    if (window.matchMedia('(hover: none)').matches) return; // omitir en táctil
    $$('.card').forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        card.style.setProperty('--mx', `${e.clientX - r.left}px`);
        card.style.setProperty('--my', `${e.clientY - r.top}px`);
      });
    });
  }

  /* -------------------------------------------------------------------
     5. Filtro de proyectos por categoría
  ------------------------------------------------------------------- */
  function initPortfolioFilter() {
    const buttons = $$('.filter-btn');
    const cards = $$('.project-card');
    if (!buttons.length || !cards.length) return;

    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const filter = btn.dataset.filter;
        buttons.forEach(b => b.classList.toggle('active', b === btn));
        cards.forEach(card => {
          const cats = (card.dataset.category || '').split(' ');
          const show = filter === 'all' || cats.includes(filter);
          card.classList.toggle('hide', !show);
        });
      });
    });
  }

  /* -------------------------------------------------------------------
     6. Modal de video (Fisioterapia y Bodegas)
  ------------------------------------------------------------------- */
  function initVideoModal() {
    const modal = $('#videoModal');
    if (!modal) return;
    const video    = $('#modalVideo');
    const source   = $('#modalSource');
    const titleEl  = $('#modalTitle');
    const backdrop = $('.modal-backdrop', modal);
    const closeBtn = $('.modal-close', modal);

    const open = (src, title) => {
      if (src) {
        source.src = src;
        video.setAttribute('poster', modal.dataset.poster || '');
        video.load();
      }
      titleEl.textContent = title || 'Demo del sistema';
      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      const play = video.play();
      if (play && typeof play.catch === 'function') play.catch(() => {});
    };

    const close = () => {
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      try { video.pause(); video.currentTime = 0; } catch (_) {}
    };

    $$('[data-video]').forEach(trigger => {
      trigger.addEventListener('click', () => {
        modal.dataset.poster = trigger.dataset.poster || '';
        open(trigger.dataset.video, trigger.dataset.title);
      });
    });

    closeBtn && closeBtn.addEventListener('click', close);
    backdrop && backdrop.addEventListener('click', close);
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && modal.classList.contains('open')) close();
    });
  }

  /* -------------------------------------------------------------------
     6b. Modal de imagen (lightbox del portafolio): abre en grande las
         tarjetas que son solo captura (Ópticas, Restaurantes, Inventario).
         Las tarjetas con video (Fisioterapia, Bodegas) siguen abriendo el
         modal de video de arriba, sin cambios.
  ------------------------------------------------------------------- */
  function initImageLightbox() {
    const triggers = $$('.lightbox-trigger');
    const modal = $('#imageModal');
    if (!triggers.length || !modal) return;

    const imgEl    = $('#imageModalImg');
    const titleEl  = $('#imageModalTitle');
    const descEl   = $('#imageModalDesc');
    const tagsEl   = $('#imageModalTags');
    const backdrop = $('.modal-backdrop', modal);
    const closeBtn = $('.modal-close', modal);

    const open = (trigger) => {
      const card = trigger.closest('.project-card');
      const sourceImg = $('img', trigger);
      const heading   = card && $('h3', card);
      const paragraph = card && $('p', card);
      const tags      = card ? $$('.tag', card) : [];

      if (sourceImg && imgEl) {
        imgEl.src = sourceImg.src;
        imgEl.alt = sourceImg.alt || '';
      }
      if (titleEl) titleEl.textContent = heading ? heading.textContent.trim() : 'Proyecto';
      if (descEl)  descEl.textContent  = paragraph ? paragraph.textContent.trim() : '';
      if (tagsEl) {
        tagsEl.innerHTML = '';
        tags.forEach(tag => tagsEl.appendChild(tag.cloneNode(true)));
      }

      modal.classList.add('open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      trackEvent('portfolio_image_view', { project: titleEl ? titleEl.textContent : '' });
    };

    const close = () => {
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    };

    triggers.forEach(trigger => trigger.addEventListener('click', () => open(trigger)));
    closeBtn && closeBtn.addEventListener('click', close);
    backdrop && backdrop.addEventListener('click', close);
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && modal.classList.contains('open')) close();
    });
  }

  /* -------------------------------------------------------------------
     7. Formulario de contacto: validación en tiempo real + WhatsApp
  ------------------------------------------------------------------- */
  function initContactForm() {
    const form = $('#contactForm');
    if (!form) return;

    const rules = {
      nombre:  v => v.trim().length >= 3        || 'Ingresa tu nombre completo (mín. 3 caracteres).',
      telefono:v => /^[+\d][\d\s()-]{6,}$/.test(v.trim()) || 'Ingresa un teléfono/WhatsApp válido.',
      negocio: v => v.trim() !== ''             || 'Selecciona tu tipo de negocio.',
      mensaje: v => v.trim().length >= 10       || 'Cuéntanos un poco más (mín. 10 caracteres).'
    };

    const fields = {};
    Object.keys(rules).forEach(name => {
      const input = form.elements[name];
      if (!input) return;
      fields[name] = input.closest('.field');
      const evt = input.tagName === 'SELECT' ? 'change' : 'input';
      input.addEventListener(evt, () => validate(name));
      input.addEventListener('blur', () => validate(name));
    });

    function validate(name) {
      const input = form.elements[name];
      const wrap  = fields[name];
      const res   = rules[name](input.value);
      const ok    = res === true;
      wrap.classList.toggle('valid', ok && input.value.trim() !== '');
      wrap.classList.toggle('invalid', !ok);
      const msg = $('.field-msg', wrap);
      if (msg) msg.textContent = ok ? '' : res;
      return ok;
    }

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let valid = true;
      Object.keys(rules).forEach(n => { if (!validate(n)) valid = false; });
      if (!valid) {
        const firstInvalid = $('.field.invalid input, .field.invalid select, .field.invalid textarea', form);
        firstInvalid && firstInvalid.focus();
        return;
      }

      const data = {
        nombre:   form.elements.nombre.value.trim(),
        telefono: form.elements.telefono.value.trim(),
        negocio:  form.elements.negocio.value.trim(),
        mensaje:  form.elements.mensaje.value.trim()
      };

      const text =
        `Hola MAFC 👋, soy *${data.nombre}*.\n` +
        `📱 Teléfono/WhatsApp: ${data.telefono}\n` +
        `🏢 Tipo de negocio: ${data.negocio}\n` +
        `📝 Mensaje: ${data.mensaje}\n\n` +
        `Quisiera cotizar un software a medida.`;

      const url = `https://wa.me/${WA_PHONE}?text=${encodeURIComponent(text)}`;

      trackEvent('generate_lead', { negocio: data.negocio, form_id: 'contactForm' });

      const btn = $('#submitBtn', form);
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = 'Abriendo WhatsApp…'; }

      window.open(url, '_blank', 'noopener');

      const feedback = $('#formFeedback');
      if (feedback) { feedback.hidden = false; }
      setTimeout(() => {
        form.reset();
        Object.values(fields).forEach(f => f.classList.remove('valid', 'invalid'));
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label || 'Enviar por WhatsApp'; }
      }, 1200);
    });
  }

  /* -------------------------------------------------------------------
     8. Año dinámico en el footer
  ------------------------------------------------------------------- */
  function initFooterYear() {
    const y = $('#year');
    if (y) y.textContent = new Date().getFullYear();
  }
})();
