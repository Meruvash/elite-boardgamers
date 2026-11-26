"""Gera hf/index.html: "Como se joga Ticket to Ride?" (Elite Boardgamers), vertical 1080x1920, ~60 s.
Formato "Como se joga" (docs/video/REFERENCIA_COMO_SE_JOGA.md): mapa estilizado desenhado por nós (posição aproximada das
cidades, rotas e cores nossas), cartas de vagão, bilhetes e trens em código. Nada da arte da caixa, nenhuma imagem de IA.
Regras: manual Galápagos e manual Days of Wonder (2015). Uso: python3 montar.py
"""
import json, re, difflib, unicodedata, math
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
def alinhar(fid):
    toks, ws = FALAS[fid]["texto"].split(), pw(fid)
    a, b = [norm(x) for x in toks], [norm(w["w"]) for w in ws]
    out = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): out[i1 + k] = (ws[j1 + k]["s"], ws[j1 + k]["e"])
        elif i2 > i1:
            s = ws[j1]["s"] if j1 < len(ws) else ws[-1]["e"]; e = ws[j2 - 1]["e"] if j2 > j1 else s + .3
            for k in range(i2 - i1): out[i1 + k] = (s + (e - s) * k / (i2 - i1), s + (e - s) * (k + 1) / (i2 - i1))
    return list(zip(toks, out))
blocos = []
for fid in range(1, 11):
    cur = []
    for tok, (s, e) in alinhar(fid):
        cur.append((tok, s, e))
        if len(cur) == 3 or re.search(r"[.,:?!]$", tok): blocos.append(cur); cur = []
    if cur: blocos.append(cur)
LEG = []
for i, b in enumerate(blocos):
    prox = blocos[i + 1][0][1] if i + 1 < len(blocos) else TOTAL
    LEG.append({"ini": round(b[0][1], 3), "fim": round(min(prox, b[-1][2] + .35), 3), "w": [[t, round(s, 3)] for t, s, _ in b]})
CAPA_FIM = 1.9
LEG = [l for l in LEG if l["fim"] > CAPA_FIM]
for l in LEG: l["ini"] = max(l["ini"], CAPA_FIM)

M = {k: ts(*v) for k, v in {
    "bilhete1": (1, "bilhete"), "tirar": (1, "tirar"), "pode": (1, "pode"), "saida1": (1, "saida"),
    "palavra": (2, "palavra"), "bilhete2": (2, "bilhete"),
    "secretos": (3, "secretos"), "cidades": (3, "cidades"), "ligou": (3, "Ligou"), "ganha": (3, "ganha"), "nao": (3, "Nao"), "perde": (3, "perde"),
    "vez": (4, "vez"), "compra": (4, "compra"), "vagao": (4, "vagao"), "pega": (4, "pega"), "ocupa": (4, "ocupa"), "pagando": (4, "pagando"), "cor": (4, "cor"),
    "agora": (5, "Agora"), "longa": (5, "longa"), "manual": (5, "manual"), "tres": (5, "tres"), "quatro": (5, "quatro"), "seis": (5, "seis"), "quinze": (5, "15"),
    "locomotiva": (6, "locomotiva"), "qualquer": (6, "qualquer"), "pegar": (6, "pegar"), "compra6": (6, "compra"), "essa": (6, "essa"),
    "dois": (7, "dois"), "todo": (7, "todo"), "maior": (7, "maior"), "dez": (7, "10"),
    "historia": (8, "historia"), "n1900": (8, "1900"), "amigos": (8, "amigos"), "milhao": (8, "milhao"), "cidades8": (8, "cidades"), "sete": (8, "sete"),
    "fechar": (9, "fechar"), "pirraca": (9, "pirraca"), "segue": (10, "segue")}.items()}
M["f"] = {i: FI[i]["inicio"] for i in FI}

# ---------- mapa (coordenadas do mundo 1080 x 1920; posições aproximadas, desenho nosso) ----------
CID = {"Seattle": (190, 190), "Portland": (160, 270), "S. Francisco": (130, 540), "Los Angeles": (210, 720), "Helena": (430, 260),
       "Salt Lake": (370, 450), "Phoenix": (340, 790), "Denver": (530, 520), "El Paso": (490, 900), "Duluth": (650, 240),
       "Kansas City": (660, 520), "Oklahoma": (650, 700), "Dallas": (660, 860), "Houston": (730, 960), "Chicago": (790, 370),
       "St. Louis": (760, 530), "Little Rock": (760, 730), "New Orleans": (850, 950), "Nashville": (860, 620), "Atlanta": (920, 760),
       "Miami": (985, 1060), "Washington": (965, 470), "New York": (965, 330)}
