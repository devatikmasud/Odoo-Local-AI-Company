/* EIGENKERN – main.js (vanilla JS, no dependencies) */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var header = doc.querySelector('.site-header');
  var toggle = doc.querySelector('.nav-toggle');
  var nav = doc.getElementById('main-nav');
  var toTop = doc.querySelector('.to-top');

  /* Sticky header: shrink + shadow after scrolling; back-to-top button */
  function onScroll() {
    var y = window.pageYOffset || root.scrollTop;
    if (header) header.classList.toggle('is-scrolled', y > 8);
    if (toTop) toTop.classList.toggle('show', y > 600);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Mobile menu */
  function setMenu(open) {
    root.classList.toggle('nav-open', open);
    if (toggle) toggle.setAttribute('aria-expanded', String(open));
  }
  if (toggle) {
    toggle.addEventListener('click', function () { setMenu(!root.classList.contains('nav-open')); });
  }
  if (nav) {
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a') && !e.target.closest('.has-sub > .nav-link')) setMenu(false);
    });
  }
  doc.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      setMenu(false);
      doc.querySelectorAll('.has-sub.is-open').forEach(function (li) { li.classList.remove('is-open'); });
    }
  });

  /* Sub-menus (touch / keyboard) */
  doc.querySelectorAll('.has-sub').forEach(function (li) {
    var btn = li.querySelector('.sub-toggle');
    if (btn) btn.addEventListener('click', function () {
      var open = li.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
    });
  });
  doc.addEventListener('click', function (e) {
    if (!e.target.closest('.has-sub')) doc.querySelectorAll('.has-sub.is-open').forEach(function (li) { li.classList.remove('is-open'); });
  });

  /* Active link while scrolling */
  var links = [].slice.call(doc.querySelectorAll('.main-nav .nav-link'));
  var map = links.map(function (a) {
    var id = (a.getAttribute('href') || '').split('#')[1];
    return id ? { a: a, el: doc.getElementById(id) } : null;
  }).filter(function (x) { return x && x.el; });
  if ('IntersectionObserver' in window && map.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (l) { l.classList.remove('is-active'); });
        map.forEach(function (m) { if (m.el === en.target) m.a.classList.add('is-active'); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    map.forEach(function (m) { spy.observe(m.el); });
  }

  /* Scroll reveal */
  var items = doc.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.01, rootMargin: '0px 0px -6% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }



  /* Bilingual route map: switch language on the current page, never redirect
     an inner-page visitor to Contact or to the homepage unless no counterpart exists. */
  (function languageRouting() {
    var deToEn = {
      'index.html':'index.html', 'branchen.html':'industries.html',
      'steuer.html':'tax-firms.html', 'aerzte.html':'medical-practices.html',
      'handwerk.html':'trades.html', 'rechtsanwaelte.html':'law-firms.html',
      'kommunen.html':'municipalities.html', 'industrie.html':'industry.html',
      'energie.html':'energy-agriculture.html', 'bildung.html':'education.html',
      'technologie.html':'technology.html', 'lokale-ki.html':'local-ai.html',
      'server.html':'own-server.html', 'hybrid.html':'hybrid-mode.html',
      'waechter.html':'guardian.html', 'hardware.html':'hardware.html',
      'preise.html':'pricing.html', 'videos.html':'videos.html', 'faq.html':'faq.html',
      'kontakt.html':'contact.html', 'testen.html':'try-local-ai.html',
      'impressum.html':'imprint.html', 'datenschutz.html':'privacy.html', 'agb.html':'terms.html'
    };
    var path = window.location.pathname || '/index.html';
    var isEnglish = /\/en\//i.test(path);
    var filename = path.split('/').pop() || 'index.html';
    var enToDe = {};
    Object.keys(deToEn).forEach(function (de) { enToDe[deToEn[de]] = de; });
    var currentDir = path.slice(0, path.lastIndexOf('/') + 1);
    var baseDir = isEnglish ? currentDir.replace(/en\/$/i, '') : currentDir;
    var englishDir = baseDir + 'en/';
    var deFile = isEnglish ? (enToDe[filename] || 'index.html') : filename;
    var enFile = isEnglish ? filename : (deToEn[filename] || 'index.html');
    var deTarget = baseDir + deFile;
    var enTarget = englishDir + enFile;

    document.querySelectorAll('.lang-switch a[lang]').forEach(function (a) {
      var targetLang = (a.getAttribute('lang') || '').toLowerCase();
      if (targetLang === 'de') a.setAttribute('href', deTarget);
      if (targetLang === 'en') a.setAttribute('href', enTarget);
      var active = (targetLang === 'en' && isEnglish) || (targetLang === 'de' && !isEnglish);
      if (active) {
        a.classList.add('is-active');
        a.setAttribute('aria-current', 'page');
      } else {
        a.classList.remove('is-active');
        a.removeAttribute('aria-current');
      }
    });
    document.documentElement.setAttribute('lang', isEnglish ? 'en' : 'de');
    document.documentElement.setAttribute('translate', 'no');
  })();

  /* FAQ: only one answer open at a time */
  var faq = doc.querySelectorAll('.faq-item');
  faq.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) faq.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });
  /* Contact form: static site, so open the visitor's e-mail program with the prepared message */
  var form = doc.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = form.elements;
      var de = (root.getAttribute('lang') || 'de') === 'de';
      var lines = [
        'Name: ' + f.name.value,
        (de ? 'Unternehmen: ' : 'Company: ') + f.company.value,
        (de ? 'E-Mail: ' : 'Email: ') + f.email.value,
        (de ? 'Telefon: ' : 'Phone: ') + f.phone.value,
        (de ? 'Anliegen: ' : 'Topic: ') + f.topic.value,
        '',
        f.message.value
      ];
      window.location.href = 'mailto:' + form.getAttribute('data-to') +
        '?subject=' + encodeURIComponent(form.getAttribute('data-subject')) +
        '&body=' + encodeURIComponent(lines.join('\n'));
    });
  }
})();
