#!/usr/bin/env python3
"""EIGENKERN static site generator.

Usage:  python3 build/build.py

Generates the German (default, site root) and English (/en/) pages from the single
content dictionary in content.py, so both languages always share the same layout.
Output: index.html, kontakt.html, impressum.html, datenschutz.html, agb.html,
        en/index.html, en/contact.html, en/imprint.html, en/privacy.html, en/terms.html,
        sitemap.xml, robots.txt
"""
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import SITE, T, ICONS, LEGAL  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
esc = html.escape
LEGAL_KEYS = ("imprint", "privacy", "terms")


# ------------------------------------------------------------------ helpers
def icon(name, cls="i"):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def sprite():
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>']
    for name, (body, mode) in ICONS.items():
        if mode == "raw":
            attrs = ""
        elif mode:
            attrs = 'fill="currentColor" stroke="none"'
        else:
            attrs = 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
        out.append(f'<symbol id="i-{name}" viewBox="0 0 24 24" {attrs}>{body}</symbol>')
    out.append("</defs></svg>")
    return "".join(out)


FLAG_ROUND = ('<svg class="flag-round" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><defs><clipPath id="fc"><circle cx="12" cy="12" r="11"/></clipPath></defs>'
              '<g clip-path="url(#fc)"><rect width="24" height="8" fill="#111"/><rect y="8" width="24" height="8" fill="#d11"/><rect y="16" width="24" height="8" fill="#fc0"/></g>'
              '<circle cx="12" cy="12" r="11" fill="none" stroke="rgba(255,255,255,.35)"/></svg>')


def pre(lang):
    return "" if lang == "de" else "../"


def page_file(lang, key):
    if key == "index":
        return "index.html"
    if key == "contact":
        return T[lang]["contact"]["file"]
    return T[lang]["legal"][key]["file"]


def page_url(lang, key):
    base = SITE["url"] + ("" if lang == "de" else "/en")
    return base + "/" if key == "index" else f"{base}/{page_file(lang, key)}"


def head(lang, key, title, desc, prefix, noindex=False, extra=""):
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    canonical = page_url(lang, key)
    de_url, en_url = page_url("de", key), page_url("en", key)
    og_locale, og_alt = ("de_DE", "en_US") if lang == "de" else ("en_US", "de_DE")
    preload = f'<link rel="preload" href="{prefix}assets/img/hero/hero-office.jpg" as="image">\n' if key == "index" else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#061a33">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="de" href="{de_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{de_url}">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{og_locale}">
<meta property="og:locale:alternate" content="{og_alt}">
<meta property="og:image" content="{SITE['url']}/assets/img/seo/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
{preload}<link rel="stylesheet" href="{prefix}assets/css/style.css">
{extra}<script>document.documentElement.className='js';</script>
</head>
"""


def header(lang, key):
    t = T[lang]
    prefix = pre(lang)
    h = "" if key == "index" else "index.html"        # anchors point to the home page from sub pages
    contact = t["contact"]["file"]
    nav = []
    for item in t["nav"]:
        href = h + item["href"]
        if item.get("sub"):
            subs = "".join(f'<li><a href="{h}{s["href"]}">{esc(s["label"])}</a></li>' for s in item["sub"])
            nav.append(
                f'<li class="has-sub"><a href="{href}" class="nav-link" aria-haspopup="true">{esc(item["label"])}{icon("chevron-down", "i i-sm")}</a>'
                f'<button class="sub-toggle" type="button" aria-label="{esc(item["label"])}" aria-expanded="false">{icon("chevron-down", "i i-sm")}</button>'
                f'<ul class="sub">{subs}</ul></li>')
        else:
            nav.append(f'<li><a href="{href}" class="nav-link">{esc(item["label"])}</a></li>')
    other = "en" if lang == "de" else "de"
    alt = ("en/" if lang == "de" else "../") + page_file(other, key)
    if lang == "de":
        sw = ('<a class="lang is-active" href="#" aria-current="true" lang="de" hreflang="de">DE</a>'
              f'<a class="lang" href="{alt}" lang="en" hreflang="en" title="English">EN</a>')
    else:
        sw = (f'<a class="lang" href="{alt}" lang="de" hreflang="de" title="Deutsch">DE</a>'
              '<a class="lang is-active" href="#" aria-current="true" lang="en" hreflang="en">EN</a>')
    cta = f'<a class="btn btn-dark btn-sm" href="{contact}">{esc(t["cta_header"])} {icon("arrow-right", "i i-sm")}</a>'
    return f"""<body>
{sprite()}
<a class="skip" href="#main">{esc(t['skip'])}</a>
<header class="site-header" id="top">
  <div class="container header-row">
    <a class="logo" href="{'index.html' if key == 'index' else 'index.html'}" aria-label="EIGENKERN – {esc(t['home_label'])}">
      <img src="{prefix}assets/img/brand/logo-mark.svg" width="44" height="44" alt=""><span>EIGENKERN</span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="{esc(t['nav_label'])}">
      <ul>{''.join(nav)}</ul>
      <div class="nav-extra"><div class="lang-switch" role="group" aria-label="{esc(t['lang_label'])}">{sw}</div>{cta}</div>
    </nav>
    <div class="header-tools">
      <div class="lang-switch lang-switch--bar" role="group" aria-label="{esc(t['lang_label'])}">{sw}</div>
      <span class="header-cta">{cta}</span>
      <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="{esc(t['menu'])}">
        <span class="bars">{icon('menu')}</span><span class="x">{icon('close')}</span>
      </button>
    </div>
  </div>