CORES = {"verde": "#3f9a4a", "azul": "#2f6fbf", "vermelho": "#c8402e", "amarelo": "#e8b830", "preto": "#2a2a2e", "branco": "#f2efe6", "rosa": "#d46aa8", "laranja": "#e8862a", "cinza": "#9a9a9a"}
ROTAS = [("Seattle", "Portland", 1, "cinza"), ("Seattle", "Helena", 4, "amarelo"), ("Portland", "S. Francisco", 4, "verde"), ("S. Francisco", "Los Angeles", 2, "amarelo"),
         ("S. Francisco", "Salt Lake", 5, "branco"), ("Los Angeles", "Phoenix", 3, "cinza"), ("Los Angeles", "El Paso", 6, "preto"), ("Helena", "Duluth", 4, "laranja"),
         ("Helena", "Salt Lake", 3, "rosa"), ("Salt Lake", "Denver", 3, "vermelho"), ("Phoenix", "Denver", 5, "branco"), ("Phoenix", "El Paso", 3, "cinza"),
         ("Denver", "Kansas City", 4, "preto"), ("El Paso", "Dallas", 4, "vermelho"), ("Denver", "Oklahoma", 4, "vermelho"), ("Duluth", "Chicago", 3, "vermelho"),
         ("Kansas City", "St. Louis", 2, "azul"), ("Oklahoma", "Little Rock", 2, "cinza"), ("Dallas", "Houston", 1, "cinza"), ("Houston", "New Orleans", 2, "cinza"),
         ("Chicago", "St. Louis", 2, "verde"), ("St. Louis", "Little Rock", 2, "branco"), ("Little Rock", "New Orleans", 3, "verde"), ("St. Louis", "Nashville", 2, "cinza"),
         ("Nashville", "Atlanta", 1, "cinza"), ("Atlanta", "Miami", 5, "azul"), ("New Orleans", "Atlanta", 4, "amarelo"), ("Chicago", "New York", 5, "laranja"),
         ("Washington", "New York", 2, "preto"), ("Nashville", "Washington", 4, "amarelo"), ("Oklahoma", "Dallas", 2, "cinza"), ("Kansas City", "Oklahoma", 2, "cinza")]
RID = {(a, b): k for k, (a, b, _, _) in enumerate(ROTAS)}
def segs(k):
    a, b, n, cor = ROTAS[k]; (x1, y1), (x2, y2) = CID[a], CID[b]
    L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; ang = math.degrees(math.atan2(uy, ux))
    pad = 22; usable = L - 2 * pad; sl = usable / n; w = sl - 6
    return [(x1 + ux * (pad + sl * (i + .5)), y1 + uy * (pad + sl * (i + .5)), w, ang) for i in range(n)]
rotas = ""; trens = ""
for k, (a, b, n, cor) in enumerate(ROTAS):
    for i, (cx, cy, w, ang) in enumerate(segs(k)):
        rotas += f'<i class="seg" style="left:{cx - w / 2:.1f}px;top:{cy - 11:.1f}px;width:{w:.1f}px;background:{CORES[cor]};transform:rotate({ang:.2f}deg)"></i>'
        trens += f'<i class="trem" id="r{k}t{i}" style="left:{cx - w / 2 + 3:.1f}px;top:{cy - 9:.1f}px;width:{w - 6:.1f}px;transform:rotate({ang:.2f}deg)"></i>'
cids = "".join(f'<div class="cid" style="left:{x - 15}px;top:{y - 15}px"></div><div class="cn" style="left:{x - 80}px;top:{y + 14}px">{n}</div>' for n, (x, y) in CID.items())
TERRA = "M120 150 L320 120 L560 150 L700 190 L800 250 L900 230 L1000 250 L1030 380 L1000 520 L960 640 L1010 760 L1040 1050 L980 1110 L930 960 L850 1000 L760 1010 L690 1050 L640 960 L560 930 L480 980 L420 900 L300 860 L200 790 L120 680 L80 520 L100 330 Z"
# pista de pontos em volta do mapa
pista = "".join(f'<div class="pt" style="left:{40 + i * 40}px;top:42px">{i}</div>' for i in range(0, 25, 1))
mapa = (f'<div id="mapa"><svg viewBox="0 0 1080 1220" width="1080" height="1220"><defs><pattern id="ond" width="40" height="20" patternUnits="userSpaceOnUse"><path d="M0 10 q10 -8 20 0 t20 0" stroke="#9cc3cf" fill="none" stroke-width="2"/></pattern></defs>'
        f'<rect x="30" y="30" width="1020" height="1160" rx="24" fill="#b9d6dc"/><rect x="30" y="30" width="1020" height="1160" rx="24" fill="url(#ond)" opacity=".6"/>'
        f'<path d="{TERRA}" fill="#efe1bd" stroke="#a88a5a" stroke-width="5"/><path d="{TERRA}" fill="none" stroke="#d8c49a" stroke-width="18" opacity=".5"/>'
        f'<rect x="30" y="30" width="1020" height="1160" rx="24" fill="none" stroke="#6a4a2a" stroke-width="14"/></svg>{pista}</div>')

