#!/usr/bin/env python3
"""Render the Direction B prototype from content.py.

  python3 build.py            -> writes b.html next to this file
  python3 build.py --fragment DIR OUT  -> writes an artifact fragment (no doctype/html/head/body,
                                          profile photo inlined) for preview publishing
"""
import base64, html, os, sys
from content import *

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_REL = "../dist/assets/img/profile.jpg"
SITE = "https://hamedmahdavi72.github.io/"

def me(authors):
    return authors.replace("H. Mahdavi", "<strong>H. Mahdavi</strong>")

def meta(desc):
    d = html.escape(desc, quote=True)
    return f'''<meta name="description" content="{d}"/>
<meta property="og:type" content="profile"/>
<meta property="og:title" content="{NAME}"/>
<meta property="og:description" content="{d}"/>
<meta property="og:url" content="{SITE}"/>
<meta property="og:image" content="{SITE}dist/assets/img/profile.jpg"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:site" content="@hamedmahdavi93"/>'''

DESC = ("Hamed Mahdavi is a Ph.D. candidate at Penn State working on LLM reasoning, post-training, "
        "evaluation, and synthetic data. Previously at Prelude and a collaborator on Gemini IMO 2025.")

THEME_JS = '''<script>
(function(){var r=document.documentElement;
try{var t=localStorage.getItem('theme');if(t==='dark'||t==='light')r.setAttribute('data-theme',t)}catch(e){}
document.addEventListener('click',function(e){var b=e.target.closest('[data-toggle-theme]');if(!b)return;
var cur=r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
var n=cur==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}});
})();
</script>'''

TOGGLE = '<button type="button" class="toggle" data-toggle-theme aria-label="Switch color theme">◐</button>'

GUTTER = "padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));"

