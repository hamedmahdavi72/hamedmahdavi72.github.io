#!/usr/bin/env python3
"""Render the site (index.html at the repo root) from content.py.

  python3 build.py            -> writes ../index.html
  python3 build.py --fragment DIR OUT  -> writes an artifact fragment (no doctype/html/head/body,
                                          profile photo inlined) for preview publishing
"""
import base64, html, os, sys
from content import *

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_REL = "dist/assets/img/profile.jpg"
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
        "evaluation, and synthetic data. Previously at a stealth AI startup and a collaborator on Gemini IMO 2025.")

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
    items = [f'<a href="{u}">{l}</a>' for l, u, *_ in LINKS]
    if with_cv: items.insert(0, f'<a href="{CV}">CV</a>')
    if with_email: items.append(f'<a href="mailto:{EMAIL}">{EMAIL}</a>')
    return f'<nav class="{cls}">' + "".join(items) + "</nav>"

def org(o, lk):
    return f'<a href="{lk}">{o}</a>' if lk else o

def topic_tags(ts):
    return "".join(f'<span class="topic">#{x.replace(" ", "-")}</span>' for x in ts)

def pub_links(links, cls="plinks"):
    return f'<span class="{cls}">' + "".join(f'<a href="{u}">{l}</a>' for l, u in links.items()) + "</span>"

# ---------------------------------------------------------------- B: editorial two-column, amber-terminal package
REPO_URL = "https://github.com/hamedmahdavi72/hamedmahdavi72.github.io"

def bibtex(i, t, a, v, y, links):
    first = a.split(",")[0].strip().split()[-1].lower()
    word = "".join(ch for ch in t.split()[0] if ch.isalpha()).lower()
    key = f"{first}{y}{word}"
    authors = " and ".join(x.strip() for x in a.split(","))
    url = next(iter(links.values()))
    if v in ("Preprint", "Submitted to ICLR"):
        kind, venue = "misc", f"  note = {{{v}}},\n"
    elif v == "Digital Discovery":
        kind, venue = "article", f"  journal = {{{v}}},\n"
    else:
        kind, venue = "inproceedings", f"  booktitle = {{{v}}},\n"
    return f"@{kind}{{{key},\n  title = {{{t}}},\n  author = {{{authors}}},\n{venue}  year = {{{y}}},\n  url = {{{url}}}\n}}"

PIXEL = {
 "medal": """
....####....
...#....#...
...#.##.#...
...#....#...
....####....
..xxx..xxx..
..xxxxxxxx..
..xx.xx.xx..
..xxxxxxxx..
...xxxxxx...
....xxxx....
.....xx.....""",
 "trophy": """
.##########.
.#........#.
x#........#x
x#........#x
.#........#.
..#......#..
...######...
.....##.....
.....##.....
....####....
..########..
..########..""",
 "coins": """
............
..########..
.#........#.
.#.xxxxxx.#.
..########..
..########..
.#........#.
.#.xxxxxx.#.
..########..
..########..
.#........#.
..########..""",
 "star": """
.....##.....
.....##.....
....####....
....####....
############
.##########.
..########..
...######...
...##..##...
..##....##..
.#........#.
............""",
}
def pix(name, size=22):
    rows = PIXEL[name].strip("\n").split("\n")
    d = {"#": [], "x": []}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in d: d[ch].append(f"M{x} {y}h1v1h-1z")
    paths = (f'<path fill="var(--accent)" d="{"".join(d["#"])}"/>' if d["#"] else "") + (f'<path fill="var(--muted)" d="{"".join(d["x"])}"/>' if d["x"] else "")
    return f'<svg class="pix" viewBox="0 0 12 12" width="{size}" height="{size}" shape-rendering="crispEdges" aria-hidden="true">{paths}</svg>'

with open(os.path.join(HERE, "..", "dist", "assets", "img", "profile-pixel.png"), "rb") as _f:
    PIXEL_PORTRAIT = "data:image/png;base64," + base64.b64encode(_f.read()).decode()