# cartas de vagão, bilhetes, estoque
VAG = '<svg viewBox="0 0 60 30" width="70"><rect x="4" y="4" width="52" height="16" rx="3" fill="rgba(255,255,255,.85)"/><circle cx="16" cy="24" r="5" fill="#222"/><circle cx="44" cy="24" r="5" fill="#222"/></svg>'
def cv(i, cor, x, y, loco=False):
    bg = "linear-gradient(90deg,#c8402e,#e8b830,#3f9a4a,#2f6fbf,#d46aa8)" if loco else CORES[cor]
    return f'<div class="cv" id="{i}" style="left:{x}px;top:{y}px;background:{bg}">{VAG}<b>{"LOCOMOTIVA" if loco else ""}</b></div>'
MERC = [("verde", False), ("azul", False), ("", True), ("vermelho", False), ("amarelo", False)]
merc = "".join(cv(f"k{i}", c, 60 + i * 170, 1250, l) for i, (c, l) in enumerate(MERC)) + '<div class="cv monte" style="left:910px;top:1250px">?</div>'
mao = "".join(cv(f"h{i}", c, 60 + i * 120, 1460) for i, c in enumerate(["verde", "verde", "preto", "verde", "rosa"]))
def bil(i, a, b, v, x, y, extra=""):
    return f'<div class="bil" id="{i}" style="left:{x}px;top:{y}px"><small>BILHETE DE DESTINO</small><div>{a}<br>→ {b}</div><b>{v}</b>{extra}</div>'
bils = bil("bA", "Chicago", "New Orleans", 7, 60, 1650, '<i class="res" id="resA"></i>') + bil("bB", "Seattle", "New York", 22, 400, 1650)
estoque = '<div id="estq"><svg viewBox="0 0 60 30" width="80"><rect x="4" y="6" width="52" height="16" rx="4" fill="#e8862a" stroke="#7a3a0a" stroke-width="2"/></svg><span id="n45">45</span><span id="n2">2</span><small>TRENS</small></div>'

MUNDO = f"""<div id="world"><div id="mesa"></div>{mapa}<div id="rotas">{rotas}</div><div id="trens">{trens}</div>{cids}
<div class="rot" style="left:60px;top:1215px">CARTAS ABERTAS</div>{merc}<div class="rot" style="left:60px;top:1425px">SUA MÃO</div>{mao}
<div class="rot" style="left:60px;top:1615px">SEUS BILHETES (SECRETOS)</div>{bils}{estoque}
<div id="loco1"><svg viewBox="0 0 80 50" width="90"><rect x="8" y="14" width="44" height="22" rx="4" fill="#2a2a2e"/><rect x="40" y="4" width="18" height="32" rx="3" fill="#c8402e"/><rect x="14" y="4" width="8" height="12" fill="#2a2a2e"/><circle cx="20" cy="40" r="7" fill="#555"/><circle cx="44" cy="40" r="7" fill="#555"/><path d="M60 30 L74 40 H56Z" fill="#e8b830"/></svg></div>
</div>"""