</header>
"""


def band(lang):
    t = T[lang]
    return f"""<section class="cta-band" aria-labelledby="band-title">
  <div class="container band-row">
    <div class="band-copy"><h2 id="band-title">{esc(t['band']['title'])}</h2><p>{esc(t['band']['text'])}</p></div>
    <a class="btn btn-teal" href="{t['contact']['file']}">{esc(t['band']['button'])} {icon('arrow-right', 'i i-sm')}</a>
  </div>
</section>
"""


def footer(lang, key):
    t = T[lang]
    prefix = pre(lang)
    h = "" if key == "index" else "index.html"
    nav = "".join(f'<li><a href="{h}{i["href"]}">{esc(i["label"])}</a></li>' for i in t["nav"])
    legal = "".join(f'<li><a href="{L["file"]}">{esc(L["label"])}</a></li>' for L in t["legal"].values())
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div class="foot-brand">
      <a class="logo logo-light" href="index.html" aria-label="EIGENKERN"><img src="{prefix}assets/img/brand/logo-mark-light.svg" width="52" height="52" alt=""><span>EIGENKERN</span></a>
      <p>{esc(t['footer']['claim'])}</p>
    </div>
    <nav class="foot-nav" aria-label="{esc(t['footer']['nav_label'])}"><ul>{nav}</ul></nav>
    <address class="foot-contact">
      <a href="tel:{SITE['phone_raw']}">{icon('phone')}<span>{SITE['phone']}</span></a>
      <a href="mailto:{SITE['email']}">{icon('mail')}<span>{SITE['email']}</span></a>
      <span class="foot-addr">{icon('map-pin')}<span>{esc(t['footer']['location'])}</span></span>
    </address>
    <div class="foot-legal">
      <ul class="legal-links">{legal}</ul>
      <ul class="social" aria-label="{esc(t['footer']['social'])}">
        <li><a href="{SITE['linkedin']}" rel="noopener" aria-label="LinkedIn">{icon('linkedin')}</a></li>
        <li><a href="{SITE['youtube']}" rel="noopener" aria-label="YouTube">{icon('youtube')}</a></li>
        <li><a href="{SITE['x']}" rel="noopener" aria-label="X">{icon('x')}</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© {SITE['year']} EIGENKERN. {esc(t['footer']['rights'])}</p>
    <p>{esc(t['footer']['made'])} {FLAG_ROUND}</p>
  </div>
</footer>
<a class="to-top" href="#top" aria-label="{esc(t['footer']['top'])}">{icon('chevron-down', 'i i-sm up')}</a>
<script src="{prefix}assets/js/main.js" defer></script>
</body>
</html>
"""