def links_html(cls="links", with_cv=True, with_email=True):
    items = [f'<a href="{u}">{l}</a>' for l, u in LINKS]
    if with_cv: items.insert(0, f'<a href="{CV}">CV</a>')
    if with_email: items.append(f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    return f'<nav class="{cls}">' + "".join(items) + "</nav>"

def org(o, lk):
    return f'<a href="{lk}">{o}</a>' if lk else o

def topic_tags(ts):
    return "".join(f'<span class="topic">#{x.replace(" ", "-")}</span>' for x in ts)

def pub_links(links, cls="plinks"):
    return f'<span class="{cls}">' + "".join(f'<a href="{u}">{l}</a>' for l, u in links.items()) + "</span>"

# ---------------------------------------------------------------- B: editorial two-column
def variant_b(img):
    css = f'''
/* Layout: sticky slate identity column on the left, paper content column on the right. */
:root{{--paper:#f4f5f7;--ink:#1b1f26;--muted:#5b6370;--rule:#d8dce3;--slate:#1e2430;--slate-fg:#eef0f4;--slate-muted:#9aa3b2;
--accent:#9a6a12;--accent-on-slate:#d9a441;--card:#ffffff;--badge:#e9edf3;
--display:"Fraunces",Georgia,serif;--body:"Figtree",system-ui,-apple-system,"Segoe UI",sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#15181d;--ink:#e8eaee;--muted:#9aa3b2;--rule:#2a303a;--slate:#0f1217;--card:#1c2128;--badge:#262c36;--accent:#d9a441;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#15181d;--ink:#e8eaee;--muted:#9aa3b2;--rule:#2a303a;--slate:#0f1217;--card:#1c2128;--badge:#262c36;--accent:#d9a441;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:16.5px;line-height:1.6}}
a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
a:focus-visible,button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.page{{display:grid;grid-template-columns:minmax(300px,360px) 1fr;min-height:100vh}}
.side{{background:var(--slate);color:var(--slate-fg);position:sticky;top:0;height:100vh;overflow:auto;{GUTTER}padding-block:3rem;padding-left:max(2.5rem,env(safe-area-inset-left,0px))}}
.side img{{width:132px;height:132px;border-radius:50%;object-fit:cover;border:3px solid var(--accent-on-slate)}}
.side h1{{font-family:var(--display);font-weight:500;font-size:2.5rem;line-height:1.05;margin:1.4rem 0 .4rem;letter-spacing:-.01em;text-wrap:balance}}
.side .tag{{color:var(--slate-muted);margin:0 0 1.4rem;font-size:1.02rem}}
.side p{{font-size:.97rem;color:var(--slate-fg);opacity:.9}}
.side a{{color:var(--accent-on-slate)}}
.pills{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1.4rem 0}}
.pills a{{font-size:.85rem;padding:.35rem .8rem;border:1px solid rgba(255,255,255,.22);border-radius:999px;color:var(--slate-fg);text-decoration:none}}
.pills a:hover{{border-color:var(--accent-on-slate);color:var(--accent-on-slate)}}
.pills a.cv{{background:var(--accent-on-slate);color:var(--slate);border-color:var(--accent-on-slate);font-weight:600}}
.email{{font-size:.9rem;color:var(--slate-muted);word-break:break-all}}
.toggle{{position:absolute;top:1rem;right:1rem;background:none;border:1px solid rgba(255,255,255,.25);color:var(--slate-fg);border-radius:999px;width:2rem;height:2rem;cursor:pointer}}
.main{{min-width:0;{GUTTER}padding-block:3.5rem 5rem;padding-left:max(3.5rem,env(safe-area-inset-left,0px));padding-right:max(3.5rem,env(safe-area-inset-right,0px))}}
.inner{{max-width:48rem}}
.hero h2{{font-family:var(--display);font-weight:500;font-size:clamp(1.9rem,3.2vw,2.7rem);line-height:1.15;margin:0 0 1rem;letter-spacing:-.015em;text-wrap:balance}}
.hero h2 em{{font-style:italic;color:var(--accent)}}
.hero p{{font-size:1.08rem;max-width:40rem}}
section{{margin-top:3.5rem}}
h3.sec{{font-family:var(--display);font-weight:500;font-size:1.65rem;margin:0 0 1.2rem;display:flex;align-items:baseline;gap:1rem}}
h3.sec::after{{content:"";flex:1;height:1px;background:var(--rule)}}
.news{{display:grid;grid-template-columns:6rem 1fr;gap:.6rem 1rem;margin:0;position:relative}}
.news dt{{color:var(--muted);font-size:.9rem;font-variant-numeric:tabular-nums;padding-top:.1rem}}
.news dt::before{{content:"";display:inline-block;width:.5rem;height:.5rem;border-radius:50%;background:var(--accent);margin-right:.6rem;vertical-align:middle}}
.news dd{{margin:0;min-width:0}}
.cards{{display:grid;gap:.9rem}}
.card{{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:1.1rem 1.25rem;display:grid;gap:.35rem}}
.card .top{{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;font-size:.8rem}}
.badge{{background:var(--badge);color:var(--ink);padding:.15rem .55rem;border-radius:4px;font-weight:600;letter-spacing:.03em}}
.year{{color:var(--muted);font-variant-numeric:tabular-nums}}
.card .t{{font-family:var(--display);font-weight:500;font-size:1.15rem;line-height:1.3}}
.card .au{{font-size:.92rem;color:var(--muted)}}
.plinks{{display:flex;gap:.5rem;margin-top:.3rem}}
.plinks a{{font-size:.82rem;font-weight:600;padding:.3rem .7rem;border-radius:6px;background:var(--badge);color:var(--ink)}}
.plinks a:hover{{background:var(--accent);color:#fff;text-decoration:none}}
.job{{display:grid;grid-template-columns:1fr auto;gap:.15rem 1.5rem;padding:1rem 0 1rem 1.25rem;border-left:2px solid var(--rule)}}
.job:hover{{border-left-color:var(--accent)}}
.job .r{{font-family:var(--display);font-weight:500;font-size:1.15rem}}
.job .o{{color:var(--muted);font-size:.95rem;grid-column:1}}
.job .d{{grid-row:1;grid-column:2;color:var(--muted);font-size:.9rem;white-space:nowrap;font-variant-numeric:tabular-nums}}
.job ul{{grid-column:1/-1;margin:.4rem 0 0;padding-left:1.1rem;font-size:.97rem}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem}}
.two>div{{min-width:0}}
.item{{margin-bottom:1rem}} .item .s{{color:var(--muted);font-size:.9rem}}
ul.plain{{margin:0;padding-left:1.1rem}}
footer{{margin-top:4rem;color:var(--muted);font-size:.85rem}}
@media (max-width:860px){{.page{{grid-template-columns:1fr}}.side{{position:static;height:auto;padding-block:2.5rem;padding-left:max(16px,env(safe-area-inset-left,0px))}}.main{{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:2.5rem 4rem}}.two{{grid-template-columns:1fr}}}}
@media (max-width:560px){{.job{{grid-template-columns:1fr}}.job .d{{grid-row:auto;grid-column:1;white-space:normal}}.news{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
'''
    head = f'''<title>{NAME}</title>
{meta(DESC)}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;1,9..144,500&family=Figtree:wght@400;600&display=swap"/>
<style>{css}</style>'''
    pills = f'<div class="pills"><a class="cv" href="{CV}">Download CV</a>' + "".join(f'<a href="{u}">{l}</a>' for l, u in LINKS) + "</div>"
    side = (f'<aside class="side">{TOGGLE}<img src="{img}" alt="Portrait of {NAME}"/>'
            f'<h1>Hamed<br/>Mahdavi</h1><p class="tag">{TAGLINE}</p><p>{BIO[0]}</p>{pills}<div class="email">{EMAIL}</div></aside>')
    m = ['<main class="main"><div class="inner">']
    m.append('<div class="hero"><h2>Teaching language models to reason, <em>and checking the work.</em></h2>' + "".join(f"<p>{p}</p>" for p in BIO[1:]) + "</div>")
    m.append('<section id="news"><h3 class="sec">News</h3><dl class="news">' + "".join(f"<dt>{d}</dt><dd>{t}</dd>" for d, t in NEWS) + "</dl></section>")
    m.append('<section id="publications"><h3 class="sec">Publications</h3><div class="cards">' + "".join(
        f'<article class="card"><div class="top"><span class="badge">{v}</span><span class="year">{y}</span></div><div class="t">{t}</div><div class="au">{me(a)}</div>{pub_links(l)}</article>'
        for t, a, v, y, l, _ in PUBS) + "</div></section>")
    m.append('<section id="experience"><h3 class="sec">Experience</h3>' + "".join(
        f'<div class="job"><div class="r">{t}</div><div class="d">{d}</div><div class="o">{org(o, lk)} · {loc}</div><ul>' + "".join(f"<li>{x}</li>" for x in bl) + "</ul></div>"
        for t, o, loc, d, bl, lk in EXPERIENCE) + "</section>")
    m.append('<section><div class="two"><div><h3 class="sec">Education</h3>' + "".join(
        f'<div class="item"><strong>{t}</strong><div class="s">{o} · {d}</div><div class="s">{n}</div></div>' for t, o, d, n in EDUCATION) +
        '</div><div><h3 class="sec">Honors</h3>' + "".join(
        f'<div class="item"><strong>{t}</strong><div class="s">{d} · {n}</div></div>' for t, d, n in HONORS) + "</div></div></section>")
    m.append('<section id="interests"><h3 class="sec">Interests</h3><ul class="plain">' + "".join(f"<li>{i}</li>" for i in INTERESTS) + f"</ul><p>{OUTSIDE}</p></section>")
    m.append(f'<footer>{NAME} · Last updated October 2026</footer></div></main>')
    return head, f'<div class="page">{side}{"".join(m)}</div>{THEME_JS}'

VARIANTS = {"b": variant_b}

def full_doc(head, body):
    return f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>\n<link rel="icon" href="../dist/assets/img/favicon.ico"/>\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'

TITLES = {"b": "Direction B Editorial"}

def fragment(head, body, key):
    head = head.replace(f"<title>{NAME}</title>", f"<title>{TITLES[key]}</title>", 1)
    return f'<meta name="claude:viewport-fit-sides" content="cover">\n{head}\n{body}\n'

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fragment":
        key, out = sys.argv[2], sys.argv[3]
        with open(os.path.join(HERE, "..", "dist", "assets", "img", "profile.jpg"), "rb") as f:
            data = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
        head, body = VARIANTS[key](data)
        open(out, "w").write(fragment(head, body, key)); print(out)
    else:
        for k, fn in VARIANTS.items():
            head, body = fn(IMG_REL)
            p = os.path.join(HERE, f"{k}.html"); open(p, "w").write(full_doc(head, body)); print(p)