COR = "#E98B1E"
CSS = f"""
@font-face{{font-family:'Inter';src:url(assets/fonts/inter-latin-900-normal.woff2) format('woff2');font-weight:900}}
@font-face{{font-family:'Newsreader';src:url(assets/fonts/newsreader-latin-600-italic.woff2) format('woff2');font-weight:600;font-style:italic}}
@font-face{{font-family:'IBM Plex Mono';src:url(assets/fonts/ibm-plex-mono-latin-500-normal.woff2) format('woff2');font-weight:500}}
*{{box-sizing:border-box;margin:0}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#2a1a0e}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#2a1a0e}}
#world{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0}} #world > *{{position:absolute}}
#mesa{{left:-1200px;top:-1200px;width:3480px;height:4320px;background:repeating-linear-gradient(90deg,rgba(0,0,0,.05) 0 3px,transparent 3px 40px),linear-gradient(180deg,#6b4529,#5a3a20 50%,#6b4529)}}
#mapa{{left:0;top:0;width:1080px;height:1220px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.45))}}
.pt{{position:absolute;width:34px;height:22px;font:900 12px/22px 'Inter';text-align:center;color:#6a4a2a;background:#f4ead2;border-radius:4px;opacity:.85}}
#rotas,#trens{{left:0;top:0}} .seg{{position:absolute;height:22px;border-radius:5px;border:2px solid rgba(0,0,0,.45);transform-origin:50% 50%;box-shadow:0 2px 2px rgba(0,0,0,.25)}}
.trem{{position:absolute;height:18px;border-radius:6px;background:linear-gradient(180deg,#f4a040,#d0701a);border:2px solid #6a2e04;transform-origin:50% 50%;opacity:0;box-shadow:0 3px 3px rgba(0,0,0,.4)}}
.trem.az{{background:linear-gradient(180deg,#5a90d8,#2a5aa8);border-color:#0a2a5a}}
.cid{{width:30px;height:30px;border-radius:50%;background:#fff8e8;border:5px solid #6a2e1a;box-shadow:0 3px 4px rgba(0,0,0,.35)}}
.cn{{width:160px;text-align:center;font:900 19px 'Inter';color:#3a2414;text-shadow:0 0 4px #fff8e8,0 0 4px #fff8e8}}
.rot{{font:900 20px 'Inter';color:rgba(255,248,232,.9);letter-spacing:.12em}}
.cv{{width:150px;height:150px;border-radius:14px;border:4px solid #fff8e8;box-shadow:0 8px 14px rgba(0,0,0,.4);display:flex;flex-direction:column;align-items:center;justify-content:center}}
.cv b{{font:900 15px 'Inter';color:#fff;text-shadow:0 2px 3px rgba(0,0,0,.6);margin-top:8px}}
.cv.monte{{background:repeating-linear-gradient(45deg,#3a2a1a 0 10px,#4a3624 10px 20px);font:900 60px 'Inter';color:#e8c27a;width:120px}}
#mao .cv{{width:120px}} .cv[id^=h]{{width:120px;height:130px}}
.bil{{width:310px;height:220px;background:#f6ecd0;border-radius:16px;border:4px solid #8a6a3a;box-shadow:0 8px 14px rgba(0,0,0,.4);padding:14px 18px;font:900 34px/1.15 'Inter';color:#3a2414}}
.bil small{{display:block;font:900 14px 'Inter';letter-spacing:.12em;color:#8a6a3a;margin-bottom:10px}} .bil b{{position:absolute;right:16px;bottom:10px;font:900 54px 'Inter';color:#2f6fbf}}
.res{{position:absolute;left:16px;bottom:12px;font:900 54px 'Inter';font-style:normal}}
#estq{{left:780px;top:1660px;width:240px;text-align:center}} #estq span{{display:block;font:900 110px/1 'Inter';color:#fff8e8;-webkit-text-stroke:5px #3a1a08;paint-order:stroke fill}}
#estq #n2{{position:absolute;left:0;right:0;top:48px;color:#ff7a5a;opacity:0}} #estq small{{display:block;font:900 22px 'Inter';color:#fff8e8;letter-spacing:.12em}}
#loco1{{left:0;top:0;opacity:0}}
#topo{{position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(180deg,rgba(20,12,6,.72),rgba(20,12,6,.35) 60%,rgba(20,12,6,0))}}
#base{{position:absolute;left:0;right:0;bottom:0;height:240px;background:linear-gradient(0deg,rgba(20,12,6,.7),rgba(20,12,6,0))}}
#marca{{position:absolute;left:48px;top:150px;font:500 26px 'IBM Plex Mono';color:rgba(255,248,232,.8)}}
#capa{{position:absolute;left:0;right:0;top:250px;text-align:center}}
#capa-tag{{display:inline-block;background:{COR};color:#111;font:900 38px 'Inter';letter-spacing:.05em;padding:10px 24px}}
#capa-t{{font:900 180px/1 'Inter';color:#fff;-webkit-text-stroke:8px #1c1008;paint-order:stroke fill;margin-top:22px}}
#capa-sub{{font:italic 600 56px 'Newsreader';color:#fff2d8;margin-top:14px;text-shadow:0 3px 14px rgba(0,0,0,.9)}}
#caps{{position:absolute;left:60px;right:60px;top:330px;height:200px}}
.cap{{position:absolute;left:0;right:0;top:0;text-align:center;opacity:0;font:900 78px/1.15 'Inter';color:#fff;-webkit-text-stroke:6px #1c1008;paint-order:stroke fill}}
.cap span{{display:inline-block;padding:2px 14px;border-radius:12px;margin:0 2px;background:rgba(233,139,30,0)}}
.big{{position:absolute;left:0;right:0;text-align:center;font:900 200px/1 'Inter';color:#fff;-webkit-text-stroke:9px #1c1008;paint-order:stroke fill;opacity:0}}
.pop{{position:absolute;font:900 90px 'Inter';color:#fff;-webkit-text-stroke:7px #1c1008;paint-order:stroke fill;opacity:0}}
.selo{{position:absolute;font:900 54px 'Inter';color:#fff;background:#b8402a;border:6px solid #ffd27a;border-radius:14px;padding:8px 24px;opacity:0}}
.fonte{{position:absolute;left:48px;right:48px;bottom:56px;text-align:center;font:500 26px 'IBM Plex Mono';color:rgba(255,248,232,.85);opacity:0}}
#escuro{{position:absolute;inset:0;background:rgba(15,9,4,.72);opacity:0}}
#bilG{{position:absolute;left:290px;top:820px;opacity:0}}
#tabela{{position:absolute;left:150px;top:640px;width:780px;opacity:0;background:rgba(20,12,6,.88);border:5px solid #ffd27a;border-radius:18px;padding:16px 26px}}
#tabela div{{background:rgba(233,139,30,0);border-radius:8px;padding:0 10px;display:flex;justify-content:space-between;font:900 46px/1.35 'Inter';color:#d8ccb0}} #tabela div.on{{color:#fff;background:rgba(233,139,30,.35);border-radius:8px;padding:0 10px}}
#tabela .h{{font-size:24px;color:#ffd27a;letter-spacing:.1em}}
#jornal{{position:absolute;left:90px;top:620px;width:900px;opacity:0;background:#efe4c8;border:6px double #3a2414;padding:22px 30px;box-shadow:0 20px 40px rgba(0,0,0,.5);transform:rotate(-2deg)}}
#jornal h2{{font:italic 600 46px 'Newsreader';color:#3a2414;text-align:center;border-bottom:3px solid #3a2414;padding-bottom:8px}}
#jornal p{{font:900 66px/1.15 'Inter';color:#2a1a0e;text-align:center;margin-top:16px}} #jornal p span{{display:block;opacity:0}}
#fim{{position:absolute;left:0;right:0;bottom:120px;text-align:center;opacity:0}} #fim img{{width:420px}} #fim div{{font:500 30px 'IBM Plex Mono';color:#fff8e8;margin-top:16px}}
"""
TAB = "".join(f'<div id="tb{n}"><span>{n} vagão{"" if n == 1 else "es"}</span><span>{p} pts</span></div>' for n, p in [(1, 1), (2, 2), (3, 4), (4, 7), (5, 10), (6, 15)])
TELA = f"""<div id="topo"></div><div id="base"></div><div id="marca">@eliteboardgamers</div><div id="escuro"></div>
<div id="bilG">{bil("bG", "Chicago", "New Orleans", 7, 0, 0)}</div>
<div class="big" id="bbil" style="top:560px;font-size:170px">BILHETE</div>
<div id="tabela"><div class="h"><span>ROTA</span><span>PONTOS NA HORA</span></div>{TAB}</div>
<div id="jornal"><h2>A aposta de 1900</h2><p><span id="j1">5 amigos</span><span id="j2">US$ 1 milhão</span><span id="j3">7 dias</span></p></div>
<div class="pop" id="pmais7" style="left:600px;top:760px;color:#7fe08a">+7</div><div class="pop" id="pmenos7" style="left:600px;top:760px;color:#ff7a5a">−7</div>
<div class="pop" id="p4" style="left:640px;top:820px">+4</div><div class="pop" id="p15" style="left:300px;top:820px">+15</div><div class="pop" id="p10" style="left:620px;top:820px">+10</div>
<div class="selo" id="s1rod" style="left:170px;top:640px">ÚLTIMA RODADA</div><div class="selo" id="sbloq" style="left:250px;top:640px">ROTA FECHADA</div>
<div class="selo" id="ssoum" style="left:230px;top:1000px;background:#3a2414">SÓ 1 CARTA</div>
<div class="fonte" id="f1">Regras: manual Galápagos e Days of Wonder (2015)</div><div class="fonte" id="f2">Tabela de pontos: manual, p. 4</div><div class="fonte" id="f3">Introdução do manual Days of Wonder (2015)</div>
<div id="capa"><div id="capa-tag">TICKET TO RIDE EM 1 MINUTO</div><div id="capa-t">TIRA<br>PONTO?</div><div id="capa-sub">o bilhete que vira contra você</div></div>
<div id="caps">{''.join(f'<div class="cap" id="c{i}">' + ''.join(f'<span id="c{i}w{j}">{t}</span>' for j, (t, _) in enumerate(l["w"])) + '</div>' for i, l in enumerate(LEG))}</div>
<div id="fim"><img src="assets/img/logo-eb-156.png"><div>guia completo: eliteboardgamers.com.br/como-jogar</div></div>"""