def variant_b(img):
    css = f'''
/* Layout: sticky slate identity column (amber on slate, like an amber phosphor terminal) beside a graph-paper content column. */
:root{{--paper:#f7f7f8;--ink:#16181d;--muted:#5d626c;--rule:#e3e4e8;--grid:rgba(22,24,29,.06);--slate:#0e1013;--slate-2:#15181d;--slate-fg:#e8e9ec;--slate-muted:#8b909a;--hair:rgba(255,255,255,.08);--tile:rgba(255,255,255,.05);
--accent:#9a6a12;--accent-on-slate:#e6ab3c;--card:#ffffff;--badge:#eef0f3;
--display:"Fraunces",Georgia,serif;--body:"Figtree",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#111318;--ink:#e8e9ec;--muted:#8b909a;--rule:#262a31;--grid:rgba(232,233,236,.045);--slate:#0a0b0e;--slate-2:#101217;--card:#171a20;--badge:#21252d;--accent:#e6ab3c;color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#111318;--ink:#e8e9ec;--muted:#8b909a;--rule:#262a31;--grid:rgba(232,233,236,.045);--slate:#0a0b0e;--slate-2:#101217;--card:#171a20;--badge:#21252d;--accent:#e6ab3c;color-scheme:dark}}
/* Konami: green phosphor mode, wins over both themes */
:root.phosphor,:root.phosphor[data-theme]{{--slate-2:#041004;--hair:rgba(157,255,157,.15);--tile:rgba(157,255,157,.06);--paper:#050c06;--ink:#9dff9d;--muted:#5fbf5f;--rule:#1d3a1d;--grid:rgba(157,255,157,.08);--slate:#020602;--slate-fg:#9dff9d;--slate-muted:#5fbf5f;--accent:#9dff9d;--accent-on-slate:#9dff9d;--card:#0a1a0a;--badge:#143014;color-scheme:dark}}
:root.phosphor body{{text-shadow:0 0 .6px currentColor}}
:root.phosphor body::after{{content:"";position:fixed;inset:0;pointer-events:none;z-index:40;background:repeating-linear-gradient(0deg,rgba(0,0,0,.22) 0 1px,transparent 1px 3px),radial-gradient(ellipse at center,transparent 60%,rgba(0,0,0,.55) 100%)}}
:root.phosphor .side img{{filter:grayscale(1) sepia(1) hue-rotate(70deg) saturate(3) contrast(1.1)}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:16.5px;line-height:1.6}}
a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
a:focus-visible,button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.page{{display:grid;grid-template-columns:minmax(300px,360px) 1fr;min-height:100vh}}
.side{{background:linear-gradient(180deg,var(--slate),var(--slate-2));box-shadow:inset -1px 0 0 var(--hair);color:var(--slate-fg);position:sticky;isolation:isolate;top:0;height:100vh;overflow:auto;scrollbar-width:none;{GUTTER}padding-block:2.5rem;padding-left:max(2.5rem,env(safe-area-inset-left,0px))}}
.side::before{{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(70% 45% at 15% 0%,color-mix(in srgb,var(--accent-on-slate) 16%,transparent),transparent 70%)}}
.side::-webkit-scrollbar{{display:none}}
.side img{{width:112px;height:112px;border-radius:50%;object-fit:cover;border:2px solid var(--hair);box-shadow:0 0 0 1px var(--slate),0 8px 30px rgba(0,0,0,.45)}}
.side h1{{font-family:var(--display);font-weight:500;font-size:2.3rem;line-height:1.05;margin:1.1rem 0 .35rem;letter-spacing:-.01em;text-wrap:balance}}
.side .tag{{color:var(--slate-muted);margin:0 0 .9rem;font-size:.98rem}}
.status{{display:inline-flex;align-items:center;gap:.55rem;font-family:var(--mono);font-size:.78rem;color:var(--slate-fg);border:1px solid var(--hair);background:var(--tile);border-radius:999px;padding:.35rem .8rem .35rem .6rem;margin-bottom:1.2rem}}
.status .dot{{width:.55rem;height:.55rem;border-radius:50%;background:var(--accent-on-slate);box-shadow:0 0 0 0 var(--accent-on-slate);animation:pulse 2.2s ease-out infinite}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 color-mix(in srgb,var(--accent-on-slate) 60%,transparent)}}100%{{box-shadow:0 0 0 .6rem transparent}}}}
.side p{{font-size:.97rem;color:var(--slate-fg);opacity:.9}}
.side a{{color:var(--accent-on-slate)}}
.side a.cvbtn{{display:grid;grid-template-columns:1fr auto;align-items:center;gap:1rem;margin:1.2rem 0 .7rem;padding:.7rem .9rem;border-radius:10px;border:1.5px solid var(--accent-on-slate);color:var(--slate-fg);text-decoration:none;background:transparent;transition:background .15s,color .15s}}
.side a.cvbtn .big{{font-family:var(--display);font-size:1.15rem;line-height:1.1}}
.side a.cvbtn .m{{display:block;font-family:var(--mono);font-size:.7rem;color:var(--slate-muted);margin-top:.25rem}}
.side a.cvbtn .arr{{font-family:var(--mono);font-size:1.1rem;color:var(--accent-on-slate);width:2rem;height:2rem;border-radius:6px;display:grid;place-items:center;border:1px solid color-mix(in srgb,var(--accent-on-slate) 40%,transparent)}}
.side a.cvbtn:hover,.side a.cvbtn:focus-visible{{background:var(--accent-on-slate);color:var(--slate)}}
.side a.cvbtn:hover .m,.side a.cvbtn:hover .arr{{color:var(--slate);border-color:var(--slate)}}
.linklist{{display:grid;gap:.15rem;margin:0 0 1rem}}
.linklist a{{display:grid;grid-template-columns:2rem 1fr auto;align-items:center;gap:.75rem;padding:.3rem .5rem;border-radius:8px;color:var(--slate-fg);text-decoration:none;border:1px solid transparent}}
.linklist a:hover,.linklist a:focus-visible{{border-color:var(--hair);background:var(--tile)}}
.linklist .mark{{width:2rem;height:2rem;border-radius:6px;display:grid;place-items:center;font-family:var(--mono);font-size:.74rem;font-weight:600;background:var(--tile);color:var(--slate-fg);border:1px solid var(--hair)}}
.linklist a:hover .mark{{background:var(--accent-on-slate);color:var(--slate);border-color:var(--accent-on-slate)}}
.linklist .lbl{{min-width:0;line-height:1.2}}
.linklist .lbl small{{display:block;font-family:var(--mono);font-size:.7rem;color:var(--slate-muted);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.linklist .arr{{font-family:var(--mono);color:var(--slate-muted);opacity:0;transform:translateX(-4px);transition:opacity .15s,transform .15s}}
.linklist a:hover .arr{{opacity:1;transform:none;color:var(--accent-on-slate)}}
/* phosphor goes 8-bit */
:root.phosphor .side h1,:root.phosphor .hero h2,:root.phosphor h3.sec,:root.phosphor .card .t,:root.phosphor .job .r,:root.phosphor .toast{{font-family:"Silkscreen",var(--mono);letter-spacing:0}}
:root.phosphor .side h1{{font-size:1.5rem;line-height:1.4}} :root.phosphor .hero h2{{font-size:1.25rem;line-height:1.6}} :root.phosphor h3.sec{{font-size:1rem}} :root.phosphor .card .t,:root.phosphor .job .r{{font-size:.8rem;line-height:1.7}}
:root.phosphor .hero h2 em{{font-style:normal}}
:root.phosphor .side img{{image-rendering:pixelated;border-radius:0;filter:none}}
:root.phosphor .status .dot{{border-radius:0;animation:blink 1s steps(1,end) infinite;box-shadow:none}}
@keyframes blink{{50%{{opacity:0}}}}
:root.phosphor .card,:root.phosphor .side a.cvbtn,:root.phosphor .side a.cvbtn .arr,:root.phosphor .linklist .mark,:root.phosphor .badge,:root.phosphor .plinks a,:root.phosphor .copy{{border-radius:0}}
:root.phosphor .card{{box-shadow:4px 4px 0 var(--rule)}}
:root.phosphor .toast{{border-radius:0;font-size:.7rem;box-shadow:4px 4px 0 var(--accent-on-slate)}}
.toggle{{position:absolute;top:1rem;right:1rem;background:var(--tile);border:1px solid var(--hair);color:var(--slate-fg);border-radius:999px;width:2rem;height:2rem;cursor:pointer}}
.main{{min-width:0;background-color:var(--paper);background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:24px 24px;{GUTTER}padding-block:3.5rem 5rem;padding-left:max(3.5rem,env(safe-area-inset-left,0px));padding-right:max(3.5rem,env(safe-area-inset-right,0px))}}
.inner{{max-width:48rem}}
.hero h2{{font-family:var(--display);font-weight:500;font-size:clamp(1.9rem,3.2vw,2.7rem);line-height:1.15;margin:0 0 1rem;letter-spacing:-.015em;text-wrap:balance}}
.hero h2 em{{font-style:italic;color:var(--accent)}}
.hero p{{font-size:1.08rem;max-width:40rem}}
section{{margin-top:3.5rem}}
.eyebrow{{font-family:var(--mono);font-size:.74rem;color:var(--accent);letter-spacing:.04em;margin-bottom:.3rem}}
h3.sec{{font-family:var(--display);font-weight:500;font-size:1.65rem;margin:0 0 1.2rem;display:flex;align-items:baseline;gap:1rem}}
h3.sec::after{{content:"";flex:1;height:1px;background:var(--rule)}}
.news{{display:grid;grid-template-columns:6rem 1fr;gap:.6rem 1rem;margin:0}}
.news dt{{font-family:var(--mono);color:var(--muted);font-size:.82rem;padding-top:.2rem}}
.news dt::before{{content:"";display:inline-block;width:.5rem;height:.5rem;border-radius:50%;background:var(--accent);margin-right:.6rem;vertical-align:middle}}
.news dd{{margin:0;min-width:0}}
.cards{{display:grid;gap:.9rem}}
.card{{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:1.1rem 1.25rem;display:grid;gap:.35rem}}
.card .top{{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;font-size:.8rem}}
.badge{{font-family:var(--mono);background:var(--badge);color:var(--ink);padding:.15rem .55rem;border-radius:4px;font-weight:600;letter-spacing:.02em}}
.year{{font-family:var(--mono);color:var(--muted)}}
.card .t{{font-family:var(--display);font-weight:500;font-size:1.15rem;line-height:1.3}}
.card .au{{font-size:.92rem;color:var(--muted)}}
.row{{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.3rem;align-items:center}}
.plinks{{display:contents}}
.plinks a,.copy{{font-size:.8rem;font-weight:600;padding:.3rem .7rem;border-radius:6px;background:var(--badge);color:var(--ink);border:0;font-family:var(--body);cursor:pointer;line-height:1.4}}
.plinks a:hover,.copy:hover{{background:var(--accent);color:#fff;text-decoration:none}}
.copy{{font-family:var(--mono);font-size:.74rem;font-weight:500}}
.copy[data-done]{{background:var(--accent);color:#fff}}
.job{{display:grid;grid-template-columns:1fr auto;gap:.15rem 1.5rem;padding:1rem 0 1rem 1.25rem;border-left:2px solid var(--rule)}}
.job:hover{{border-left-color:var(--accent)}}
.job .r{{font-family:var(--display);font-weight:500;font-size:1.15rem}}
.job .o{{color:var(--muted);font-size:.95rem;grid-column:1}}
.job .d{{grid-row:1;grid-column:2;font-family:var(--mono);color:var(--muted);font-size:.8rem;white-space:nowrap;padding-top:.3rem}}
.job ul{{grid-column:1/-1;margin:.4rem 0 0;padding-left:1.1rem;font-size:.97rem}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem}}
.two>div{{min-width:0}}
.item{{margin-bottom:1rem}} .item .s{{color:var(--muted);font-size:.9rem}}
ul.plain{{margin:0;padding-left:1.1rem}}
footer{{margin-top:4rem;color:var(--muted);font-size:.82rem;font-family:var(--mono);display:flex;flex-wrap:wrap;gap:.3rem 1.2rem}}
.toast{{position:fixed;left:50%;bottom:calc(1.2rem + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:70;background:var(--slate);color:var(--slate-fg);font-family:var(--mono);font-size:.8rem;padding:.6rem 1rem;border-radius:8px;border:1px solid var(--accent-on-slate)}}
.toast[hidden]{{display:none}}
@media (max-height:720px) and (min-width:861px){{.side{{position:static;height:auto;min-height:100vh}}}}
@media (max-width:860px){{.page{{grid-template-columns:1fr}}
.side{{position:static;height:auto;display:grid;grid-template-columns:auto 1fr;grid-auto-rows:auto;column-gap:1rem;align-items:center;padding-block:1.5rem 1.6rem;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.side img{{width:72px;height:72px;grid-row:1/3;grid-column:1;align-self:center}}
.side h1{{grid-column:2;font-size:1.75rem;margin:0;align-self:end;padding-right:2.6rem}}
.side .tag{{grid-column:2;margin:.15rem 0 0;font-size:.9rem;align-self:start}}
.side .status,.side .cvbtn,.side .linklist,.side .email{{grid-column:1/-1}}
.side .status{{margin:1.1rem 0 .2rem;justify-self:start}}
.side a.cvbtn{{margin:.9rem 0 .7rem}}
.linklist{{grid-template-columns:1fr 1fr;gap:.2rem .5rem;margin-bottom:.8rem}}
.linklist a{{padding:.3rem .4rem}} .linklist .arr{{display:none}}
.main{{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:2.5rem 4rem}}.two{{grid-template-columns:1fr}}}}
@media (max-width:480px){{.status{{font-size:.7rem;padding:.3rem .65rem .3rem .5rem}}.linklist .lbl small{{display:none}}.side .tag{{font-size:.85rem}}}}
@media (max-width:560px){{.job{{grid-template-columns:1fr}}.job .d{{grid-row:auto;grid-column:1;white-space:normal}}.news{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
'''
    head = f'''<title>{NAME}</title>
{meta(DESC)}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;1,9..144,500&family=Figtree:wght@400;600&family=JetBrains+Mono:wght@400;500&family=Silkscreen&display=swap"/>
<style>{css}</style>'''
    pills = (f'<a class="cvbtn" href="{CV}"><span><span class="big">Curriculum vitae</span><span class="m">PDF · 2 pages · updated Oct 2026</span></span><span class="arr">↓</span></a><nav class="linklist" aria-label="Profiles">' +
             "".join(f'<a href="{u}"><span class="mark">{mk}</span><span class="lbl">{l}<small>{sub}</small></span><span class="arr">→</span></a>' for l, u, mk, sub in LINKS) + "</nav>")
    side = (f'<aside class="side">{TOGGLE}<img src="{img}" alt="Portrait of {NAME}"/>'
            f'<h1>Hamed<br/>Mahdavi</h1><p class="tag">{TAGLINE}</p>'
            f'<div class="status"><span class="dot"></span>Open to research scientist roles · late 2026</div>'
            f'{pills}<div class="email">{EMAIL}</div></aside>')
    def sec(id_, label, body, eyebrow=None):
        eb = eyebrow or f"// {label.lower()}"
        return f'<section id="{id_}"><div class="eyebrow">{eb}</div><h3 class="sec">{label}</h3>{body}</section>'
    m = ['<main class="main"><div class="inner">']
    m.append('<div class="hero"><div class="eyebrow">// about</div><h2>Teaching language models to reason, <em>and checking the work.</em></h2>' + f"<p>{BIO[0]}</p><p>{BIO[1]}</p></div>")
    m.append(sec("news", "News", '<dl class="news">' + "".join(f"<dt>{d}</dt><dd>{t}</dd>" for d, t in NEWS) + "</dl>"))
    cards = []
    for i, (t, a, v, y, l, _) in enumerate(PUBS):
        bib = html.escape(bibtex(i, t, a, v, y, l), quote=True)
        first_url = html.escape(next(iter(l.values())), quote=True)
        cards.append(f'<article class="card"><div class="top"><span class="badge">{v}</span><span class="year">{y}</span></div><div class="t">{t}</div><div class="au">{me(a)}</div>'
                     f'<div class="row">{pub_links(l)}<button type="button" class="copy" data-copy="{first_url}" data-label="copy link">copy link</button>'
                     f'<button type="button" class="copy" data-copy="{bib}" data-label="copy bibtex">copy bibtex</button></div></article>')
    m.append(sec("publications", "Publications", '<div class="cards">' + "".join(cards) + "</div>"))
    m.append(sec("experience", "Experience", "".join(
        f'<div class="job"><div class="r">{t}</div><div class="d">{d}</div><div class="o">{org(o, lk)} · {loc}</div><ul>' + "".join(f"<li>{x}</li>" for x in bl) + "</ul></div>"
        for t, o, loc, d, bl, lk in EXPERIENCE)))
    m.append('<section id="education"><div class="two"><div><div class="eyebrow">// education</div><h3 class="sec">Education</h3>' + "".join(
        f'<div class="item"><strong>{t}</strong><div class="s">{o} · {d}</div><div class="s">{n}</div></div>' for t, o, d, n in EDUCATION) +
        '</div><div id="honors"><div class="eyebrow">// honors</div><h3 class="sec">Honors</h3>' + "".join(
        f'<div class="item"><strong>{t}</strong><div class="s">{d} · {n}</div></div>' for t, d, n in HONORS) + "</div></div></section>")
    m.append(sec("interests", "Interests", '<ul class="plain">' + "".join(f"<li>{i}</li>" for i in INTERESTS) + f"</ul><p>{OUTSIDE}</p>"))
    m.append(f'<footer><span>{NAME} · updated 2026-10</span><span>No framework. __KB__ KB of HTML and CSS.</span><a href="{REPO_URL}">Source on GitHub</a></footer></div></main>')
    toast_el = '<div class="toast" id="toast" hidden></div>'
    js = THEME_JS + '''<script>
(function(){var PIXEL_PORTRAIT="''' + PIXEL_PORTRAIT + '''";
var toast=document.getElementById('toast'),tt;
function say(m){toast.textContent=m;toast.hidden=false;clearTimeout(tt);tt=setTimeout(function(){toast.hidden=true},1800)}
function copy(text,done){function ok(){done&&done();say('Copied')}
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(ok,function(){fallback()})}else{fallback()}
 function fallback(){var ta=document.createElement('textarea');ta.value=text;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');ok()}catch(e){say('Select and copy manually')}document.body.removeChild(ta)}}
document.addEventListener('click',function(e){var b=e.target.closest('.copy');if(!b)return;copy(b.getAttribute('data-copy'),function(){b.setAttribute('data-done','');b.textContent='copied';setTimeout(function(){b.removeAttribute('data-done');b.textContent=b.getAttribute('data-label')},1500)})});
/* konami */
var seq=['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a'],pos=0;
document.addEventListener('keydown',function(e){var k=e.key.length===1?e.key.toLowerCase():e.key;pos=(k===seq[pos])?pos+1:(k===seq[0]?1:0);
 if(pos===seq.length){pos=0;var on=document.documentElement.classList.toggle('phosphor');var im=document.querySelector('.side img');
  if(on){im.setAttribute('data-src',im.src);im.src=PIXEL_PORTRAIT;say('ACHIEVEMENT UNLOCKED · phosphor mode')}else{im.src=im.getAttribute('data-src');say('back to amber.')}}});
})();
</script>'''
    body = f'<div class="page">{side}{"".join(m)}</div>{toast_el}{js}'
    return head, body