# ------------------------------------------------------------------ home
def home_main(lang):
    t = T[lang]
    p = pre(lang)
    contact = t["contact"]["file"]
    h = t["hero"]
    arrow = icon("arrow-right", "i i-sm")

    trust = "".join(f'<li>{icon(i["icon"], "i i-lg")}<span><strong>{esc(i["a"])}</strong><br>{esc(i["b"])}</span></li>' for i in t["trust"])

    tiles = "".join(
        f'<li class="ind-card"><a href="{contact}"><img src="{p}assets/img/industries/{c["photo"]}.jpg" width="324" height="174" alt="" loading="lazy" style="object-position:{c["pos"]}">'
        f'<span class="ind-label">{icon(c["icon"], "i")}<span>{esc(c["label"])}</span></span></a></li>' for c in t["industries"]["items"])

    options = []
    for n, o in enumerate(t["options"]["items"], 1):
        ext = o["art"].rsplit(".", 1)[1]
        size = 'width="220" height="180"' if "ki-box" in o["art"] else ('width="200" height="170"' if "cloud" in o["art"] else 'width="346" height="214"')
        options.append(
            f'<li class="option" id="{o["id"]}"><article class="option-card">'
            f'<div class="option-art option-art--{ext}"><img src="{p}assets/img/{o["art"]}" {size} alt="" loading="lazy"></div>'
            f'<div class="option-body"><h3>{n:02d}. {esc(o["title"])}</h3><p>{esc(o["text"])}</p>'
            f'<a class="link-arrow" href="{contact}">{esc(t["options"]["more"])} {arrow}</a></div></article></li>')

    guard = []
    for n, s in enumerate(t["guard"]["steps"]):
        last = n == len(t["guard"]["steps"]) - 1
        guard.append(
            f'<li class="g-item{" g-last" if last else ""}"><article><span class="g-ico">{icon(s["icon"])}</span>'
            f'<h3>{esc(s["title"])}</h3><p>{esc(s["text"])}</p></article>'
            + ("" if last else f'<span class="g-arrow" aria-hidden="true">{icon("arrow-right")}</span>') + "</li>")

    steps = "".join(
        f'<li class="step"><span class="step-num">{n}</span><div class="step-card">{icon(s["icon"], "i step-ico")}'
        f'<p><strong>{esc(s["a"])}</strong>{"<br>" + esc(s["b"]) if s["b"] else ""}</p></div></li>'
        for n, s in enumerate(t["flow"]["items"], 1))

    checks = "".join(f'<li><span class="tick">{icon("check")}</span>{esc(x)}</li>' for x in t["why"]["list"])
    pr = t["pricing"]
    faq = "".join(
        f'<details class="faq-item"><summary><span>{esc(q["q"])}</span>{icon("plus", "i faq-plus")}</summary>'
        f'<div class="faq-a"><p>{esc(q["a"])}</p></div></details>' for q in t["faq"]["items"])

    return f"""<main id="main">
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-bg" role="img" aria-label="{esc(h['alt'])}"><span class="glass glass-1"></span><span class="glass glass-2"></span></div>
  <div class="container">
    <div class="hero-copy">
      <p class="hero-eyebrow">{esc(h['badge'])}</p>
      <h1 id="hero-title">{esc(h['title1'])}<br><span class="grad">{esc(h['title2'])}</span></h1>
      <p class="hero-sub">{esc(h['sub'])}</p>
      <p class="lead">{esc(h['lead'])}</p>
      <div class="btn-row">
        <a class="btn btn-dark" href="{contact}">{esc(h['cta1'])} {icon('arrow-right', 'i i-sm')}</a>
        <a class="btn btn-ghost" href="#technologie"><span class="play">{icon('play', 'i i-xs')}</span>{esc(h['cta2'])}</a>
      </div>
    </div>
  </div>
</section>
<section class="trust" aria-label="{esc(t['trust_label'])}"><div class="container"><ul>{trust}</ul></div></section>

<section class="section industries" id="branchen" aria-labelledby="ind-title">
  <div class="container split split-ind">
    <div class="split-copy reveal">
      <p class="eyebrow">{esc(t['industries']['eyebrow'])}</p>
      <h2 id="ind-title">{esc(t['industries']['title'])}</h2>
      <p>{esc(t['industries']['text'])}</p>
      <a class="text-link" href="{contact}">{esc(t['industries']['cta'])} {arrow}</a>
    </div>
    <ul class="ind-grid reveal">{tiles}</ul>
  </div>
</section>

<section class="section options" id="loesungen" aria-labelledby="opt-title">
  <div class="container split split-opt">
    <div class="split-copy reveal">
      <p class="eyebrow eyebrow-line">{esc(t['options']['eyebrow'])}</p>
      <h2 id="opt-title">{esc(t['options']['title'])}</h2>
      <p>{esc(t['options']['text'])}</p>
      <a class="btn btn-dark btn-sm" href="{contact}">{esc(t['options']['cta'])} {arrow}</a>
    </div>
    <ol class="options-grid reveal">{''.join(options)}</ol>
  </div>
</section>

<section class="section guard" id="technologie" aria-labelledby="guard-title">
  <div class="container split split-guard">
    <div class="split-copy reveal">
      <p class="eyebrow eyebrow-line">{esc(t['guard']['eyebrow'])}</p>
      <h2 id="guard-title">{esc(t['guard']['title'])}</h2>
      <p>{esc(t['guard']['text'])}</p>
      <a class="btn btn-outline-teal btn-sm" href="{contact}">{esc(t['guard']['cta'])} {arrow}</a>
    </div>
    <ol class="guard-flow reveal">{''.join(guard)}</ol>
  </div>
</section>

<section class="section flow" id="ablauf" aria-labelledby="flow-title">
  <div class="container flow-grid">
    <div class="split-copy reveal">
      <p class="eyebrow eyebrow-plain">{esc(t['flow']['eyebrow'])}</p>
      <h2 id="flow-title">{esc(t['flow']['title'])}</h2>
      <p>{esc(t['flow']['text'])}</p>
      <a class="btn btn-dark btn-sm" href="{contact}">{esc(t['flow']['cta'])} {arrow}</a>
    </div>
    <ol class="steps reveal">{steps}</ol>
    <aside class="cta-card reveal" aria-labelledby="cta-title">
      <div class="cta-copy">
        <h3 id="cta-title">{esc(t['cta_card']['title'])}</h3>
        <p>{esc(t['cta_card']['text'])}</p>
        <a class="btn btn-dark btn-sm" href="{contact}">{esc(t['cta_card']['button'])} {arrow}</a>
      </div>
      <img class="cta-photo" src="{p}assets/img/why/building.jpg" width="441" height="570" alt="" loading="lazy">
    </aside>
  </div>
</section>

<section class="section value" aria-label="{esc(t['why']['eyebrow'])}">
  <div class="container value-grid">
    <div class="why reveal" id="ueber-uns">
      <div class="why-copy">
        <p class="eyebrow eyebrow-line eyebrow-light">{esc(t['why']['eyebrow'])}</p>
        <h2>{esc(t['why']['title'])}</h2>
        <ul class="checks">{checks}</ul>
        <a class="btn btn-outline-light btn-sm" href="{contact}">{esc(t['why']['cta'])} {arrow}</a>
      </div>
      <img class="why-img" src="{p}assets/img/why/building.jpg" width="441" height="570" alt="{esc(t['why']['alt'])}" loading="lazy">
    </div>
    <div class="pricing reveal" id="preise">
      <h2>{esc(pr['title'])}</h2>
      <p class="pricing-sub">{esc(pr['sub'])}</p>
      <div class="price-grid">
        <article class="price price-main"><h3>{esc(pr['license'])}</h3><div class="price-body"><p class="amount"><small>{esc(pr['from'])}</small> {esc(pr['license_price'])}</p><p class="vat">{esc(pr['vat'])}</p><a class="btn btn-pill btn-xs" href="{contact}">{esc(pr['details'])} {icon('arrow-right', 'i i-xs')}</a></div></article>
        <span class="price-plus" aria-hidden="true">+</span>
        <article class="price"><h3>{esc(pr['care'])}</h3><div class="price-body"><p class="amount"><small>{esc(pr['from'])}</small> {esc(pr['care_price'])}</p><p class="vat">{esc(pr['vat'])}</p><a class="btn btn-pill btn-xs" href="{contact}">{esc(pr['details'])} {icon('arrow-right', 'i i-xs')}</a></div></article>
      </div>
    </div>
    <div class="faq reveal" id="faq">
      <h2>{esc(t['faq']['title'])}</h2>
      <div class="faq-list">{faq}</div>
    </div>
  </div>
</section>
{band(lang)}</main>
"""


