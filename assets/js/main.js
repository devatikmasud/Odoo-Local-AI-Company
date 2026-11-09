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
    if (y < 120) clearActive();
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
  function clearActive() { (links || []).forEach(function (l) { l.classList.remove('is-active'); }); }
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
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  /* FAQ: only one answer open at a time */
  var faq = doc.querySelectorAll('.faq-item');
  faq.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) faq.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });

  /* Contact form: validates, then opens the visitor's mail app with the enquiry prefilled.
     (Static hosting has no mail backend. To send via a service instead, replace this
     block with a fetch() POST to your form endpoint.) */
  var form = doc.querySelector('form[data-contact]');
  if (form) {
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if (form.elements.website && form.elements.website.value) return;   // honeypot: bots only
      var lines = [];
      [].slice.call(form.querySelectorAll('input[name], select[name], textarea[name]')).forEach(function (el) {
        if (el.name === 'website' || el.name === 'consent' || !el.value) return;
        var lab = form.querySelector('label[for="' + el.id + '"]');
        var text = lab ? lab.textContent.replace(/\s*\*\s*$/, '').replace(/\s*\(.*\)$/, '') : el.name;
        lines.push(text + ': ' + el.value);
      });
      var body = lines.join('\n');
      window.location.href = 'mailto:' + form.getAttribute('data-to') +
        '?subject=' + encodeURIComponent(form.getAttribute('data-subject')) +
        '&body=' + encodeURIComponent(body);
      if (status) { status.hidden = false; status.focus && status.setAttribute('tabindex', '-1'); }
    });
  }
})();


/* EIGENKERN detail-page routing: keep homepage markup/design unchanged. */
(function () {
  'use strict';
  var industryRoutesDE = {
    'steuerkanzleien': 'steuer.html', 'arztpraxen': 'aerzte.html',
    'handwerk': 'handwerk.html', 'rechtsanwälte': 'rechtsanwaelte.html',
    'rechtsanwaelte': 'rechtsanwaelte.html', 'kommunen': 'kommunen.html',
    'industrie': 'industrie.html', 'energie & landwirtschaft': 'energie.html',
    'bildung': 'bildung.html'
  };
  var industryRoutesEN = {
    'tax firms': 'tax-firms.html', 'medical practices': 'medical-practices.html',
    'trades': 'trades.html', 'trades & crafts': 'trades.html', 'law firms': 'law-firms.html',
    'municipalities': 'municipalities.html', 'industry': 'industry.html',
    'energy & agriculture': 'energy-agriculture.html', 'education': 'education.html'
  };
  var solutionRoutesDE = {
    'lokale ki': 'lokale-ki.html', 'eigener server': 'server.html',
    'hybrid-modus': 'hybrid.html', 'hybrid mode': 'hybrid.html'
  };
  var solutionRoutesEN = {
    'local ai': 'local-ai.html', 'own server': 'own-server.html', 'your own server': 'own-server.html',
    'hybrid mode': 'hybrid-mode.html'
  };
  function clean(t) { return (t || '').toLowerCase().replace(/^\s*\d+\.?\s*/, '').replace(/\s+/g, ' ').trim(); }
  document.addEventListener('click', function (event) {
    var a = event.target && event.target.closest ? event.target.closest('a[href]') : null;
    if (!a) return;
    var path = window.location.pathname;
    var isEN = /\/en\/index\.html$/.test(path) || /\/en\/$/.test(path);
    var base = isEN ? '' : '';
    var href = (a.getAttribute('href') || '').trim();
    if (!/^(kontakt|contact)\.html(?:#.*)?$/i.test(href)) return;
    var option = a.closest('.option-card');
    if (option) {
      var heading = clean(option.querySelector('h3') ? option.querySelector('h3').textContent : '');
      var route = (isEN ? solutionRoutesEN : solutionRoutesDE)[heading];
      if (route) { event.preventDefault(); window.location.href = (isEN ? '' : '') + route; }
      return;
    }
    var industry = a.closest('.ind-card');
    if (industry) {
      var label = clean(industry.querySelector('.ind-label') ? industry.querySelector('.ind-label').textContent : industry.textContent);
      var route = (isEN ? industryRoutesEN : industryRoutesDE)[label];
      if (route) { event.preventDefault(); window.location.href = route; }
    }
  });
})();
