"""Gera hf/index.html: vídeo "50% de quê?" (Black de Verdade, Elite Boardgamers), 1080x1080, ~61 s.
Pinturas feitas em código (huashu-art-motion, MIT), à maneira de Caravaggio, La Tour, Cézanne, Pissarro, Jan Steen, Vermeer,
Chardin e Caillebotte; gráfico em aquarela; duas inserções curtas do próprio site. Legenda na cor do logo. Nenhuma imagem de IA.
Regras: elite-boardgamers/docs/video/DIRECAO_VIDEO_ELITE.md. Uso: python3 montar.py
"""
import json, re, difflib, unicodedata
from pathlib import Path
P = Path(__file__).resolve().parent / "hf"
T = json.load(open(P / "assets/data/tempos.json", encoding="utf-8"))
FALAS = {f["id"]: f for f in json.load(open(P.parent / "falas.json", encoding="utf-8"))}
FI = {f["fala"]: f for f in T["falas"]}
TOTAL = T["total"]
pw = lambda n: [w for w in T["palavras"] if w["fala"] == n]
norm = lambda s: unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode().strip(".,:?!\"'")
def ts(n, palavra, k=1):
    c = 0
    for w in pw(n):
        if norm(w["w"]).startswith(norm(palavra)):
            c += 1
            if c == k: return w["s"]
    raise KeyError((n, palavra))

# ---------- legendas: texto do roteiro alinhado às palavras transcritas (o "84" falado vira 3 palavras) ----------
def alinhar(fid):
    toks, ws = FALAS[fid]["texto"].split(), pw(fid)
    a, b = [norm(x) for x in toks], [norm(w["w"]) for w in ws]
    tempos = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): tempos[i1 + k] = (ws[j1 + k]["s"], ws[j1 + k]["e"])
        elif i2 > i1:
            s = ws[j1]["s"] if j1 < len(ws) else ws[-1]["e"]; e = ws[j2 - 1]["e"] if j2 > j1 else s + .3
            for k in range(i2 - i1): tempos[i1 + k] = (s + (e - s) * k / (i2 - i1), s + (e - s) * (k + 1) / (i2 - i1))
    return list(zip(toks, tempos))
blocos = []
for fid in range(1, 11):
    cur = []
    for tok, (s, e) in alinhar(fid):
        cur.append((tok, s, e))
        if len(cur) == 3 or re.search(r"[.,:?!]$", tok): blocos.append(cur); cur = []
    if cur: blocos.append(cur)
leg = []
for i, b in enumerate(blocos):
    prox = blocos[i + 1][0][1] if i + 1 < len(blocos) else TOTAL
    txt = " ".join(t for t, _, _ in b).replace("eliteboardgamers.com.br.", "eliteboardgamers.com.br")
    leg.append({"txt": txt, "ini": round(b[0][1], 3), "fim": round(min(prox, b[-1][2] + 0.45), 3)})

# ---------- cortes ----------
C = {"latour": FI[2]["inicio"] - .25, "graf": FI[4]["inicio"] - .25, "cez": FI[6]["inicio"] - .25, "pis": ts(6, "ainda") - .2,
     "steen": ts(6, "achado") - .1, "verm": ts(6, "alerta") - .1, "chardin": FI[7]["inicio"] - .25, "caille": FI[8]["inicio"] - .3,
     "mesa": FI[9]["inicio"] - .25, "cartela": FI[10]["inicio"] - .3}
M = {"etiqueta": ts(2, "etiqueta"), "loja": ts(2, "loja"), "entao": ts(3, "Então"), "nao": ts(3, "não"), "black4": ts(4, "Black"),
     "media": ts(4, "média"), "p20": ts(5, "20"), "mais": ts(5, "mais"), "avaliado": ts(6, "avaliado"), "cupom": ts(6, "cupom"),
     "achado": ts(6, "achado"), "alerta": ts(6, "alerta"), "links": ts(7, "links"), "oitenta": ts(7, "Oitenta"), "como": ts(7, "como"),
     "noticias": ts(7, "notícias"), "conta": ts(8, "conta"), "qual": ts(9, "qual"), "elite": ts(10, "Elite"), "link": ts(10, "link")}