# ------------------------------------------------------------------ contact
def contact_main(lang):
    t = T[lang]
    c = t["contact"]
    topics = "".join(f'<option value="{esc(x)}">{esc(x)}</option>' for x in c["topics"])
    info = []
    for i in c["info"]:
        val = f'<a href="{i["href"]}">{esc(i["value"])}</a>' if i["href"] else f'<span>{esc(i["value"])}</span>'
        info.append(f'<li><span class="info-ico">{icon(i["icon"])}</span><span class="info-text"><small>{esc(i["label"])}</small>{val}</span></li>')
    nxt = "".join(f'<li><span class="n">{n}</span><span>{esc(x)}</span></li>' for n, x in enumerate(c["next"], 1))
    return f"""<main id="main">
<section class="page-hero" aria-labelledby="page-title">
  <div class="page-hero-bg" aria-hidden="true"></div>
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="index.html">{esc(c['crumb_home'])}</a></li><li aria-current="page">{esc(c['label'])}</li></ol></nav>
    <p class="hero-eyebrow">{esc(c['eyebrow'])}</p>
    <h1 id="page-title">{esc(c['title'])}</h1>
    <p class="lead">{esc(c['lead'])}</p>
  </div>
</section>
<section class="section contact">
  <div class="container contact-grid">
    <div class="form-card reveal">
      <h2>{esc(c['form_title'])}</h2>
      <p class="muted">{esc(c['form_sub'])}</p>
      <form class="contact-form" data-contact data-subject="{esc(c['mail_subject'])}" data-to="{SITE['email']}" action="mailto:{SITE['email']}" method="post" enctype="text/plain">
        <div class="field-row">
          <div class="field"><label for="f-name">{esc(c['name'])} *</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="f-company">{esc(c['company'])}</label><input id="f-company" name="company" type="text" autocomplete="organization"></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="f-email">{esc(c['email'])} *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-phone">{esc(c['phone'])}</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
        </div>
        <div class="field"><label for="f-topic">{esc(c['topic'])}</label><select id="f-topic" name="topic">{topics}</select></div>
        <div class="field"><label for="f-message">{esc(c['message'])} *</label><textarea id="f-message" name="message" rows="6" placeholder="{esc(c['message_ph'])}" required></textarea></div>
        <div class="hp" aria-hidden="true"><label>Website<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
        <label class="consent"><input type="checkbox" name="consent" required><span>{c['consent']} *</span></label>
        <button class="btn btn-dark" type="submit">{esc(c['submit'])} {icon('send', 'i i-sm')}</button>
        <p class="form-status" role="status" aria-live="polite" hidden>{esc(c['success'])}</p>
      </form>
    </div>
    <aside class="contact-aside">
      <div class="info-card reveal"><h2>{esc(c['info_title'])}</h2><ul class="info-list">{''.join(info)}</ul></div>
      <div class="next-card reveal"><h2>{esc(c['next_title'])}</h2><ol>{nxt}</ol></div>
    </aside>
  </div>
</section>
{band(lang)}</main>
"""


