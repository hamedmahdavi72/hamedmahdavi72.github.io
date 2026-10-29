#!/usr/bin/env python3
"""Render the Direction B prototype from content.py.

  python3 build.py            -> writes b.html next to this file
  python3 build.py --fragment DIR OUT  -> writes an artifact fragment (no doctype/html/head/body,
                                          profile photo inlined) for preview publishing
"""
import base64, html, os, sys
from content import *

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_REL = "../dist/assets/img/profile-duotone.jpg"
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

def variant_b(img):
    css = f'''
/* Layout: sticky slate identity column (amber on slate, like an amber phosphor terminal) beside a graph-paper content column. */
:root{{--paper:#f4f5f7;--ink:#1b1f26;--muted:#5b6370;--rule:#d8dce3;--grid:rgba(27,31,38,.07);--slate:#1e2430;--slate-fg:#eef0f4;--slate-muted:#9aa3b2;
--accent:#9a6a12;--accent-on-slate:#d9a441;--card:#ffffff;--badge:#e9edf3;--overlay:rgba(27,31,38,.55);
--display:"Fraunces",Georgia,serif;--body:"Figtree",system-ui,-apple-system,"Segoe UI",sans-serif;--mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--paper:#15181d;--ink:#e8eaee;--muted:#9aa3b2;--rule:#2a303a;--grid:rgba(232,234,238,.05);--slate:#0f1217;--card:#1c2128;--badge:#262c36;--accent:#d9a441;--overlay:rgba(0,0,0,.6);color-scheme:dark}}}}
:root[data-theme="dark"]{{--paper:#15181d;--ink:#e8eaee;--muted:#9aa3b2;--rule:#2a303a;--grid:rgba(232,234,238,.05);--slate:#0f1217;--card:#1c2128;--badge:#262c36;--accent:#d9a441;--overlay:rgba(0,0,0,.6);color-scheme:dark}}
/* Konami: green phosphor mode, wins over both themes */
:root.phosphor,:root.phosphor[data-theme]{{--paper:#050c06;--ink:#9dff9d;--muted:#5fbf5f;--rule:#1d3a1d;--grid:rgba(157,255,157,.08);--slate:#020602;--slate-fg:#9dff9d;--slate-muted:#5fbf5f;--accent:#9dff9d;--accent-on-slate:#9dff9d;--card:#0a1a0a;--badge:#143014;--overlay:rgba(0,20,0,.7);color-scheme:dark}}
:root.phosphor body{{text-shadow:0 0 .6px currentColor}}
:root.phosphor body::after{{content:"";position:fixed;inset:0;pointer-events:none;z-index:40;background:repeating-linear-gradient(0deg,rgba(0,0,0,.22) 0 1px,transparent 1px 3px),radial-gradient(ellipse at center,transparent 60%,rgba(0,0,0,.55) 100%)}}
:root.phosphor .side img{{filter:grayscale(1) sepia(1) hue-rotate(70deg) saturate(3) contrast(1.1)}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:16.5px;line-height:1.6}}
a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
a:focus-visible,button:focus-visible,input:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.page{{display:grid;grid-template-columns:minmax(300px,360px) 1fr;min-height:100vh}}
.side{{background:var(--slate);color:var(--slate-fg);position:sticky;top:0;height:100vh;overflow:auto;{GUTTER}padding-block:3rem;padding-left:max(2.5rem,env(safe-area-inset-left,0px))}}
.side img{{width:132px;height:132px;border-radius:50%;object-fit:cover;border:3px solid var(--accent-on-slate)}}
.side h1{{font-family:var(--display);font-weight:500;font-size:2.5rem;line-height:1.05;margin:1.4rem 0 .4rem;letter-spacing:-.01em;text-wrap:balance}}
.side .tag{{color:var(--slate-muted);margin:0 0 1rem;font-size:1.02rem}}
.status{{display:inline-flex;align-items:center;gap:.55rem;font-family:var(--mono);font-size:.78rem;color:var(--slate-fg);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:.35rem .8rem .35rem .6rem;margin-bottom:1.2rem}}
.status .dot{{width:.55rem;height:.55rem;border-radius:50%;background:var(--accent-on-slate);box-shadow:0 0 0 0 var(--accent-on-slate);animation:pulse 2.2s ease-out infinite}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 color-mix(in srgb,var(--accent-on-slate) 60%,transparent)}}100%{{box-shadow:0 0 0 .6rem transparent}}}}
.side p{{font-size:.97rem;color:var(--slate-fg);opacity:.9}}
.side a{{color:var(--accent-on-slate)}}
.pills{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1.4rem 0 1rem}}
.pills a{{font-size:.85rem;padding:.35rem .8rem;border:1px solid rgba(255,255,255,.22);border-radius:999px;color:var(--slate-fg);text-decoration:none}}
.pills a:hover{{border-color:var(--accent-on-slate);color:var(--accent-on-slate)}}
.pills a.cv{{background:var(--accent-on-slate);color:var(--slate);border-color:var(--accent-on-slate);font-weight:600}}
.email{{font-family:var(--mono);font-size:.82rem;color:var(--slate-muted);word-break:break-all}}
.cmdk{{display:inline-flex;align-items:center;gap:.5rem;margin-top:1.4rem;background:none;border:1px solid rgba(255,255,255,.18);color:var(--slate-muted);border-radius:8px;padding:.4rem .7rem;font-family:var(--mono);font-size:.78rem;cursor:pointer}}
.cmdk:hover{{color:var(--slate-fg);border-color:var(--accent-on-slate)}}
kbd{{font-family:var(--mono);font-size:.72rem;border:1px solid currentColor;border-radius:4px;padding:.05rem .35rem;opacity:.85}}
.toggle{{position:absolute;top:1rem;right:1rem;background:none;border:1px solid rgba(255,255,255,.25);color:var(--slate-fg);border-radius:999px;width:2rem;height:2rem;cursor:pointer}}
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
/* command palette */
.pal{{position:fixed;inset:0;z-index:60;background:var(--overlay);display:flex;align-items:flex-start;justify-content:center;padding:12vh max(16px,env(safe-area-inset-right,0px)) 0 max(16px,env(safe-area-inset-left,0px))}}
.pal[hidden]{{display:none}}
.pal .box{{width:min(36rem,100%);background:var(--card);color:var(--ink);border:1px solid var(--rule);border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.35);overflow:hidden}}
.pal input{{width:100%;border:0;border-bottom:1px solid var(--rule);background:transparent;color:var(--ink);font:1rem var(--body);padding:.9rem 1rem;outline:none}}
.pal ul{{list-style:none;margin:0;padding:.4rem;max-height:50vh;overflow:auto}}
.pal li{{display:flex;justify-content:space-between;gap:1rem;padding:.55rem .7rem;border-radius:8px;cursor:pointer;font-size:.95rem}}
.pal li[aria-selected="true"]{{background:var(--badge)}}
.pal li .k{{font-family:var(--mono);font-size:.72rem;color:var(--muted);flex:none}}
.pal li span:first-child{{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.pal .hint{{font-family:var(--mono);font-size:.7rem;color:var(--muted);padding:.5rem 1rem;border-top:1px solid var(--rule)}}
.toast{{position:fixed;left:50%;bottom:calc(1.2rem + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:70;background:var(--slate);color:var(--slate-fg);font-family:var(--mono);font-size:.8rem;padding:.6rem 1rem;border-radius:8px;border:1px solid var(--accent-on-slate)}}
.toast[hidden]{{display:none}}
@media (max-width:860px){{.page{{grid-template-columns:1fr}}.side{{position:static;height:auto;padding-block:2.5rem;padding-left:max(16px,env(safe-area-inset-left,0px))}}.main{{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:2.5rem 4rem}}.two{{grid-template-columns:1fr}}}}
@media (max-width:560px){{.job{{grid-template-columns:1fr}}.job .d{{grid-row:auto;grid-column:1;white-space:normal}}.news{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
'''
    head = f'''<title>{NAME}</title>
{meta(DESC)}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;1,9..144,500&family=Figtree:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap"/>
<style>{css}</style>'''
    pills = f'<div class="pills"><a class="cv" href="{CV}">Download CV</a>' + "".join(f'<a href="{u}">{l}</a>' for l, u in LINKS) + "</div>"
    side = (f'<aside class="side">{TOGGLE}<img src="{img}" alt="Portrait of {NAME}"/>'
            f'<h1>Hamed<br/>Mahdavi</h1><p class="tag">{TAGLINE}</p>'
            f'<div class="status"><span class="dot"></span>Open to research scientist roles · late 2026</div>'
            f'<p>{BIO[0]}</p>{pills}<div class="email">{EMAIL}</div>'
            f'<button type="button" class="cmdk" data-cmdk>Search this page <kbd>⌘K</kbd></button></aside>')
    def sec(id_, label, body, eyebrow=None):
        eb = eyebrow or f"// {label.lower()}"
        return f'<section id="{id_}"><div class="eyebrow">{eb}</div><h3 class="sec">{label}</h3>{body}</section>'
    m = ['<main class="main"><div class="inner">']
    m.append('<div class="hero"><div class="eyebrow">// about</div><h2>Teaching language models to reason, <em>and checking the work.</em></h2>' + f"<p>{BIO[1]}</p></div>")
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
    # palette items
    items = [("Go to " + s, "#" + i, "section") for i, s in (("news","News"),("publications","Publications"),("experience","Experience"),("education","Education"),("honors","Honors"),("interests","Interests"))]
    items += [(t, next(iter(l.values())), "paper") for t, a, v, y, l, _ in PUBS]
    items += [("Download CV", CV, "file")] + [(l, u, "link") for l, u in LINKS] + [("Copy email address", "copy:" + EMAIL, "action")]
    pal_items = "".join(f'<li data-url="{html.escape(u, quote=True)}"><span>{html.escape(t)}</span><span class="k">{k}</span></li>' for t, u, k in items)
    palette = (f'<div class="pal" id="pal" hidden role="dialog" aria-modal="true" aria-label="Search this page"><div class="box">'
               f'<input id="pal-q" type="text" placeholder="Jump to a section, open a paper, copy email…" autocomplete="off"/>'
               f'<ul id="pal-list">{pal_items}</ul><div class="hint">↑↓ navigate · ↵ open · esc close</div></div></div>'
               f'<div class="toast" id="toast" hidden></div>')
    js = THEME_JS + '''<script>
(function(){
var toast=document.getElementById('toast'),tt;
function say(m){toast.textContent=m;toast.hidden=false;clearTimeout(tt);tt=setTimeout(function(){toast.hidden=true},1800)}
function copy(text,done){function ok(){done&&done();say('Copied')}
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(ok,function(){fallback()})}else{fallback()}
 function fallback(){var ta=document.createElement('textarea');ta.value=text;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');ok()}catch(e){say('Select and copy manually')}document.body.removeChild(ta)}}
document.addEventListener('click',function(e){var b=e.target.closest('.copy');if(!b)return;copy(b.getAttribute('data-copy'),function(){b.setAttribute('data-done','');b.textContent='copied';setTimeout(function(){b.removeAttribute('data-done');b.textContent=b.getAttribute('data-label')},1500)})});
/* command palette */
var pal=document.getElementById('pal'),q=document.getElementById('pal-q'),list=document.getElementById('pal-list'),rows=[].slice.call(list.children),sel=0;
function open(){pal.hidden=false;q.value='';filter();q.focus()}
function close(){pal.hidden=true}
function visible(){return rows.filter(function(r){return !r.hidden})}
function filter(){var v=q.value.trim().toLowerCase();rows.forEach(function(r){r.hidden=v&&r.textContent.toLowerCase().indexOf(v)<0});sel=0;paint()}
function paint(){var vis=visible();rows.forEach(function(r){r.setAttribute('aria-selected','false')});if(vis[sel]){vis[sel].setAttribute('aria-selected','true');vis[sel].scrollIntoView({block:'nearest'})}}
function go(r){if(!r)return;var u=r.getAttribute('data-url');close();if(u.indexOf('copy:')===0){copy(u.slice(5))}else if(u.charAt(0)==='#'){var t=document.querySelector(u);t&&t.scrollIntoView({behavior:'smooth',block:'start'})}else if(u.indexOf('http')===0){window.open(u,'_blank','noopener')||(location.href=u)}else{location.href=u}}
document.addEventListener('keydown',function(e){
 if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();pal.hidden?open():close();return}
 if(pal.hidden)return;
 if(e.key==='Escape'){close()}else if(e.key==='ArrowDown'){e.preventDefault();sel=Math.min(sel+1,visible().length-1);paint()}else if(e.key==='ArrowUp'){e.preventDefault();sel=Math.max(sel-1,0);paint()}else if(e.key==='Enter'){e.preventDefault();go(visible()[sel])}});
q.addEventListener('input',filter);
list.addEventListener('click',function(e){var r=e.target.closest('li');r&&go(r)});
pal.addEventListener('click',function(e){if(e.target===pal)close()});
document.addEventListener('click',function(e){if(e.target.closest('[data-cmdk]'))open()});
/* konami */
var seq=['ArrowUp','ArrowUp','ArrowDown','ArrowDown','ArrowLeft','ArrowRight','ArrowLeft','ArrowRight','b','a'],pos=0;
document.addEventListener('keydown',function(e){var k=e.key.length===1?e.key.toLowerCase():e.key;pos=(k===seq[pos])?pos+1:(k===seq[0]?1:0);
 if(pos===seq.length){pos=0;var on=document.documentElement.classList.toggle('phosphor');say(on?'phosphor mode engaged. same code to exit.':'back to amber.')}});
})();
</script>'''
    body = f'<div class="page">{side}{"".join(m)}</div>{palette}{js}'
    return head, body

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
        with open(os.path.join(HERE, "..", "dist", "assets", "img", "profile-duotone.jpg"), "rb") as f:
            data = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
        h0, b0 = VARIANTS[key](IMG_REL)
        kb = str(round(len(full_doc(h0, b0).encode()) / 1024))
        head, body = VARIANTS[key](data)
        open(out, "w").write(fragment(head, body, key).replace("__KB__", kb)); print(out)
    else:
        for k, fn in VARIANTS.items():
            head, body = fn(IMG_REL)
            doc = full_doc(head, body); doc = doc.replace("__KB__", str(round(len(doc.encode()) / 1024)))
            p = os.path.join(HERE, f"{k}.html"); open(p, "w").write(doc); print(p)