XF = 0.35
ORD = ["el_caravaggio", "el_latour", "el_grafico", "el_cezanne", "el_pissarro", "el_steen", "el_vermeer", "el_chardin", "el_caillebotte", "el_mesa_dia"]
INI = [0, C["latour"], C["graf"], C["cez"], C["pis"], C["steen"], C["verm"], C["chardin"], C["caille"], C["mesa"], C["cartela"]]
VIDEOS = "\n".join(f'<video id="v{k}" class="clip artv" data-start="{INI[k]:.3f}" data-duration="{INI[k + 1] + XF - INI[k]:.3f}" data-media-start="0" '
                   f'data-track-index="{k}" muted playsinline src="assets/art/{s}.mp4"></video>' for k, s in enumerate(ORD))
def ov(i, a, b, html, cls="", tr=12):
    return f'<div id="{i}" class="clip ov {cls}" data-start="{a:.3f}" data-duration="{b - a:.3f}" data-track-index="{tr}">{html}</div>'
cred = lambda i, a, b, txt, tr: ov(i, a, b, txt, "cred", tr)
OVS = [
    ov("o-capa", 0, 1.15, '<div id="capa-tag">BLACK FRIDAY · JOGOS DE TABULEIRO</div><div id="capa-t">50% de quê?</div><div id="capa-sub">como saber se o desconto é real</div>', "capa", 11),
    cred("c1", 1.3, C["latour"], 'PINTURA FEITA EM CÓDIGO, À MANEIRA DE CARAVAGGIO, “OS TRAPACEIROS” (c. 1594)', 12),
    ov("o-ex", M["etiqueta"] - .2, M["loja"] + 1.4, '<div id="ex"><s>DE R$ 400</s><b>POR R$ 200</b></div><div id="ex-selo">EXEMPLO</div>', "", 13),
    cred("c2", C["latour"] + .3, C["graf"], 'À MANEIRA DE GEORGES DE LA TOUR (c. 1640)', 14),
    ov("o-q", M["entao"] + .2, M["nao"] + .6, '<div class="mao" id="q">?</div>', "", 15),
    ov("o-card1", M["black4"] - .15, M["black4"] + 2.25, '<div class="card" id="card1"><div class="cimg" style="background-image:url(assets/img/black.png)"></div><div class="cardleg">eliteboardgamers.com.br/black · 25/11/2026</div></div>', "", 16),
    ov("o-graf", M["media"] - .1, C["cez"], '<div class="mao gl" id="gl-preco">preço</div><div class="mao gl" id="gl-media">média real</div><div class="mao gl" id="gl-20">−20%</div>'
       '<div id="cont"><b>116</b><span>jogos com desconto real</span><small>LIDO EM 25/11/2026, 20H40</small></div>', "", 17),
    cred("c3", C["graf"] + .3, C["cez"], 'ILUSTRAÇÃO DO MÉTODO · FONTE: ELITEBOARDGAMERS.COM.BR/BLACK, 25/11/2026', 18),
    ov("o-t1", M["avaliado"] - .2, C["pis"], '<div class="tag">nota 7+ no BGG ou premiado</div>', "", 19),
    cred("c4", C["cez"] + .2, C["pis"], 'À MANEIRA DE CÉZANNE, “OS JOGADORES DE CARTAS” (1890–95)', 20),
    ov("o-t2", C["pis"] + .05, C["steen"], '<div class="tag">cupom</div>', "", 21), cred("c5", C["pis"] + .05, C["steen"], 'À MANEIRA DE PISSARRO', 22),
    ov("o-t3", C["steen"] + .05, C["verm"], '<div class="tag">achado da comunidade</div>', "", 23), cred("c6", C["steen"] + .05, C["verm"], 'À MANEIRA DE JAN STEEN', 24),
    ov("o-t4", C["verm"] + .05, C["chardin"], '<div class="tag">alerta no celular · sem cadastro</div>', "", 25), cred("c7", C["verm"] + .05, C["chardin"], 'À MANEIRA DE VERMEER', 26),
    ov("o-semc", M["links"] - .1, M["oitenta"] - .1, '<div id="semc">links sem comissão</div>', "", 27),
    ov("o-andar", M["oitenta"] - .1, C["caille"], '<div class="mao andar" id="an1">84 resenhas</div><div class="mao andar" id="an2">como jogar</div><div class="mao andar" id="an3">notícias</div>', "", 28),
    ov("o-card2", M["oitenta"] - .05, M["oitenta"] + 2.2, '<div class="card card2" id="card2"><div class="cimg" style="background-image:url(assets/img/resenhas.png)"></div><div class="cardleg">eliteboardgamers.com.br/resenhas · 25/11/2026</div></div>', "", 29),
    cred("c8", C["chardin"] + .3, C["caille"], 'À MANEIRA DE CHARDIN, “O CASTELO DE CARTAS” (c. 1737)', 30),
    cred("c9", C["caille"] + .3, C["mesa"], 'À MANEIRA DE CAILLEBOTTE, “RUA DE PARIS, DIA DE CHUVA” (1877)', 31),
    cred("c10", C["mesa"] + .2, C["cartela"], 'PINTURA FEITA EM CÓDIGO', 32),
]
CART = """<div id="ct-luz"></div><img id="ct-logo" src="assets/img/logo-eb-156.png">
<div id="ct-t">Black de <i>Verdade</i></div><div id="ct-url">eliteboardgamers.com.br</div><div id="ct-bio">@eliteboardgamers · link na bio</div>
<div id="ct-sec">NOTÍCIAS · RESENHAS · COMO JOGAR · LANÇAMENTOS</div>
<div id="ct-fontes">Fonte: radar Black de Verdade e página de resenhas, eliteboardgamers.com.br, lidos em 25/11/2026 · pinturas feitas em código à maneira de Caravaggio, La Tour, Cézanne, Pissarro, Jan Steen, Vermeer, Chardin e Caillebotte (domínio público) · trilha original</div>"""
SFX = [("cartas", 3.3, .5), ("papel", FI[2]["inicio"] + .2, .45), ("sopro", M["nao"] - .2, .5), ("whoosh", C["graf"] - .1, .35), ("papel", M["black4"] - .1, .4),
       ("cartas", M["p20"] - .1, .3), ("moeda", C["cez"] + .1, .35), ("dado", C["steen"] + .05, .45), ("cartas", C["chardin"] + .2, .4), ("papel", M["oitenta"], .4),
       ("cartas", M["como"] - .1, .3), ("whoosh", C["cartela"] - .15, .35)]