# ------------------------------------------------------------------ jsonld
def ld(data):
    return "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n' for d in data)


def org():
    return {"@context": "https://schema.org", "@type": "Organization", "name": "EIGENKERN", "url": SITE["url"] + "/",
            "logo": SITE["url"] + "/assets/img/brand/logo-mark.svg", "email": SITE["email"], "telephone": SITE["phone"],
            "address": {"@type": "PostalAddress", "addressLocality": "Berlin", "addressCountry": "DE"},
            "sameAs": [SITE["linkedin"], SITE["youtube"], SITE["x"]]}


def jsonld_home(lang):
    t = T[lang]
    base = SITE["url"] + ("" if lang == "de" else "/en")
    return ld([
        org(),
        {"@context": "https://schema.org", "@type": "Product", "name": t["schema"]["product"], "description": t["meta"]["desc"],
         "brand": {"@type": "Brand", "name": "EIGENKERN"},
         "offers": [{"@type": "Offer", "name": t["pricing"]["license"], "price": "9900", "priceCurrency": "EUR", "url": base + "/#preise"},
                    {"@type": "Offer", "name": t["pricing"]["care"], "price": "99", "priceCurrency": "EUR", "url": base + "/#preise"}]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in t["faq"]["items"]]},
    ])


def jsonld_contact(lang):
    t = T[lang]
    c = t["contact"]
    return ld([
        org(),
        {"@context": "https://schema.org", "@type": "ContactPage", "name": c["schema_name"], "url": page_url(lang, "contact"),
         "inLanguage": lang, "about": {"@type": "Organization", "name": "EIGENKERN"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": c["crumb_home"], "item": page_url(lang, "index")},
            {"@type": "ListItem", "position": 2, "name": c["label"], "item": page_url(lang, "contact")}]},
    ])