# rotas da história
CAMINHO = [RID[("Chicago", "St. Louis")], RID[("St. Louis", "Little Rock")], RID[("Little Rock", "New Orleans")]]
R3 = RID[("Little Rock", "New Orleans")]; R6 = RID[("Los Angeles", "El Paso")]
LONGO = [RID[("El Paso", "Dallas")], RID[("Dallas", "Houston")], RID[("Houston", "New Orleans")]]
BLOQ = RID[("St. Louis", "Little Rock")]
nseg = {k: ROTAS[k][2] for k in range(len(ROTAS))}
JS = """
const tl = gsap.timeline({ paused: true }); const W = '#world';
function cam(t, x, y, s, d = .9, sy = 1150, ease = 'power2.inOut') { tl.to(W, { x: 540 - x * s, y: sy - y * s, scale: s, duration: d, ease }, t); }
function trens(k, t, dur = .3, cls = '') { for (let i = 0; i < NSEG[k]; i++) { const id = '#r' + k + 't' + i; if (cls) tl.set(id, { background: 'linear-gradient(180deg,#5a90d8,#2a5aa8)', borderColor: '#0a2a5a' }, t);
  tl.fromTo(id, { opacity: 0, y: -30, scale: 1.3 }, { opacity: 1, y: 0, scale: 1, duration: dur, ease: 'back.out(2)', immediateRender: false }, t + i * .08); } }
function some(k, t) { for (let i = 0; i < NSEG[k]; i++) tl.to('#r' + k + 't' + i, { opacity: 0, duration: .2 }, t + i * .03); }
tl.set(W, { x: 540 - 600 * 1.0, y: 1150 - 640 * 1.0, scale: 1.0 }, 0); tl.set('#bilG', { scale: 1.6 }, 0);
// 1 · capa; o bilhete Chicago → New Orleans entra; "tirar pontos": −7
cam(0, 780, 760, 1.25, 3.0, 1150, 'power1.out');
tl.to('#capa', { opacity: 0, y: -40, duration: .35, ease: 'power2.in' }, CAPA_FIM - .35);
tl.to('#escuro', { opacity: .55, duration: .3 }, M.tirar - .6);
tl.fromTo('#bilG', { opacity: 0, y: 300, rotation: -10 }, { opacity: 1, y: 0, rotation: -3, duration: .45, ease: 'back.out(1.6)' }, M.tirar - .6);
tl.fromTo('#pmenos7', { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in' }, M.tirar + .1);
tl.to('#pmenos7', { opacity: 0, duration: .2 }, M.saida1);
tl.to('#bilG', { y: -8, rotation: 2, duration: .2, yoyo: true, repeat: 3 }, M.pode);
// 2 · BILHETE
cam(M.f[2] - .1, 870, 900, 1.55, .9);
tl.to('#bilG', { scale: 2.0, y: 60, rotation: 0, duration: .5, ease: 'power3.out' }, M.f[2] - .05);
tl.fromTo('#bbil', { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: .22, ease: 'power4.in' }, M.bilhete2 - .05);
tl.to(['#bbil', '#bilG'], { opacity: 0, duration: .3 }, M.f[3] - .2); tl.to('#escuro', { opacity: 0, duration: .3 }, M.f[3] - .2);
// 3 · bilhetes secretos; ligou: trens no caminho, +7; não ligou: falta um trecho, −7
cam(M.f[3] - .2, 300, 1760, 1.25, .8);
tl.to(['#bA', '#bB'], { rotationY: 180, duration: .25, yoyo: true, repeat: 1, stagger: .1 }, M.secretos);
cam(M.cidades - .4, 800, 660, 1.4, .8);
tl.to(['.cid'], { scale: 1.25, duration: .2, yoyo: true, repeat: 1 }, M.cidades);
CAMINHO.forEach((k, j) => trens(k, M.ligou + j * .25, .25));
tl.fromTo('#pmais7', { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in', immediateRender: false }, M.ganha);
tl.to('#pmais7', { opacity: 0, duration: .2 }, M.nao - .1);
some(CAMINHO[1], M.nao - .05);
tl.fromTo('#pmenos7', { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in', immediateRender: false }, M.perde);
tl.to('#pmenos7', { opacity: 0, duration: .2 }, M.f[4] - .15);
CAMINHO.forEach((k, j) => some(k, M.f[4] - .15));
// 4 · o turno: compra 2 cartas; pega bilhetes; ocupa a rota verde de 3 pagando 3 cartas verdes
cam(M.vez - .4, 540, 1450, 1.0, .8);
tl.to('#k0', { x: 600 - 60, y: 210, duration: .45, ease: 'power2.inOut' }, M.compra);
tl.to('#k1', { x: 780 - 230, y: 210, duration: .45, ease: 'power2.inOut' }, M.compra + .3);
tl.to(['#bA', '#bB'], { y: -26, duration: .18, yoyo: true, repeat: 1, stagger: .08 }, M.pega);
cam(M.ocupa - .3, 780, 820, 1.45, .7);
['#h0', '#h1', '#h3'].forEach((h, j) => tl.to(h, { x: 850 - 60 - j * 120, y: 840 - 1460, scale: .5, opacity: 0, duration: .5, ease: 'power2.in' }, M.pagando + j * .1));
trens(R3, M.pagando + .35, .3);
// 5 · a saída: rota longa; tabela do manual; +4 e +15
tl.fromTo('#p4', { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in' }, M.agora);
tl.to('#p4', { opacity: 0, duration: .2 }, M.longa);
tl.to('#escuro', { opacity: .6, duration: .3 }, M.manual - .3);
tl.fromTo('#tabela', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .35 }, M.manual - .3);
tl.to('#f2', { opacity: 1, duration: .3 }, M.manual); tl.to('#f2', { opacity: 0, duration: .3 }, M.f[6] - .2);
tl.set('#tb3', { backgroundColor: 'rgba(233,139,30,.45)', color: '#fff' }, M.tres); tl.set('#tb3', { backgroundColor: 'rgba(233,139,30,0)', color: '#d8ccb0' }, M.seis); tl.set('#tb6', { backgroundColor: 'rgba(233,139,30,.45)', color: '#fff' }, M.seis);
tl.to(['#tabela', '#escuro'], { opacity: 0, duration: .25 }, M.seis + .3);
cam(M.seis, 350, 810, 1.35, .5);
trens(R6, M.seis + .25, .2);
tl.fromTo('#p15', { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: .22, ease: 'power4.in' }, M.quinze + .05);
tl.to('#p15', { opacity: 0, duration: .25 }, M.f[6] - .1);
// 6 · locomotiva coringa; pegou aberta: só 1 carta
cam(M.f[6] - .2, 540, 1320, 1.25, .8);
tl.to('#k2', { scale: 1.2, y: -30, duration: .25, yoyo: true, repeat: 1 }, M.locomotiva);
tl.to('#k2', { rotation: 360, duration: .7, ease: 'power2.inOut' }, M.qualquer - .2);
tl.to('#k2', { x: 900 - 400, y: 210, duration: .45, ease: 'power2.inOut' }, M.pegar);
tl.fromTo('#ssoum', { opacity: 0, scale: 1.7 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in' }, M.compra6);
tl.to('#k3', { x: 10, duration: .06, yoyo: true, repeat: 5 }, M.compra6 + .1);
tl.to('#ssoum', { opacity: 0, duration: .2 }, M.f[7] - .15);
// 7 · estoque 45 → 2; última rodada; maior caminho +10
cam(M.f[7] - .2, 880, 1760, 1.3, .7);
tl.to('#n45', { opacity: 0, duration: .15 }, M.dois); tl.fromTo('#n2', { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: .2, immediateRender: false }, M.dois);
tl.fromTo('#s1rod', { opacity: 0, scale: 1.7 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in' }, M.todo);
tl.to('#s1rod', { opacity: 0, duration: .2 }, M.maior - .2);
cam(M.maior - .4, 620, 860, 1.05, .6);
LONGO.forEach((k, j) => trens(k, M.maior - .2 + j * .15, .2));
[R3].concat(LONGO).concat([R6]).forEach(k => { for (let i = 0; i < NSEG[k]; i++) tl.to('#r' + k + 't' + i, { boxShadow: '0 0 0 6px rgba(255,230,120,.95)', duration: .2, yoyo: true, repeat: 3 }, M.dez - .2); });
tl.fromTo('#p10', { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in' }, M.dez);
tl.to('#p10', { opacity: 0, duration: .2 }, M.f[8] - .1);
// 8 · a aposta de 1900 (introdução do manual): jornal + locomotiva atravessando o mapa
cam(M.f[8] - .2, 560, 640, .9, 1.0);
tl.to('#escuro', { opacity: .45, duration: .3 }, M.n1900 - .3);
tl.fromTo('#jornal', { opacity: 0, y: 60, rotation: -6 }, { opacity: 1, y: 0, rotation: -2, duration: .4, ease: 'back.out(1.5)' }, M.n1900 - .3);
tl.to('#f3', { opacity: 1, duration: .3 }, M.n1900); tl.to('#f3', { opacity: 0, duration: .3 }, M.f[9] - .2);
tl.to('#j1', { opacity: 1, duration: .2 }, M.amigos - .1); tl.to('#j2', { opacity: 1, duration: .2 }, M.milhao - .1); tl.to('#j3', { opacity: 1, duration: .2 }, M.sete - .1);
tl.set('#loco1', { x: 130, y: 500, opacity: 1 }, M.historia);
tl.to('#loco1', { keyframes: [{ x: 360, y: 420, duration: 1.4 }, { x: 520, y: 490, duration: 1.4 }, { x: 760, y: 340, duration: 1.6 }, { x: 930, y: 300, duration: 1.4 }], ease: 'none' }, M.historia);
tl.to(['#jornal', '#escuro', '#loco1'], { opacity: 0, duration: .3 }, M.f[9] - .2);
// 9 · rota fechada por outro jogador
cam(M.f[9] - .2, 770, 640, 1.6, .6);
trens(BLOQ, M.fechar - .2, .22, 'az');
tl.fromTo('#sbloq', { opacity: 0, scale: 1.7 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in' }, M.fechar + .1);
tl.to('#sbloq', { opacity: 0, duration: .2 }, M.f[10] - .2);
// 10 · a mesa inteira e o fecho
cam(M.f[10] - .2, 540, 980, .62, 1.4, 1000, 'power2.out');
tl.fromTo('#fim', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .5 }, M.segue);
tl.to('#f1', { opacity: 1, duration: .3 }, M.segue);
LEG.forEach((b, i) => { tl.set('#c' + i, { opacity: 1 }, b.ini); tl.set('#c' + i, { opacity: 0 }, b.fim);
  b.w.forEach(([t, s], j) => { tl.set('#c' + i + 'w' + j, { backgroundColor: '#E98B1E' }, Math.max(s, b.ini)); if (j + 1 < b.w.length) tl.set('#c' + i + 'w' + j, { backgroundColor: 'rgba(233,139,30,0)' }, Math.max(b.w[j + 1][1], b.ini)); }); });
tl.to({}, { duration: TOTAL }, 0);
window.__timelines = window.__timelines || {}; window.__timelines['video'] = tl;
"""
CONST = (f"const TOTAL={TOTAL}, CAPA_FIM={CAPA_FIM}, M={json.dumps(M)}, LEG={json.dumps(LEG, ensure_ascii=False)}, NSEG={json.dumps(nseg)}, "
         f"CAMINHO={json.dumps(CAMINHO)}, R3={R3}, R6={R6}, LONGO={json.dumps(LONGO)}, BLOQ={BLOQ};")
