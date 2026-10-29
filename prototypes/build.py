#!/usr/bin/env python3
"""Render the four prototype directions from content.py.

  python3 build.py            -> writes a.html b.html c.html d.html next to this file
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

# ---------------------------------------------------------------- A: academic minimal
def variant_a(img):
    css = f'''
/* Layout: one quiet column, ~44rem, text first; serif for reading, sans for labels. */
:root{{--bg:#fdfdfb;--fg:#1c1d1a;--muted:#5d615a;--rule:#dcdfd8;--accent:#1f5f4a;--accent-soft:#e6f0eb;
--serif:"Source Serif 4",Georgia,"Times New Roman",serif;--sans:"Source Sans 3",system-ui,-apple-system,"Segoe UI",sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121413;--fg:#e6e4dd;--muted:#a3a79e;--rule:#2b2f2b;--accent:#7fc3a4;--accent-soft:#1b2b25;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#121413;--fg:#e6e4dd;--muted:#a3a79e;--rule:#2b2f2b;--accent:#7fc3a4;--accent-soft:#1b2b25;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--serif);font-size:17px;line-height:1.6}}
.wrap{{max-width:46rem;margin:0 auto;{GUTTER}padding-block:3rem 4rem}}
a{{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}}
a:hover,a:focus-visible{{border-bottom-color:currentColor}}
a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
header{{display:flex;gap:1.5rem;align-items:flex-start;margin-bottom:2.5rem}}
header img{{width:96px;height:96px;border-radius:50%;object-fit:cover;flex:none}}
header h1{{font-size:2rem;font-weight:600;margin:0;letter-spacing:-.01em;text-wrap:balance}}
.tag{{color:var(--muted);margin:.25rem 0 0;font-style:italic}}
.affil{{font-family:var(--sans);color:var(--muted);font-size:.95rem;margin:.15rem 0 .6rem}}
.links{{display:flex;flex-wrap:wrap;gap:.25rem 1rem;font-family:var(--sans);font-size:.95rem}}
.links a{{color:var(--fg);border-bottom:1px solid var(--rule)}}
.links a:hover{{border-bottom-color:var(--accent);color:var(--accent)}}
.toggle{{margin-left:auto;background:none;border:1px solid var(--rule);color:var(--muted);border-radius:999px;width:2rem;height:2rem;cursor:pointer;font-size:1rem;flex:none}}
section{{margin-top:2.5rem}}
h2{{font-family:var(--sans);font-size:.8rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600;margin:0 0 .9rem;padding-bottom:.4rem;border-bottom:1px solid var(--rule)}}
p{{margin:0 0 1rem}}
.news{{display:grid;grid-template-columns:5.5rem 1fr;gap:.35rem 1rem;margin:0}}
.news dt{{font-family:var(--sans);color:var(--muted);font-size:.9rem;padding-top:.15rem;font-variant-numeric:tabular-nums}}
.news dd{{margin:0;min-width:0}}
.pub{{margin:0 0 1.15rem}}
.pub .t{{font-weight:600}}
.pub .au{{font-family:var(--sans);font-size:.95rem;color:var(--muted)}}
.pub .v{{font-family:var(--sans);font-size:.9rem}}
.pub .v em{{font-style:normal;color:var(--accent)}}
.plinks a{{font-family:var(--sans);font-size:.85rem;margin-left:.6rem;padding:.05rem .45rem;border:1px solid var(--rule);border-radius:4px;color:var(--fg)}}
.plinks a:hover{{border-color:var(--accent);color:var(--accent)}}
.job{{display:grid;grid-template-columns:1fr auto;gap:.1rem 1rem;margin-bottom:1.2rem}}
.job .r{{font-weight:600}}
.job .o{{font-family:var(--sans);color:var(--muted);font-size:.95rem;grid-column:1}}
.job .d{{font-family:var(--sans);color:var(--muted);font-size:.9rem;grid-row:1;grid-column:2;white-space:nowrap;font-variant-numeric:tabular-nums}}
.job ul{{grid-column:1/-1;margin:.3rem 0 0;padding-left:1.1rem}}
.job li{{margin-bottom:.25rem}}
.edu{{margin-bottom:.9rem}} .edu .s{{font-family:var(--sans);color:var(--muted);font-size:.92rem}}
.hon{{margin-bottom:.8rem}} .hon .s{{font-family:var(--sans);color:var(--muted);font-size:.92rem}}
ul.plain{{margin:0;padding-left:1.1rem}}
footer{{margin-top:3rem;font-family:var(--sans);color:var(--muted);font-size:.85rem;border-top:1px solid var(--rule);padding-top:1rem}}
@media (max-width:560px){{header{{flex-wrap:wrap}}header img{{width:72px;height:72px}}.job{{grid-template-columns:1fr}}.job .d{{grid-row:auto;grid-column:1;white-space:normal}}.news{{grid-template-columns:1fr}}.news dt{{padding-top:.4rem}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
'''
    head = f'''<title>{NAME}</title>
{meta(DESC)}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Source+Sans+3:wght@400;600&display=swap"/>
<style>{css}</style>'''
    b = [f'<div class="wrap"><header><img src="{img}" alt="Portrait of {NAME}"/><div style="min-width:0;flex:1">'
         f'<h1>{NAME}</h1><p class="tag">{TAGLINE}</p><p class="affil">{AFFIL}</p>{links_html()}</div>{TOGGLE}</header>']
    b.append('<section id="about"><h2>About</h2>' + "".join(f"<p>{p}</p>" for p in BIO) + "</section>")
    b.append('<section id="news"><h2>News</h2><dl class="news">' + "".join(f"<dt>{d}</dt><dd>{t}</dd>" for d, t in NEWS) + "</dl></section>")
    b.append('<section id="publications"><h2>Publications</h2>' + "".join(
        f'<div class="pub"><div class="t">{t}</div><div class="au">{me(a)}</div><div class="v"><em>{v}</em>, {y}{pub_links(l)}</div></div>'
        for t, a, v, y, l, _ in PUBS) + "</section>")
    b.append('<section id="experience"><h2>Experience</h2>' + "".join(
        f'<div class="job"><div class="r">{t}</div><div class="d">{d}</div><div class="o">{org(o, lk)}, {loc}</div><ul>' + "".join(f"<li>{x}</li>" for x in bl) + "</ul></div>"
        for t, o, loc, d, bl, lk in EXPERIENCE) + "</section>")
    b.append('<section id="education"><h2>Education</h2>' + "".join(
        f'<div class="edu"><div><strong>{t}</strong>, {o} <span class="s">· {d}</span></div><div class="s">{n}</div></div>' for t, o, d, n in EDUCATION) + "</section>")
    b.append('<section id="honors"><h2>Honors</h2>' + "".join(
        f'<div class="hon"><div><strong>{t}</strong> <span class="s">· {d}</span></div><div class="s">{n}</div></div>' for t, d, n in HONORS) + "</section>")
    b.append('<section id="interests"><h2>Interests</h2><ul class="plain">' + "".join(f"<li>{i}</li>" for i in INTERESTS) + f"</ul><p style=\"margin-top:1rem\">{OUTSIDE}</p></section>")
    b.append(f'<footer>{NAME} · Last updated October 2026</footer></div>{THEME_JS}')
    return head, "".join(b)

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

# ---------------------------------------------------------------- C: research-first, interactive
def variant_c(img):
    css = f'''
/* Layout: single column with a working diagram up top, filterable publications, and dense data labels in mono. */
:root{{--bg:#fbfbfd;--fg:#171a21;--muted:#5f6675;--rule:#dfe2ea;--accent:#2b4c7e;--accent-soft:#e4eaf5;--chip:#eef0f5;--chip-on:#2b4c7e;--chip-on-fg:#fff;--node:#ffffff;
--sans:"Manrope",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0f1117;--fg:#e6e8ee;--muted:#9aa2b3;--rule:#272c38;--accent:#8fb0e6;--accent-soft:#1a2335;--chip:#1c212c;--chip-on:#8fb0e6;--chip-on-fg:#0f1117;--node:#161a23;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0f1117;--fg:#e6e8ee;--muted:#9aa2b3;--rule:#272c38;--accent:#8fb0e6;--accent-soft:#1a2335;--chip:#1c212c;--chip-on:#8fb0e6;--chip-on-fg:#0f1117;--node:#161a23;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:16.5px;line-height:1.6}}
a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
a:focus-visible,button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.wrap{{max-width:52rem;margin:0 auto;{GUTTER}padding-block:3rem 4rem}}
.top{{display:flex;gap:1.5rem;align-items:center;flex-wrap:wrap}}
.top img{{width:88px;height:88px;border-radius:14px;object-fit:cover;flex:none}}
h1{{font-size:2.1rem;font-weight:800;letter-spacing:-.02em;margin:0;line-height:1.1}}
.tag{{color:var(--muted);margin:.3rem 0 .6rem}}
.links{{display:flex;flex-wrap:wrap;gap:.4rem}}
.links a{{font-family:var(--mono);font-size:.78rem;padding:.25rem .6rem;border:1px solid var(--rule);border-radius:6px;color:var(--fg)}}
.links a:hover{{border-color:var(--accent);color:var(--accent);text-decoration:none}}
.toggle{{margin-left:auto;background:none;border:1px solid var(--rule);color:var(--muted);border-radius:8px;width:2rem;height:2rem;cursor:pointer;align-self:flex-start}}
section{{margin-top:3rem}}
.lbl{{font-family:var(--mono);font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:600;margin:0 0 .8rem}}
h2{{font-size:1.45rem;font-weight:800;letter-spacing:-.015em;margin:0 0 1rem}}
p{{margin:0 0 1rem}}
.diagram{{overflow-x:auto;margin:1rem 0 1.2rem;border:1px solid var(--rule);border-radius:12px;background:var(--accent-soft)}}
.diagram svg{{display:block;width:100%;min-width:560px;height:auto}}
.node{{fill:var(--node);stroke:var(--accent);stroke-width:1.5}}
.ntext{{font-family:var(--sans);font-weight:800;font-size:17px;fill:var(--fg)}}
.nsub{{font-family:var(--mono);font-size:11px;fill:var(--muted)}}
.arrow{{stroke:var(--accent);stroke-width:2;fill:none}}
.loopgrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}}
.loopgrid div{{min-width:0;font-size:.93rem}}
.loopgrid b{{display:block;font-family:var(--mono);font-size:.78rem;color:var(--accent);margin-bottom:.2rem}}
.news{{display:grid;grid-template-columns:6rem 1fr;gap:.45rem 1rem;margin:0}}
.news dt{{font-family:var(--mono);font-size:.8rem;color:var(--muted);padding-top:.25rem}}
.news dd{{margin:0;min-width:0}}
.chips{{display:flex;flex-wrap:wrap;gap:.45rem;margin-bottom:1.2rem}}
.chip{{font-family:var(--mono);font-size:.76rem;padding:.3rem .7rem;border-radius:999px;border:1px solid var(--rule);background:var(--chip);color:var(--fg);cursor:pointer}}
.chip[aria-pressed="true"]{{background:var(--chip-on);color:var(--chip-on-fg);border-color:var(--chip-on)}}
.pub{{display:grid;grid-template-columns:4.2rem 1fr;gap:.2rem 1rem;padding:.9rem 0;border-top:1px solid var(--rule)}}
.pub:last-child{{border-bottom:1px solid var(--rule)}}
.pub[hidden]{{display:none}}
.pub .y{{font-family:var(--mono);font-size:.85rem;color:var(--muted);padding-top:.2rem}}
.pub .t{{font-weight:700;line-height:1.35}}
.pub .au{{font-size:.9rem;color:var(--muted);grid-column:2}}
.pub .m{{grid-column:2;display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;font-size:.82rem;margin-top:.25rem}}
.venue{{font-family:var(--mono);background:var(--accent-soft);color:var(--accent);padding:.12rem .5rem;border-radius:4px}}
.topic{{font-family:var(--mono);color:var(--muted)}}
.plinks a{{font-family:var(--mono);font-size:.78rem;padding:.15rem .5rem;border:1px solid var(--rule);border-radius:4px;margin-right:.35rem;color:var(--fg)}}
.plinks a:hover{{border-color:var(--accent);color:var(--accent);text-decoration:none}}
.job{{display:grid;grid-template-columns:7.5rem 1fr;gap:.1rem 1rem;padding:.8rem 0;border-top:1px solid var(--rule)}}
.job .d{{font-family:var(--mono);font-size:.78rem;color:var(--muted);padding-top:.3rem}}
.job .r{{font-weight:700}} .job .o{{grid-column:2;color:var(--muted);font-size:.92rem}}
.job ul{{grid-column:2;margin:.3rem 0 0;padding-left:1.1rem;font-size:.95rem}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:2rem}} .two>div{{min-width:0}}
.item{{margin-bottom:.9rem;font-size:.95rem}} .item .s{{color:var(--muted);font-size:.88rem}}
ul.plain{{margin:0;padding-left:1.1rem;columns:2;column-gap:2rem}}
footer{{margin-top:3.5rem;font-family:var(--mono);font-size:.78rem;color:var(--muted)}}
@media (max-width:760px){{.loopgrid{{grid-template-columns:1fr 1fr}}.two{{grid-template-columns:1fr}}ul.plain{{columns:1}}}}
@media (max-width:560px){{.news,.pub,.job{{grid-template-columns:1fr}}.pub .au,.pub .m,.job .o,.job ul{{grid-column:1}}.loopgrid{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
'''
    head = f'''<title>{NAME}</title>
{meta(DESC)}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&family=JetBrains+Mono:wght@400;600&display=swap"/>
<style>{css}</style>'''
    # diagram: four nodes in a row, forward arrows, return arrow underneath
    xs = [12, 202, 392, 582]; w, h, y = 166, 58, 18
    svg = ['<svg viewBox="0 0 760 150" role="img" aria-label="Loop: evaluate, generate, train, benchmark, and back to evaluate">',
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor" style="color:var(--accent)"/></marker></defs>']
    subs = ["evals · failure analysis", "agents · verifiable data", "SFT · RLHF · RLVR · pretrain", "metrics · ablations"]
    for i, (x, (name, _)) in enumerate(zip(xs, LOOP)):
        svg.append(f'<rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
                   f'<text class="ntext" x="{x+w/2}" y="{y+25}" text-anchor="middle">{name}</text>'
                   f'<text class="nsub" x="{x+w/2}" y="{y+44}" text-anchor="middle">{subs[i]}</text>')
        if i < 3:
            svg.append(f'<line class="arrow" x1="{x+w}" y1="{y+h/2}" x2="{xs[i+1]-2}" y2="{y+h/2}" marker-end="url(#ah)"/>')
    svg.append(f'<path class="arrow" d="M{xs[3]+w/2} {y+h} V118 H{xs[0]+w/2} V{y+h+2}" marker-end="url(#ah)"/>')
    svg.append(f'<text class="nsub" x="380" y="134" text-anchor="middle">repeat until the benchmark moves</text></svg>')
    topics = ["All"] + sorted({t for *_, ts in PUBS for t in ts}, key=lambda s: ["Reasoning","Evaluation","Post-training","Reinforcement Learning","Materials"].index(s))
    b = [f'<div class="wrap"><div class="top"><img src="{img}" alt="Portrait of {NAME}"/><div style="min-width:0;flex:1"><h1>{NAME}</h1><p class="tag">{TAGLINE} · {AFFIL}</p>{links_html()}</div>{TOGGLE}</div>']
    b.append('<section id="about"><p class="lbl">About</p>' + "".join(f"<p>{p}</p>" for p in BIO) + "</section>")
    b.append('<section id="loop"><p class="lbl">How I work</p><h2>One loop, run end to end</h2><div class="diagram">' + "".join(svg) + '</div><div class="loopgrid">' +
             "".join(f"<div><b>{i+1:02d} {n}</b>{d}</div>" for i, (n, d) in enumerate(LOOP)) + "</div></section>")
    b.append('<section id="news"><p class="lbl">News</p><dl class="news">' + "".join(f"<dt>{d}</dt><dd>{t}</dd>" for d, t in NEWS) + "</dl></section>")
    chips = "".join(f'<button type="button" class="chip" data-topic="{t}" aria-pressed="{str(t=="All").lower()}">{t}</button>' for t in topics)
    pubs = "".join(f'<article class="pub" data-topics="{"|".join(ts)}"><div class="y">{y}</div><div class="t">{t}</div><div class="au">{me(a)}</div>'
                   f'<div class="m"><span class="venue">{v}</span>{topic_tags(ts)}{pub_links(l)}</div></article>'
                   for t, a, v, y, l, ts in PUBS)
    b.append(f'<section id="publications"><p class="lbl">Publications</p><div class="chips" id="chips">{chips}</div><div id="publist">{pubs}</div></section>')
    b.append('<section id="experience"><p class="lbl">Experience</p>' + "".join(
        f'<div class="job"><div class="d">{d}</div><div class="r">{t}</div><div class="o">{org(o, lk)} · {loc}</div><ul>' + "".join(f"<li>{x}</li>" for x in bl) + "</ul></div>"
        for t, o, loc, d, bl, lk in EXPERIENCE) + "</section>")
    b.append('<section><div class="two"><div><p class="lbl">Education</p>' + "".join(
        f'<div class="item"><strong>{t}</strong><div class="s">{o} · {d}</div><div class="s">{n}</div></div>' for t, o, d, n in EDUCATION) +
        '</div><div><p class="lbl">Honors</p>' + "".join(f'<div class="item"><strong>{t}</strong><div class="s">{d} · {n}</div></div>' for t, d, n in HONORS) + "</div></div></section>")
    b.append('<section id="interests"><p class="lbl">Interests</p><ul class="plain">' + "".join(f"<li>{i}</li>" for i in INTERESTS) + f"</ul><p style=\"margin-top:1rem\">{OUTSIDE}</p></section>")
    b.append(f'<footer>{NAME} · last updated 2026-10 · <a href="{CV}">CV</a></footer></div>')
    b.append(THEME_JS + '''<script>
(function(){var chips=document.getElementById('chips'),list=document.getElementById('publist');if(!chips)return;
chips.addEventListener('click',function(e){var c=e.target.closest('.chip');if(!c)return;var t=c.getAttribute('data-topic');
chips.querySelectorAll('.chip').forEach(function(x){x.setAttribute('aria-pressed',String(x===c))});
list.querySelectorAll('.pub').forEach(function(p){p.hidden=!(t==='All'||p.getAttribute('data-topics').split('|').indexOf(t)>-1)});});})();
</script>''')
    return head, "".join(b)

# ---------------------------------------------------------------- D: the current layout, modernized
def variant_d(img):
    css = f'''
/* Layout: the existing fixed sidebar-with-portrait idea, rebuilt without Bootstrap; warmer type, dark mode, denser content. */
:root{{--bg:#fffdf9;--fg:#231f1b;--muted:#6b625a;--rule:#e6dfd6;--side:#b5532f;--side-fg:#fff5ee;--side-muted:#f3c9b5;--accent:#a3461f;--soft:#f6ece4;
--sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--serif:"IBM Plex Serif",Georgia,serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#15120f;--fg:#ebe4dc;--muted:#a79c91;--rule:#2d2622;--side:#7e3519;--side-fg:#fff5ee;--side-muted:#e9b89f;--accent:#e58b63;--soft:#241c17;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#15120f;--fg:#ebe4dc;--muted:#a79c91;--rule:#2d2622;--side:#7e3519;--side-fg:#fff5ee;--side-muted:#e9b89f;--accent:#e58b63;--soft:#241c17;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:16.5px;line-height:1.6}}
a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
a:focus-visible,button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.side{{position:fixed;top:0;left:0;bottom:0;width:17rem;background:var(--side);color:var(--side-fg);display:flex;flex-direction:column;align-items:center;gap:.4rem;padding-block:2.5rem;padding-left:max(1rem,env(safe-area-inset-left,0px));padding-right:1rem;text-align:center;overflow:auto}}
.side img{{width:150px;height:150px;border-radius:50%;object-fit:cover;border:5px solid rgba(255,255,255,.25);margin-bottom:.8rem}}
.side .nm{{font-family:var(--serif);font-size:1.5rem;font-weight:600;line-height:1.15}}
.side nav{{display:flex;flex-direction:column;gap:.15rem;margin-top:1.2rem;width:100%}}
.side nav a{{color:var(--side-fg);text-transform:uppercase;letter-spacing:.12em;font-size:.8rem;font-weight:600;padding:.45rem;border-radius:6px}}
.side nav a:hover{{background:rgba(255,255,255,.12);text-decoration:none}}
.side .soc{{display:flex;gap:.6rem;flex-wrap:wrap;justify-content:center;margin-top:auto;padding-top:1.5rem}}
.side .soc a{{color:var(--side-fg);font-size:.8rem;border:1px solid rgba(255,255,255,.35);padding:.25rem .6rem;border-radius:999px}}
.side .soc a:hover{{background:var(--side-fg);color:var(--side);text-decoration:none}}
.toggle{{background:none;border:1px solid rgba(255,255,255,.35);color:var(--side-fg);border-radius:999px;width:2rem;height:2rem;cursor:pointer;margin-top:.8rem}}
.main{{margin-left:17rem;{GUTTER}padding-left:max(3.5rem,env(safe-area-inset-left,0px));padding-right:max(3rem,env(safe-area-inset-right,0px));padding-block:3rem 5rem}}
.inner{{max-width:46rem}}
h1{{font-family:var(--serif);font-size:2.6rem;font-weight:600;line-height:1.1;margin:0 0 .3rem;letter-spacing:-.01em}}
h1 span{{color:var(--accent)}}
.sub{{color:var(--muted);margin:0 0 1.5rem}}
.lead{{font-size:1.08rem}}
section{{margin-top:3rem;padding-top:2rem;border-top:1px solid var(--rule)}}
h2{{font-family:var(--serif);font-size:1.7rem;font-weight:600;margin:0 0 1.2rem;letter-spacing:-.01em}}
p{{margin:0 0 1rem}}
.news{{display:grid;grid-template-columns:5.5rem 1fr;gap:.5rem 1rem;margin:0}}
.news dt{{color:var(--accent);font-weight:600;font-size:.9rem;font-variant-numeric:tabular-nums;padding-top:.1rem}}
.news dd{{margin:0;min-width:0}}
.job{{display:grid;grid-template-columns:1fr auto;gap:.1rem 1.5rem;margin-bottom:1.6rem}}
.job .r{{font-family:var(--serif);font-size:1.2rem;font-weight:600}}
.job .o{{color:var(--muted);grid-column:1;font-size:.95rem}}
.job .d{{grid-row:1;grid-column:2;color:var(--accent);font-weight:600;font-size:.9rem;white-space:nowrap;font-variant-numeric:tabular-nums}}
.job ul{{grid-column:1/-1;margin:.4rem 0 0;padding-left:1.1rem;font-size:.97rem}}
.pub{{padding:.9rem 1rem;border-radius:8px;margin-bottom:.6rem;background:var(--soft)}}
.pub .t{{font-weight:600}} .pub .au{{font-size:.9rem;color:var(--muted)}}
.pub .v{{font-size:.88rem;margin-top:.2rem}} .pub .v em{{font-style:normal;color:var(--accent);font-weight:600}}
.plinks a{{font-size:.82rem;margin-left:.5rem;padding:.1rem .5rem;border:1px solid var(--rule);border-radius:4px;color:var(--fg);background:var(--bg)}}
.plinks a:hover{{border-color:var(--accent);color:var(--accent);text-decoration:none}}
.item{{margin-bottom:1rem}} .item .s{{color:var(--muted);font-size:.9rem}} .item .r{{font-family:var(--serif);font-weight:600;font-size:1.1rem}}
ul.plain{{margin:0;padding-left:1.1rem}}
footer{{margin-top:3rem;color:var(--muted);font-size:.85rem}}
@media (max-width:860px){{.side{{position:static;width:auto;flex-direction:row;flex-wrap:wrap;justify-content:center;align-items:center;gap:.6rem 1rem;padding-block:1.2rem;padding-right:max(1rem,env(safe-area-inset-right,0px));text-align:left}}.side img{{width:56px;height:56px;margin:0;border-width:2px}}.side nav{{flex-direction:row;flex-wrap:wrap;justify-content:center;margin:0;width:auto}}.side .soc{{margin:0;padding:0}}.toggle{{margin:0}}.main{{margin-left:0;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:2rem 4rem}}}}
@media (max-width:560px){{.job{{grid-template-columns:1fr}}.job .d{{grid-row:auto;grid-column:1;white-space:normal}}.news{{grid-template-columns:1fr}}h1{{font-size:2.1rem}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
'''
    head = f'''<title>{NAME}</title>
{meta(DESC)}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Serif:wght@600&display=swap"/>
<style>{css}</style>'''
    secs = [("about","About"),("news","News"),("experience","Experience"),("publications","Publications"),("education","Education"),("honors","Honors"),("interests","Interests")]
    side = (f'<aside class="side"><img src="{img}" alt="Portrait of {NAME}"/><div class="nm">{NAME}</div><nav>' +
            "".join(f'<a href="#{i}">{l}</a>' for i, l in secs) + '</nav><div class="soc">' +
            f'<a href="{CV}">CV</a>' + "".join(f'<a href="{u}">{l}</a>' for l, u in LINKS) + f'</div>{TOGGLE}</aside>')
    m = ['<main class="main"><div class="inner">']
    m.append(f'<div id="about"><h1>Hamed <span>Mahdavi</span></h1><p class="sub">{AFFIL} · <a href="mailto:{EMAIL}">{EMAIL}</a></p>' + "".join(f'<p class="lead">{p}</p>' for p in BIO) + "</div>")
    m.append('<section id="news"><h2>News</h2><dl class="news">' + "".join(f"<dt>{d}</dt><dd>{t}</dd>" for d, t in NEWS) + "</dl></section>")
    m.append('<section id="experience"><h2>Experience</h2>' + "".join(
        f'<div class="job"><div class="r">{t}</div><div class="d">{d}</div><div class="o">{org(o, lk)} · {loc}</div><ul>' + "".join(f"<li>{x}</li>" for x in bl) + "</ul></div>"
        for t, o, loc, d, bl, lk in EXPERIENCE) + "</section>")
    m.append('<section id="publications"><h2>Publications</h2>' + "".join(
        f'<div class="pub"><div class="t">{t}</div><div class="au">{me(a)}</div><div class="v"><em>{v}</em>, {y}{pub_links(l)}</div></div>' for t, a, v, y, l, _ in PUBS) + "</section>")
    m.append('<section id="education"><h2>Education</h2>' + "".join(
        f'<div class="item"><div class="r">{t}</div><div class="s">{o} · {d}</div><div class="s">{n}</div></div>' for t, o, d, n in EDUCATION) + "</section>")
    m.append('<section id="honors"><h2>Honors and Awards</h2>' + "".join(
        f'<div class="item"><div class="r">{t}</div><div class="s">{d} · {n}</div></div>' for t, d, n in HONORS) + "</section>")
    m.append('<section id="interests"><h2>Interests</h2><ul class="plain">' + "".join(f"<li>{i}</li>" for i in INTERESTS) + f"</ul><p style=\"margin-top:1rem\">{OUTSIDE}</p></section>")
    m.append(f'<footer>{NAME} · Last updated October 2026</footer></div></main>')
    return head, side + "".join(m) + THEME_JS

VARIANTS = {"a": variant_a, "b": variant_b, "c": variant_c, "d": variant_d}

def full_doc(head, body):
    return f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>\n<link rel="icon" href="../dist/assets/img/favicon.ico"/>\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'

TITLES = {"a": "Direction A Academic Minimal", "b": "Direction B Editorial", "c": "Direction C Research First", "d": "Direction D Sidebar Modernized"}

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