sfx = "\n".join(f'<audio id="sx{n}" class="clip" data-start="{s:.3f}" data-duration="1.2" data-track-index="{40 + n}" data-volume="{v}" src="assets/audio/sfx/{f}.mp3"></audio>' for n, (f, s, v) in enumerate(SFX))
COR = "#E98B1E"   # laranja do logo EB

HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>50% de quê? · Black de Verdade</title>
<script src="assets/lib/gsap.min.js"></script>
<style>
@font-face{{font-family:'Inter';src:url(assets/fonts/inter-latin-900-normal.woff2) format('woff2');font-weight:900}}
@font-face{{font-family:'Newsreader';src:url(assets/fonts/newsreader-latin-500-normal.woff2) format('woff2');font-weight:500}}
@font-face{{font-family:'Newsreader';src:url(assets/fonts/newsreader-latin-600-italic.woff2) format('woff2');font-weight:600;font-style:italic}}
@font-face{{font-family:'IBM Plex Mono';src:url(assets/fonts/ibm-plex-mono-latin-500-normal.woff2) format('woff2');font-weight:500}}
@font-face{{font-family:'Caveat';src:url(assets/fonts/caveat-700.woff2) format('woff2');font-weight:700}}
*{{box-sizing:border-box;margin:0}} html,body{{width:1080px;height:1080px;overflow:hidden;background:#000}}
#root{{position:relative;width:1080px;height:1080px;overflow:hidden;background:#000}}
.artv{{position:absolute;left:0;top:0;width:1080px;height:1080px;object-fit:cover;transform-origin:50% 50%}}
.ov{{position:absolute;inset:0;pointer-events:none}}
.mao{{font-family:'Caveat';font-weight:700;color:#fff6dc;text-shadow:0 3px 14px rgba(10,10,20,.8),0 0 2px rgba(10,10,20,.9)}}
.cred{{top:auto;bottom:0;height:auto;padding:14px 40px 16px;background:linear-gradient(0deg,rgba(8,8,12,.8),rgba(8,8,12,0));color:#f2ead8;font:500 21px/1.35 'IBM Plex Mono';letter-spacing:.04em}}
#capa-tag{{position:absolute;left:0;right:0;top:70px;margin:auto;width:max-content;background:{COR};color:#111;font:900 30px 'Inter';letter-spacing:.06em;padding:8px 18px}}
#capa-t{{position:absolute;left:0;right:0;top:130px;text-align:center;font:900 150px/1 'Inter';color:#fff;-webkit-text-stroke:6px #120c06;paint-order:stroke fill;text-shadow:0 10px 30px rgba(0,0,0,.6)}}
#capa-sub{{position:absolute;left:0;right:0;top:300px;text-align:center;font:italic 600 46px 'Newsreader';color:#fff2d8;text-shadow:0 3px 12px rgba(0,0,0,.9)}}
#ex{{position:absolute;left:0;right:0;top:110px;text-align:center;font:900 76px/1.05 'Inter';color:#fff6dc;text-shadow:0 4px 18px rgba(0,0,0,.9)}}
#ex s{{display:block;text-decoration-color:#e0402a;text-decoration-thickness:8px;opacity:.9}} #ex b{{display:block;color:{COR};font-weight:900}}
#ex-selo{{position:absolute;left:740px;top:80px;border:5px solid #e0402a;color:#e0402a;font:900 30px 'Inter';letter-spacing:.08em;padding:4px 14px;transform:rotate(8deg);background:rgba(20,12,6,.6)}}
#q{{position:absolute;left:0;right:0;top:40px;text-align:center;font-size:360px;line-height:1;color:#ffe6b0}}
.card{{position:absolute;left:560px;top:90px;width:440px;background:#0f1115;padding:10px 10px 8px;border-radius:16px;box-shadow:0 18px 44px rgba(0,0,0,.55);transform:rotate(2deg);opacity:0}}
.cimg{{width:420px;height:640px;border-radius:10px;background-size:420px auto;background-position:0 0;background-repeat:no-repeat}}
.card2 .cimg{{height:590px}} .card2{{left:70px;transform:rotate(-2deg)}}
.cardleg{{font:500 16px/1.3 'IBM Plex Mono';color:#c9ced6;margin-top:7px}}
.gl{{position:absolute;font-size:54px;opacity:0}}
#gl-preco{{left:150px;top:200px;color:#1e3a6a;text-shadow:none}} #gl-media{{left:620px;top:290px;color:#9a6a10;text-shadow:none}} #gl-20{{left:640px;top:418px;color:#c0281a;text-shadow:none;font-size:64px}}
#cont{{position:absolute;left:150px;top:520px;opacity:0;background:rgba(15,17,21,.9);padding:16px 26px 14px;border-left:10px solid #3ddc84;border-radius:6px}}
#cont b{{display:block;font:900 120px/1 'Inter';color:#3ddc84}} #cont span{{display:block;font:900 36px 'Inter';color:#eceff3}} #cont small{{display:block;font:500 20px 'IBM Plex Mono';color:#a7afbb;margin-top:6px}}
.tag{{position:absolute;left:60px;top:90px;font:900 52px/1.05 'Inter';color:#fff;background:rgba(15,17,21,.85);padding:14px 24px;border-left:10px solid {COR};max-width:900px}}
#semc{{position:absolute;left:0;right:0;top:110px;margin:auto;width:max-content;font:900 56px 'Inter';color:#3ddc84;border:7px solid #3ddc84;padding:8px 26px;transform:rotate(-4deg);background:rgba(15,17,21,.75)}}
.andar{{position:absolute;right:60px;font-size:62px;opacity:0}} #an1{{top:470px}} #an2{{top:330px}} #an3{{top:200px}}
#cartela{{background:#0f1115}}
#ct-luz{{position:absolute;inset:0;background:radial-gradient(ellipse 60% 45% at 50% 40%,#2a1e10 0%,#15120e 55%,#0b0c0f 100%)}}
#ct-logo{{position:absolute;left:304px;top:150px;width:472px}}
#ct-t{{position:absolute;left:0;right:0;top:360px;text-align:center;font:500 96px 'Newsreader';color:#eceff3}} #ct-t i{{font-weight:600;color:{COR}}}
#ct-url{{position:absolute;left:0;right:0;top:500px;text-align:center;font:900 62px 'Inter';color:#fff}}
#ct-bio{{position:absolute;left:0;right:0;top:590px;text-align:center;font:500 32px 'IBM Plex Mono';color:{COR};letter-spacing:.04em}}
#ct-sec{{position:absolute;left:0;right:0;top:680px;text-align:center;font:500 24px 'IBM Plex Mono';color:#a7afbb;letter-spacing:.18em}}
#ct-fontes{{position:absolute;left:60px;right:60px;bottom:26px;text-align:center;font:500 18px/1.4 'IBM Plex Mono';color:#8a92a0}}
#caps{{position:absolute;inset:0;z-index:30}}
.cap{{position:absolute;left:0;right:0;top:850px;display:flex;justify-content:center;opacity:0}}
.cap span{{display:inline-block;background:{COR};color:#000;font:900 54px/1.12 'Inter';padding:6px 18px 8px;border-radius:6px;box-shadow:0 6px 18px rgba(0,0,0,.3)}}
</style></head><body>
<div id="root" data-composition-id="video" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1080">
{VIDEOS}
{chr(10).join(OVS)}
<div id="cartela" class="clip ov" data-start="{C['cartela']:.3f}" data-duration="{TOTAL - C['cartela']:.3f}" data-track-index="35">{CART}</div>
<div id="caps" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="36">{''.join(f'<div class="cap" id="cap{i}"><span>{b["txt"]}</span></div>' for i, b in enumerate(leg))}</div>
<audio id="voz" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="37" data-volume="1" src="assets/audio/narracao.wav"></audio>
<audio id="trilha" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="38" data-volume="1" data-fade-in="0.3" data-fade-out="1.5" src="assets/audio/trilha_mix.wav"></audio>
{sfx}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
const C = {json.dumps(C)}, M = {json.dumps(M)}, LEG = {json.dumps(leg, ensure_ascii=False)}, XF = {XF}, INI = {json.dumps(INI)};
const enter = 'power3.out';
for (let k = 1; k < 10; k++) tl.fromTo('#v' + k, {{ opacity: 0 }}, {{ opacity: 1, duration: XF, ease: 'none' }}, INI[k]);
tl.fromTo('#v0', {{ scale: 1.0 }}, {{ scale: 1.14, duration: INI[1] + XF, ease: 'none' }}, 0);                 // abertura: a câmera se aproxima
[1, 3, 4, 5, 6, 7, 8].forEach(k => tl.fromTo('#v' + k, {{ scale: 1.0 }}, {{ scale: 1.07, duration: INI[k + 1] - INI[k] + XF, ease: 'none' }}, INI[k]));
tl.fromTo('#v2', {{ scale: 1.02 }}, {{ scale: 1.0, duration: INI[3] - INI[2], ease: 'none' }}, INI[2]);
tl.fromTo('#v9', {{ scale: 1.14 }}, {{ scale: 1.0, duration: INI[10] - INI[9] + XF, ease: 'power1.out' }}, INI[9]);   // fechamento: a câmera se afasta
document.querySelectorAll('.cred').forEach(el => tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: .4 }}, +el.dataset.start));
// capa: já pronta no quadro 0, sai antes do gancho
tl.to('#o-capa', {{ opacity: 0, y: -30, duration: .3, ease: 'power2.in' }}, .85);
// exemplo do preço "de"
tl.fromTo('#ex s', {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: .4, ease: enter }}, M.etiqueta - .2);
tl.fromTo('#ex b', {{ opacity: 0, scale: .9 }}, {{ opacity: 1, scale: 1, duration: .4, ease: enter }}, M.etiqueta + .5);
tl.fromTo('#ex-selo', {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: .22, ease: 'power4.in' }}, M.etiqueta + .9);
tl.fromTo('#q', {{ opacity: 0, scale: .7 }}, {{ opacity: 1, scale: 1, duration: .45, ease: 'back.out(2)' }}, M.entao + .2);
// cartão 1: o radar no celular
tl.fromTo('#card1', {{ opacity: 0, y: 40, rotation: 6 }}, {{ opacity: 1, y: 0, rotation: 2, duration: .45, ease: enter }}, M.black4 - .15);
tl.to('#card1 .cimg', {{ backgroundPositionY: -120, duration: 1.8, ease: 'power1.inOut' }}, M.black4 + .3);
tl.to('#card1', {{ opacity: 0, y: -24, duration: .3 }}, M.black4 + 1.95);
// gráfico
tl.fromTo('#gl-preco', {{ opacity: 0 }}, {{ opacity: 1, duration: .4 }}, M.media - .1);
tl.fromTo('#gl-media', {{ opacity: 0, x: -10 }}, {{ opacity: 1, x: 0, duration: .4 }}, M.media + .1);
tl.fromTo('#gl-20', {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: .3, ease: enter }}, M.p20);
tl.fromTo('#cont', {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: .4, ease: enter }}, M.mais - .15);
tl.from('#cont b', {{ textContent: 0, duration: .9, snap: {{ textContent: 1 }}, ease: 'power2.out' }}, M.mais - .15);
// etiquetas da lista
['#o-t1 .tag', '#o-t2 .tag', '#o-t3 .tag', '#o-t4 .tag'].forEach(s => {{ const el = document.querySelector(s); tl.fromTo(el, {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: .25, ease: enter }}, +el.parentNode.dataset.start); }});
tl.fromTo('#semc', {{ opacity: 0, scale: 1.7 }}, {{ opacity: 1, scale: 1, duration: .22, ease: 'power4.in' }}, M.links - .1);
// castelo de cartas: os andares ganham nome no ritmo da fala
tl.fromTo('#an1', {{ opacity: 0, x: 20 }}, {{ opacity: 1, x: 0, duration: .35 }}, M.oitenta + 2.2);
tl.fromTo('#an2', {{ opacity: 0, x: 20 }}, {{ opacity: 1, x: 0, duration: .35 }}, M.como - .1);
tl.fromTo('#an3', {{ opacity: 0, x: 20 }}, {{ opacity: 1, x: 0, duration: .35 }}, M.noticias - .1);
tl.fromTo('#card2', {{ opacity: 0, y: 40, rotation: -6 }}, {{ opacity: 1, y: 0, rotation: -2, duration: .45, ease: enter }}, M.oitenta - .05);
tl.to('#card2', {{ opacity: 0, y: -24, duration: .3 }}, M.oitenta + 1.9);
// cartela
tl.fromTo('#cartela', {{ opacity: 0 }}, {{ opacity: 1, duration: .45 }}, C.cartela);
tl.fromTo('#ct-logo', {{ opacity: 0, scale: .9 }}, {{ opacity: 1, scale: 1, duration: .6, ease: enter }}, M.elite - .1);
tl.fromTo('#ct-t', {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: .5, ease: enter }}, M.elite + .9);
tl.fromTo('#ct-url', {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: .5, ease: enter }}, M.link + .5);
tl.fromTo('#ct-bio', {{ opacity: 0 }}, {{ opacity: 1, duration: .4 }}, M.link);
tl.fromTo('#ct-sec', {{ opacity: 0 }}, {{ opacity: 1, duration: .5 }}, M.link + 1.4);
tl.fromTo('#ct-fontes', {{ opacity: 0 }}, {{ opacity: 1, duration: .6 }}, C.cartela + .8);
// legendas; na cartela sobem para não cobrir o endereço
tl.set('#caps', {{ y: 0 }}, 0); tl.set('#caps', {{ y: 60 }}, C.cartela);
LEG.forEach((b, i) => {{ tl.fromTo('#cap' + i, {{ opacity: 0, scale: .92 }}, {{ opacity: 1, scale: 1, duration: .12, ease: 'power2.out' }}, b.ini); tl.set('#cap' + i, {{ opacity: 0 }}, b.fim); }});
tl.to({{}}, {{ duration: {TOTAL} }}, 0);
window.__timelines = window.__timelines || {{}}; window.__timelines['video'] = tl;
</script></body></html>"""
(P / "index.html").write_text(HTML, encoding="utf-8"); (P / "hyperframes.json").write_text('{ "name": "elite-black-de-verdade" }\n')
print("ok", TOTAL, len(leg), "blocos", {k: round(v, 2) for k, v in C.items()})
for b in leg: print(round(b["ini"], 2), b["txt"])