VARIANTS = {"b": variant_b}

def full_doc(head, body):
    return f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8"/>\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>\n<link rel="icon" href="dist/assets/img/favicon.ico"/>\n{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n'

TITLES = {"b": "Direction B Editorial"}

def fragment(head, body, key):
    head = head.replace(f"<title>{NAME}</title>", f"<title>{TITLES[key]}</title>", 1)
    return f'<meta name="claude:viewport-fit-sides" content="cover">\n{head}\n{body}\n'

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fragment":
        key, out = sys.argv[2], sys.argv[3]
        with open(os.path.join(HERE, "..", "dist", "assets", "img", "profile.jpg"), "rb") as f:
            data = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
        h0, b0 = VARIANTS[key](IMG_REL)
        kb = str(round(len(full_doc(h0, b0).encode()) / 1024))
        head, body = VARIANTS[key](data)
        open(out, "w").write(fragment(head, body, key).replace("__KB__", kb)); print(out)
    else:
        for k, fn in VARIANTS.items():
            head, body = fn(IMG_REL)
            doc = full_doc(head, body); doc = doc.replace("__KB__", str(round(len(doc.encode()) / 1024)))
            p = os.path.join(HERE, "..", "index.html"); open(p, "w").write(doc); print(os.path.normpath(p))