# ------------------------------------------------------------------ writers
def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def out_path(lang, key):
    f = page_file(lang, key)
    return f if lang == "de" else f"en/{f}"


def build_home(lang):
    t = T[lang]
    out = head(lang, "index", t["meta"]["title"], t["meta"]["desc"], pre(lang), extra=jsonld_home(lang))
    write(out_path(lang, "index"), out + header(lang, "index") + home_main(lang) + footer(lang, "index"))


def build_contact(lang):
    c = T[lang]["contact"]
    out = head(lang, "contact", c["meta_title"], c["meta_desc"], pre(lang), extra=jsonld_contact(lang))
    write(out_path(lang, "contact"), out + header(lang, "contact") + contact_main(lang) + footer(lang, "contact"))


def build_legal(lang, key):
    t = T[lang]
    L = t["legal"][key]
    body = LEGAL[lang][key]
    sections = "".join(f"<h2>{esc(h)}</h2><p>{esc(p)}</p>" for h, p in body["sections"])
    out = head(lang, key, f"{L['label']} – EIGENKERN", body["intro"], pre(lang), noindex=True)
    out += header(lang, key)
    out += f"""<main id="main" class="legal"><div class="container legal-wrap">
<h1>{esc(L['label'])}</h1>
<p class="notice">{esc(LEGAL[lang]['notice'])}</p>
<p>{esc(body['intro'])}</p>{sections}
<p><a class="link-arrow" href="index.html">{esc(t['back'])} {icon('arrow-right', 'i i-sm')}</a></p>
</div></main>
"""
    write(out_path(lang, key), out + footer(lang, key))


def build_seo_files():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key, prio in (("index", "1.0"), ("contact", "0.8")):
        de, en = page_url("de", key), page_url("en", key)
        for loc in (de, en):
            xml.append(f"<url><loc>{loc}</loc>"
                       f'<xhtml:link rel="alternate" hreflang="de" href="{de}"/>'
                       f'<xhtml:link rel="alternate" hreflang="en" href="{en}"/>'
                       f'<xhtml:link rel="alternate" hreflang="x-default" href="{de}"/>'
                       f"<changefreq>monthly</changefreq><priority>{prio if loc == de else str(round(float(prio) - .1, 1))}</priority></url>")
    xml.append("</urlset>")
    write("sitemap.xml", "\n".join(xml) + "\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /build/\n\nSitemap: {SITE['url']}/sitemap.xml\n")


if __name__ == "__main__":
    for lang in ("de", "en"):
        build_home(lang)
        build_contact(lang)
        for key in LEGAL_KEYS:
            build_legal(lang, key)
    build_seo_files()
    print("built")