SFX = [("cartas", M["bilhete1"], .45), ("carimbo", M["tirar"] + .1, .55), ("carimbo", M["bilhete2"], .45), ("trem", M["ligou"], .5), ("carimbo", M["perde"], .45),
       ("cartas", M["compra"], .4), ("cartas", M["compra"] + .3, .35), ("trem", M["pagando"] + .35, .5), ("pop", M["agora"], .4), ("trem", M["seis"] + .25, .5),
       ("brilho", M["quinze"], .4), ("cartas", M["pegar"], .4), ("carimbo", M["compra6"], .45), ("apito", M["todo"], .45), ("brilho", M["dez"], .45), ("apito", M["historia"] + .2, .35),
       ("trem", M["fechar"] - .2, .45), ("carimbo", M["fechar"] + .1, .45), ("brilho", M["segue"], .35)]
sfx = "\n".join(f'<audio id="sx{n}" class="clip" data-start="{s:.3f}" data-duration="0.6" data-track-index="{40 + n}" data-volume="{v}" src="assets/audio/sfx/{f}.mp3"></audio>' for n, (f, s, v) in enumerate(SFX))
HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Como se joga Ticket to Ride?</title>
<script src="assets/lib/gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="video" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
<div id="cam" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="1" style="position:absolute;inset:0">{MUNDO}</div>
<div id="tela" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="2" style="position:absolute;inset:0">{TELA}</div>
<audio id="voz" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-volume="1" src="assets/audio/narracao.wav"></audio>
<audio id="trilha" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="1" data-fade-in="0.2" data-fade-out="1.5" src="assets/audio/trilha_mix.wav"></audio>
{sfx}
</div><script>{CONST}{JS}</script></body></html>"""
(P / "index.html").write_text(HTML, encoding="utf-8"); (P / "hyperframes.json").write_text('{ "name": "elite-como-se-joga-ticket-to-ride" }\n')
print("ok", TOTAL, len(LEG), "blocos")
