"""Gera hf/index.html: "Como se joga Everdell?" (Elite Boardgamers), vertical 1080x1920, ~61 s.
Formato "Como se joga" (docs/video/REFERENCIA_COMO_SE_JOGA.md): a mesa do jogo inteira desenhada em código (SVG + CSS),
câmera passeando, cada fala movendo uma peça. Peças, árvore, cartas e bichinhos desenhados por nós: só formas e funções,
sem a arte da caixa. Nenhuma imagem de IA. Uso: python3 montar.py
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

# ---------- legenda karaokê: blocos de até 3 palavras, palavra falada em destaque ----------
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

M = {k: ts(*v) if isinstance(v, tuple) else v for k, v in {
    "fofo": (1, "fofo"), "erro": (1, "erro"), "turno1": (1, "turno"), "conto": (1, "conto"),
    "palavra": (2, "palavra"), "par": (2, "par"),
    "vila": (3, "vila"), "n15": (3, "15"), "pontos": (3, "pontos"), "criatura": (3, "criatura"), "construcao": (3, "construcao"),
    "graveto": (3, "graveto"), "cristal": (3, "cristal"), "seixo": (3, "seixo"), "fruto": (3, "fruto"),
    "vez": (4, "vez"), "trabalhador": (4, "trabalhador"), "recurso": (4, "recurso"), "paga": (4, "paga"), "carta4": (4, "carta"), "campina": (4, "campina"),
    "agora": (5, "Agora"), "manual5": (5, "manual"), "construcao5": (5, "construcao"), "tribunal": (5, "tribunal"), "juiza": (5, "juiza"), "graca": (5, "graca"),
    "verde": (6, "verde"), "primavera": (6, "primavera"), "outono6": (6, "outono"), "fazenda": (6, "fazenda"), "tres": (6, "tres"),
    "erro7": (7, "erro"), "volta": (7, "volta"), "trazer": (7, "trazer"), "turno7": (7, "turno"), "estacao7": (7, "estacao"),
    "gente": (8, "gente"), "dois": (8, "dois"), "outono8": (8, "outono"), "seis": (8, "seis"),
    "comeca": (9, "comeca"), "humilde": (9, "humilde"), "quem9": (9, "Quem", 2), "titulo": (9, "titulo"),
    "segue": (10, "segue"), "minuto": (10, "minuto")}.items()}
M["f"] = {i: FI[i]["inicio"] for i in FI}

# ---------- desenho da mesa (coordenadas do "mundo" 1080 x 1920) ----------
COR = {"laranja": "#E98B1E", "azul": "#3b6fb6", "verde": "#5a9a3c", "roxo": "#7a4fa0", "vermelho": "#b8402a", "bronze": "#a07a44", "azulc": "#3f78c0"}
def bicho(cor, w=60):
    return (f'<svg viewBox="0 0 60 72" width="{w}" height="{w * 1.2:.0f}"><g stroke="rgba(0,0,0,.35)" stroke-width="2">'
            f'<ellipse cx="30" cy="50" rx="21" ry="19" fill="{cor}"/><circle cx="17" cy="10" r="7" fill="{cor}"/><circle cx="43" cy="10" r="7" fill="{cor}"/>'
            f'<circle cx="30" cy="25" r="16" fill="{cor}"/></g><circle cx="17" cy="10" r="3" fill="rgba(255,220,200,.6)"/><circle cx="43" cy="10" r="3" fill="rgba(255,220,200,.6)"/>'
            f'<circle cx="24.5" cy="24" r="2.6" fill="#1c140c"/><circle cx="35.5" cy="24" r="2.6" fill="#1c140c"/><ellipse cx="30" cy="30" rx="3.4" ry="2.4" fill="#3a2414"/>'
            f'<ellipse cx="30" cy="54" rx="11" ry="9" fill="rgba(255,255,255,.18)"/></svg>')
REC = {
    "graveto": '<svg viewBox="0 0 60 40" width="{w}"><g stroke="#3a220e" stroke-width="2"><rect x="4" y="15" width="52" height="10" rx="5" fill="#8a5a2e" transform="rotate(-12 30 20)"/><rect x="10" y="8" width="18" height="6" rx="3" fill="#7a4e26" transform="rotate(-40 19 11)"/></g></svg>',
    "cristal": '<svg viewBox="0 0 40 44" width="{w}"><polygon points="20,2 36,16 28,42 12,42 4,16" fill="#f0a531" stroke="#8a5a10" stroke-width="2"/><polygon points="20,2 26,16 20,40 14,16" fill="#ffd27a" opacity=".8"/></svg>',
    "seixo": '<svg viewBox="0 0 50 36" width="{w}"><ellipse cx="25" cy="20" rx="22" ry="14" fill="#9aa0a6" stroke="#4a4e54" stroke-width="2"/><ellipse cx="18" cy="14" rx="8" ry="4" fill="#c8ccd0"/></svg>',
    "fruto": '<svg viewBox="0 0 40 40" width="{w}"><circle cx="20" cy="22" r="16" fill="#7b2e8a" stroke="#3a1040" stroke-width="2"/><circle cx="14" cy="16" r="5" fill="#b678c2"/><path d="M20 6 q6 -6 12 -2" stroke="#3f7a2a" stroke-width="4" fill="none"/></svg>',
}
rec = lambda k, w=44: REC[k].format(w=w)
ICON = {"casa": '<svg viewBox="0 0 40 40" width="46"><path d="M5 20 L20 6 L35 20 V35 H5Z" fill="#fff8e8" stroke="#3a2a1a" stroke-width="2.5"/><rect x="16" y="23" width="8" height="12" fill="#8a5a2e"/></svg>',
        "pata": '<svg viewBox="0 0 40 40" width="46"><ellipse cx="20" cy="26" rx="9" ry="8" fill="#3a2a1a"/><circle cx="10" cy="16" r="4" fill="#3a2a1a"/><circle cx="17" cy="10" r="4" fill="#3a2a1a"/><circle cx="25" cy="10" r="4" fill="#3a2a1a"/><circle cx="31" cy="16" r="4" fill="#3a2a1a"/></svg>'}
def carta(i, nome, tipo, cor, x, y, extra="", cls="", custo="", pts=""):
    ic = ICON["casa" if tipo == "CONSTRUÇÃO" else "pata"]
    return (f'<div class="carta {cls}" id="{i}" style="left:{x}px;top:{y}px"><div class="ct" style="background:{cor}">{nome}</div>'
            f'<div class="cb">{ic}<div class="tp">{tipo}</div></div>{custo}{pts}{extra}</div>')

# a árvore, o rio, os locais, a campina e a vila
LOC = [("graveto", 3, True), ("graveto", 2, False), ("cristal", 2, True), ("cristal", 1, False), ("fruto", 1, True), ("seixo", 1, True), ("fruto", 1, False), ("graveto", 1, False)]
locs = "".join(f'<div class="loc" id="loc{k}" style="left:{70 + k * 120}px"><div class="lr {"fech" if f else "aber"}"></div>'
               f'<div class="li">{rec(r, 30)}<b>{q}</b></div></div>' for k, (r, q, f) in enumerate(LOC))
CAMP = [("Lojista", "CRIATURA", COR["verde"]), ("Sapo Balseiro", "CRIATURA", COR["verde"]), ("Fazenda", "CONSTRUÇÃO", COR["verde"]), ("Masmorra", "CONSTRUÇÃO", COR["vermelho"]),
        ("Andarilha", "CRIATURA", COR["bronze"]), ("Estalajadeiro", "CRIATURA", COR["azulc"]), ("Marido", "CRIATURA", COR["verde"]), ("Esposa", "CRIATURA", COR["roxo"])]
CX = lambda k: 95 + (k % 4) * 228; CY = lambda k: 905 + (k // 4) * 215
camp = "".join(carta(f"m{k}", n, t, c, CX(k), CY(k)) for k, (n, t, c) in enumerate(CAMP))
VX = lambda k: 75 + (k % 5) * 190; VY = lambda k: 1430 + (k // 5) * 160
vaga = "".join(f'<div class="vaga" id="s{k}" style="left:{VX(k)}px;top:{VY(k)}px">{k + 1}</div>' for k in range(15))
frutos3 = "".join(rec("fruto", 26) for _ in range(3))
CUSTO_TRIB = '<div class="custo">' + rec("graveto", 24) + rec("cristal", 18) + rec("seixo", 22) + rec("seixo", 22) + '</div>'
CUSTO_JUIZA = f'<div class="custo" id="cj">{frutos3}<i class="risco" id="risco"></i></div><div class="gratis" id="gratis">GRÁTIS</div>'
# cartas extras (fora da campina): Tribunal e Juíza (manual p. 10) e a reposição da campina
extras = (carta("trib", "Tribunal", "CONSTRUÇÃO", COR["azulc"], VX(1), VY(1), cls="vil", custo=CUSTO_TRIB, extra='<div class="ocup" id="ocup">OCUPADO</div>')
          + carta("juiza", "Juíza", "CRIATURA", COR["azulc"], 1120, VY(2), cls="vil", custo=CUSTO_JUIZA, extra='<div class="par-tag" id="partag">TRIBUNAL</div>')
          + carta("repo", "Mineira", "CRIATURA", COR["verde"], 470, 300, cls="", extra=""))

ARV = """<svg id="arvore" viewBox="0 0 700 560" width="700" height="560" style="left:190px;top:40px">
<defs><radialGradient id="cop" cx=".45" cy=".35" r=".7"><stop offset="0" stop-color="#8cc260"/><stop offset=".6" stop-color="#4f8a35"/><stop offset="1" stop-color="#2f5a22"/></radialGradient>
<linearGradient id="tro" x1="0" x2="1"><stop offset="0" stop-color="#5a3a1e"/><stop offset=".5" stop-color="#8a5a30"/><stop offset="1" stop-color="#4a2e16"/></linearGradient></defs>
<g id="copa">
<circle cx="350" cy="170" r="150" fill="url(#cop)"/><circle cx="210" cy="210" r="110" fill="url(#cop)"/><circle cx="490" cy="210" r="110" fill="url(#cop)"/>
<circle cx="270" cy="110" r="90" fill="url(#cop)"/><circle cx="430" cy="110" r="90" fill="url(#cop)"/>
<g fill="#e8a33a" opacity=".9"><circle cx="250" cy="150" r="9"/><circle cx="420" cy="90" r="8"/><circle cx="500" cy="230" r="9"/><circle cx="330" cy="240" r="7"/><circle cx="180" cy="230" r="8"/></g></g>
<path d="M300 560 C310 470 300 380 320 300 L380 300 C400 380 390 470 400 560 Z" fill="url(#tro)" stroke="#2e1c0c" stroke-width="3"/>
<path d="M320 330 C260 320 200 300 150 300" stroke="#6a4424" stroke-width="22" fill="none" stroke-linecap="round"/>
<path d="M380 330 C440 320 500 300 550 300" stroke="#6a4424" stroke-width="22" fill="none" stroke-linecap="round"/>
<path d="M330 410 C280 405 240 395 200 400" stroke="#6a4424" stroke-width="18" fill="none" stroke-linecap="round"/>
<path d="M370 410 C420 405 460 395 500 400" stroke="#6a4424" stroke-width="18" fill="none" stroke-linecap="round"/>
<rect x="322" y="440" width="56" height="80" rx="8" fill="#2e1c0c"/><rect x="328" y="450" width="44" height="64" rx="4" fill="#c8b48a" stroke="#6a4a2a" stroke-width="2"/>
</svg>"""
GALHOS = [("PRIMAVERA", "+1", 150, 230), ("VERÃO", "+1", 330, 205), ("OUTONO", "+2", 520, 230)]
galhos = "".join(f'<div class="esc" style="left:{190 + x - 60}px;top:{40 + y}px">{n}<b>{v}</b></div>' for n, v, x, y in GALHOS)
# trabalhadores: 2 no começo (na reserva do jogador) e 4 na árvore (1, 1, 2)
TR0 = [(160, 1345), (240, 1345)]
TRV = [(190 + 150 - 25, 40 + 270), (190 + 330 - 25, 40 + 245), (190 + 520 - 55, 40 + 270), (190 + 520 + 5, 40 + 270)]
trab = "".join(f'<div class="tr" id="t{k}" style="left:{x}px;top:{y}px">{bicho(COR["laranja"])}</div>' for k, (x, y) in enumerate(TR0 + TRV))
trab += f'<div class="tr" id="tazul" style="left:930px;top:640px">{bicho(COR["azul"])}</div>'
PILHAS = [("graveto", 170), ("cristal", 410), ("seixo", 650), ("fruto", 890)]
pilhas = "".join(f'<div class="pilha" id="p{k}" style="left:{x - 60}px">' + "".join(rec(r, 46) for _ in range(3)) + f'<span>{r}</span></div>' for k, (r, x) in enumerate(PILHAS))
voadores = "".join(f'<div class="voa" id="g{k}">{rec("graveto", 54)}</div>' for k in range(3)) + "".join(f'<div class="voa" id="b{k}">{rec("fruto", 46)}</div>' for k in range(3))

MUNDO = f"""<div id="world">
<div id="mesa"></div><div id="tab"></div><div id="rio"><svg viewBox="0 0 1000 90" preserveAspectRatio="none"><path id="onda" d="M0 30 Q125 10 250 30 T500 30 T750 30 T1000 30 V90 H0Z" fill="#4f8fb8"/><path d="M0 45 Q125 30 250 45 T500 45 T750 45 T1000 45" stroke="#a8d4ee" stroke-width="4" fill="none" opacity=".7"/></svg></div>
{ARV}{galhos}{pilhas}<div id="locs">{locs}</div><div class="rot" style="left:70px;top:700px">LOCAIS · ○ ABERTO  ● FECHADO</div>
<div class="rot" style="left:95px;top:875px">CAMPINA</div>{camp}
<div id="reserva"><span>SUA RESERVA</span></div><div class="rot" style="left:75px;top:1400px">SUA VILA · 15 ESPAÇOS</div>{vaga}
{extras}{trab}{voadores}
<div id="relogio"><svg viewBox="0 0 120 120" width="150"><circle cx="60" cy="60" r="54" fill="#fff8e8" stroke="#3a2a1a" stroke-width="6"/><path id="fatia" d="M60 60 L60 10 A50 50 0 1 1 59.9 10 Z" fill="#b8402a"/><circle cx="60" cy="60" r="6" fill="#3a2a1a"/></svg><b>1 TURNO</b></div>
<div id="coroa"><svg viewBox="0 0 90 50" width="110"><path d="M5 45 L12 10 L28 30 L45 4 L62 30 L78 10 L85 45 Z" fill="#7fb04a" stroke="#2f5a22" stroke-width="3"/><circle cx="45" cy="4" r="5" fill="#e8a33a"/></svg></div>
</div>"""

CSS = f"""
@font-face{{font-family:'Inter';src:url(assets/fonts/inter-latin-900-normal.woff2) format('woff2');font-weight:900}}
@font-face{{font-family:'Newsreader';src:url(assets/fonts/newsreader-latin-600-italic.woff2) format('woff2');font-weight:600;font-style:italic}}
@font-face{{font-family:'IBM Plex Mono';src:url(assets/fonts/ibm-plex-mono-latin-500-normal.woff2) format('woff2');font-weight:500}}
*{{box-sizing:border-box;margin:0}} html,body{{width:1080px;height:1920px;overflow:hidden;background:#2a1a0e}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#2a1a0e}}
#cam{{position:absolute;inset:0}}
#world{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0}}
#world > *{{position:absolute}}
#mesa{{left:-1200px;top:-1200px;width:3480px;height:4320px;background:
 repeating-linear-gradient(90deg,rgba(0,0,0,.05) 0 3px,transparent 3px 40px),
 repeating-linear-gradient(90deg,rgba(255,220,170,.04) 0 1px,transparent 1px 17px),
 linear-gradient(180deg,#7a5232,#5e3d22 40%,#6b4529)}}
#tab{{left:40px;top:20px;width:1000px;height:1350px;border-radius:26px;background:radial-gradient(ellipse at 50% 30%,#8fb862,#6a9444 55%,#557a36);box-shadow:0 30px 60px rgba(0,0,0,.45),inset 0 0 0 10px #c9a66b,inset 0 0 0 14px #8a6a3a}}
#rio{{left:40px;top:590px;width:1000px;height:90px}} #rio svg{{width:100%;height:100%}}
#arvore{{filter:drop-shadow(0 18px 20px rgba(0,0,0,.35))}}
.esc{{width:120px;text-align:center;font:900 18px 'Inter';color:#fff8e8;background:#7a4a1e;border:3px solid #e8c27a;border-radius:8px;padding:4px 0;letter-spacing:.04em}}
.esc b{{display:block;font-size:22px;color:#ffd27a}}
.pilha{{top:600px;width:130px;height:70px;display:flex;align-items:flex-end;justify-content:center;gap:0}} .pilha svg{{margin:0 -8px;filter:drop-shadow(0 4px 3px rgba(0,0,0,.35))}}
.pilha span{{position:absolute;left:0;right:0;bottom:-26px;text-align:center;font:900 17px 'Inter';color:#fff8e8;text-shadow:0 2px 4px rgba(0,0,0,.6);opacity:0;text-transform:uppercase}}
#locs{{left:0;top:725px;width:1080px;height:110px}}
.loc{{position:absolute;top:0;width:104px;height:100px;background:#f4ead2;border-radius:12px;border:3px solid #8a6a3a;box-shadow:0 6px 10px rgba(0,0,0,.3)}}
.lr{{position:absolute;left:8px;top:8px;width:30px;height:30px;border-radius:50%;border:5px solid #3a2a1a}} .lr.fech{{background:#3a2a1a}} .lr.aber{{border-style:dashed}}
.li{{position:absolute;left:0;right:0;bottom:8px;display:flex;justify-content:center;align-items:center;gap:6px}} .li b{{font:900 34px 'Inter';color:#3a2a1a}}
.rot{{font:900 20px 'Inter';color:rgba(255,248,232,.9);letter-spacing:.12em;text-shadow:0 2px 4px rgba(0,0,0,.4)}}
.carta{{width:200px;height:200px;background:#f4ead2;border-radius:14px;border:3px solid #6a4a2a;box-shadow:0 8px 14px rgba(0,0,0,.35);overflow:hidden}}
.carta .ct{{height:52px;display:flex;align-items:center;justify-content:center;text-align:center;font:900 21px/1.05 'Inter';color:#fff;padding:0 8px;text-shadow:0 2px 3px rgba(0,0,0,.35)}}
.carta .cb{{display:flex;flex-direction:column;align-items:center;padding-top:16px}} .carta .tp{{font:900 15px 'Inter';color:#6a4a2a;letter-spacing:.08em;margin-top:8px}}
.carta.vil{{width:170px;height:150px}} .carta.vil .ct{{height:44px;font-size:19px}} .carta.vil .cb{{padding-top:6px}} .carta.vil .cb svg{{width:36px}}
.custo{{position:absolute;left:6px;bottom:6px;display:flex;gap:1px;align-items:center}}
.risco{{position:absolute;left:-4px;right:-4px;top:50%;height:6px;background:#c0281a;transform-origin:0 50%;transform:scaleX(0)}}
.gratis{{position:absolute;right:6px;bottom:8px;font:900 22px 'Inter';color:#fff;background:#3aa35a;padding:3px 8px;border-radius:6px;opacity:0}}
.ocup{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-12deg);font:900 20px 'Inter';color:#fff;background:#3a2a1a;border:3px solid #ffd27a;padding:4px 10px;border-radius:8px;opacity:0}}
.par-tag{{position:absolute;left:6px;top:58px;font:900 12px 'Inter';color:#3f78c0;opacity:0}}
.vaga{{width:170px;height:150px;border-radius:14px;border:4px dashed rgba(255,248,232,.55);background:rgba(0,0,0,.12);display:flex;align-items:center;justify-content:center;font:900 40px 'Inter';color:rgba(255,248,232,.45)}}
#reserva{{left:60px;top:1336px;width:960px;height:60px}} #reserva span{{position:absolute;right:0;top:18px;font:900 18px 'Inter';color:rgba(255,248,232,.75);letter-spacing:.12em}}
.tr{{width:60px;height:72px;filter:drop-shadow(0 6px 4px rgba(0,0,0,.4));transform-origin:50% 100%}}
.voa{{left:0;top:0;opacity:0;filter:drop-shadow(0 6px 5px rgba(0,0,0,.4))}}
#relogio{{left:480px;top:1180px;width:150px;opacity:0;text-align:center}} #relogio b{{display:block;font:900 26px 'Inter';color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.7)}}
#coroa{{left:0;top:0;opacity:0}}
/* camadas da tela (fora da câmera) */
#topo{{position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(180deg,rgba(20,12,6,.72),rgba(20,12,6,.35) 60%,rgba(20,12,6,0));pointer-events:none}}
#base{{position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(0deg,rgba(20,12,6,.75),rgba(20,12,6,0));pointer-events:none}}
#marca{{position:absolute;left:48px;top:150px;font:500 26px 'IBM Plex Mono';color:rgba(255,248,232,.8)}}
#capa{{position:absolute;left:0;right:0;top:250px;text-align:center}}
#capa-tag{{display:inline-block;background:{COR['laranja']};color:#111;font:900 40px 'Inter';letter-spacing:.06em;padding:10px 24px}}
#capa-t{{font:900 190px/1 'Inter';color:#fff;-webkit-text-stroke:8px #1c1008;paint-order:stroke fill;margin-top:22px;text-shadow:0 12px 30px rgba(0,0,0,.6)}}
#capa-sub{{font:italic 600 58px 'Newsreader';color:#fff2d8;margin-top:14px;text-shadow:0 3px 14px rgba(0,0,0,.9)}}
#caps{{position:absolute;left:60px;right:60px;top:330px;height:200px}}
.cap{{position:absolute;left:0;right:0;top:0;text-align:center;opacity:0;font:900 78px/1.15 'Inter';color:#fff;-webkit-text-stroke:6px #1c1008;paint-order:stroke fill}}
.cap span{{display:inline-block;padding:2px 14px;border-radius:12px;margin:0 2px;background:rgba(233,139,30,0)}}
.cap span.on{{background:{COR['laranja']};color:#111;-webkit-text-stroke:0}}
.big{{position:absolute;left:0;right:0;text-align:center;font:900 220px/1 'Inter';color:#fff;-webkit-text-stroke:9px #1c1008;paint-order:stroke fill;opacity:0}}
.pop{{position:absolute;font:900 64px 'Inter';color:#fff;-webkit-text-stroke:6px #1c1008;paint-order:stroke fill;opacity:0}}
.selo{{position:absolute;font:900 40px 'Inter';color:#fff;background:#3a2a1a;border:5px solid #ffd27a;border-radius:12px;padding:8px 20px;opacity:0}}
.fonte{{position:absolute;left:48px;right:48px;bottom:56px;text-align:center;font:500 26px 'IBM Plex Mono';color:rgba(255,248,232,.85);opacity:0}}
#escuro{{position:absolute;inset:0;background:rgba(15,9,4,.72);opacity:0}}
#parA,#parB{{position:absolute;top:960px;opacity:0}} #parA .carta,#parB .carta{{transform:scale(1.5);transform-origin:50% 50%}}
#fim{{position:absolute;left:0;right:0;bottom:120px;text-align:center;opacity:0}}
#fim img{{width:420px}} #fim div{{font:500 30px 'IBM Plex Mono';color:#fff8e8;margin-top:16px}}
"""

# cartas grandes do "PAR" (camada de tela)
PAR_A = carta("pa", "Juíza", "CRIATURA", COR["azulc"], 0, 0).replace('class="carta "', 'class="carta" style="transform:scale(1.6)"')
PAR_B = carta("pb", "Tribunal", "CONSTRUÇÃO", COR["azulc"], 0, 0)
TELA = f"""<div id="topo"></div><div id="base"></div><div id="marca">@eliteboardgamers</div>
<div id="escuro"></div>
<div id="parA" style="left:170px">{carta("pa", "Juíza", "CRIATURA", COR["azulc"], 0, 0)}</div>
<div id="parB" style="left:710px">{carta("pb", "Tribunal", "CONSTRUÇÃO", COR["azulc"], 0, 0)}</div>
<div class="big" id="bpar" style="top:560px">PAR</div>
<div class="big" id="b15" style="top:640px;font-size:260px">15</div>
<div class="big" id="b3x" style="top:640px">3×</div>
<div class="big bs" id="n2" style="top:600px;font-size:200px">2</div><div class="big bs" id="n3" style="top:600px;font-size:200px">3</div><div class="big bs" id="n4" style="top:600px;font-size:200px">4</div><div class="big bs" id="n6" style="top:600px;font-size:200px">6</div>
<div class="pop" id="pp3" style="left:610px;top:760px">+3</div>
<div class="pop" id="ppf" style="left:210px;top:860px">+1</div>
<div class="selo" id="selo-erro" style="left:300px;top:640px;background:#b8402a;font-size:56px">ERRO</div>
<div class="selo" id="se0" style="left:470px;top:900px">AO JOGAR</div><div class="selo" id="se1" style="left:470px;top:900px">PRIMAVERA</div><div class="selo" id="se2" style="left:470px;top:900px">OUTONO</div>
<div class="fonte" id="f-man">Regras: manual Galápagos (EVE001), p. 10</div><div class="fonte" id="f-man2">Manual Galápagos, p. 6: “a pessoa mais humilde da mesa”</div>
<div id="capa"><div id="capa-tag">EVERDELL EM 1 MINUTO</div><div id="capa-t">JOGO<br>FOFO?</div><div id="capa-sub">o erro que te custa um turno</div></div>
<div id="caps">{''.join(f'<div class="cap" id="c{i}">' + ''.join(f'<span id="c{i}w{j}">{t}</span>' for j, (t, _) in enumerate(l["w"])) + '</div>' for i, l in enumerate(LEG))}</div>
<div id="fim"><img src="assets/img/logo-eb-156.png"><div>guia completo: eliteboardgamers.com.br/como-jogar</div></div>"""

JS = """
const tl = gsap.timeline({ paused: true });
const W = '#world';
// câmera: põe o ponto (x, y) do mundo no ponto (sx, sy) da tela, com zoom s
function cam(t, x, y, s, d = .9, sy = 1150, ease = 'power2.inOut') { tl.to(W, { x: 540 - x * s, y: sy - y * s, scale: s, duration: d, ease }, t); }
tl.set(W, { x: 540 - 540 * 1.05, y: 1150 - 900 * 1.05, scale: 1.05 }, 0);
// vida contínua: copa balança, rio corre, bichinhos respiram
tl.to('#copa', { rotation: 1.2, transformOrigin: '350px 400px', duration: 2.2, yoyo: true, repeat: Math.ceil(TOTAL / 2.2), ease: 'sine.inOut' }, 0);
tl.to('#onda', { x: -250, duration: 4, repeat: Math.ceil(TOTAL / 4), ease: 'none' }, 0);
document.querySelectorAll('.tr').forEach((el, i) => tl.to(el, { scaleY: 1.05, duration: .6 + (i % 3) * .1, yoyo: true, repeat: Math.ceil(TOTAL / .6), ease: 'sine.inOut' }, 0));
// 1 · capa já pronta no quadro 0; a câmera avança; "fofo": os bichinhos pulam; "erro": um cai deitado e o relógio esvazia
cam(0, 540, 640, 1.18, 2.6, 1150, 'power1.out');
tl.to('#capa', { opacity: 0, y: -40, duration: .35, ease: 'power2.in' }, CAPA_FIM - .35);
tl.to(['#t2', '#t3', '#t4', '#t5'], { y: -40, duration: .18, yoyo: true, repeat: 1, stagger: .08, ease: 'power2.out' }, M.fofo);
cam(M.erro - .5, 540, 1300, 1.0, .7);
tl.to('#t0', { rotation: -90, y: 20, duration: .3, ease: 'bounce.out' }, M.erro);
tl.fromTo('#relogio', { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .25, ease: 'back.out(2)' }, M.erro - .05);
tl.fromTo('#fatia', { scale: 1, transformOrigin: '60px 60px' }, { scale: 0, duration: .9, ease: 'power2.in' }, M.turno1 - .2);
tl.fromTo('#selo-erro', { opacity: 0, scale: 1.8, rotation: -8 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in' }, M.erro);
tl.to(['#selo-erro', '#relogio'], { opacity: 0, duration: .3 }, M.conto + .3);
tl.to('#t0', { rotation: 0, y: 0, duration: .3 }, M.conto + .3);
// 2 · PAR: a mesa escurece, criatura e construção se encaixam
tl.to('#escuro', { opacity: 1, duration: .35 }, M.f[2] - .1);
tl.fromTo('#parA', { opacity: 0, x: -300, rotation: -12 }, { opacity: 1, x: 0, rotation: -4, duration: .5, ease: 'power3.out' }, M.palavra - .5);
tl.fromTo('#parB', { opacity: 0, x: 300, rotation: 12 }, { opacity: 1, x: 0, rotation: 4, duration: .5, ease: 'power3.out' }, M.palavra - .4);
tl.to('#parA', { x: 175, rotation: 0, duration: .25, ease: 'power4.in' }, M.par - .05);
tl.to('#parB', { x: -175, rotation: 0, duration: .25, ease: 'power4.in' }, M.par - .05);
tl.fromTo('#bpar', { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: .22, ease: 'power4.in' }, M.par);
tl.to(['#parA', '#parB', '#bpar', '#escuro'], { opacity: 0, duration: .3 }, M.f[3] - .15);
// 3 · a vila: 15 espaços acendem; "pontos"; os quatro recursos saltam
cam(M.f[3] - .2, 540, 1590, 1.08, .8);
tl.fromTo('.vaga', { borderColor: 'rgba(255,248,232,.55)' }, { borderColor: '#ffd27a', background: 'rgba(255,210,122,.18)', duration: .12, stagger: .05 }, M.vila);
tl.fromTo('#b15', { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .3, ease: 'back.out(2)' }, M.n15 - .05);
tl.to('#b15', { opacity: 0, duration: .25 }, M.pontos + .2);
cam(M.criatura - .6, 540, 1000, 1.3, .7);
tl.to('#m0', { y: -24, scale: 1.08, duration: .25, yoyo: true, repeat: 1 }, M.criatura);
tl.to('#m2', { y: -24, scale: 1.08, duration: .25, yoyo: true, repeat: 1 }, M.construcao);
cam(M.graveto - .7, 530, 640, 1.75, .7);
[['graveto', 0], ['cristal', 1], ['seixo', 2], ['fruto', 3]].forEach(([k, i]) => {
  tl.to('#p' + i, { y: -36, scale: 1.25, duration: .18, yoyo: true, repeat: 1, ease: 'power2.out' }, M[k] - .05);
  tl.fromTo('#p' + i + ' span', { opacity: 0 }, { opacity: 1, duration: .15 }, M[k] - .05); });
// 4 · o turno: um trabalhador vai ao local de 3 gravetos; +3; depois joga a Fazenda da campina e paga
cam(M.vez - .3, 400, 1050, 1.0, .8);
tl.to('#t1', { keyframes: [{ x: -70, y: -700, duration: .3, ease: 'power2.out' }, { x: -138, y: -595, duration: .28, ease: 'power2.in' }] }, M.trabalhador - .1);
tl.fromTo('#pp3', { opacity: 0, y: 20 }, { opacity: 1, y: -20, duration: .3 }, M.recurso);
tl.to('#pp3', { opacity: 0, duration: .25 }, M.recurso + .8);
[0, 1, 2].forEach(i => { tl.set('#g' + i, { x: 120, y: 760, opacity: 1 }, M.recurso);
  tl.to('#g' + i, { x: 120 + i * 60, y: 1340, duration: .55, ease: 'power2.in' }, M.recurso + i * .08);
  tl.to('#g' + i, { x: 170, y: 640, duration: .5, ease: 'power2.inOut' }, M.paga + i * .06);
  tl.to('#g' + i, { opacity: 0, duration: .1 }, M.paga + .55 + i * .06); });
tl.to('#m2', { x: VX0 - CX2, y: VY0 - CY2, scaleX: .85, scaleY: .75, transformOrigin: '0 0', duration: .7, ease: 'power3.inOut', zIndex: 5 }, M.carta4 - .1);
tl.fromTo('#repo', { x: 0, y: 0, opacity: 0 }, { x: CX2 - 470, y: CY2 - 300, opacity: 1, duration: .6, ease: 'power2.out' }, M.campina);
// 5 · o par: Tribunal na vila, a Juíza encosta, "3 frutos" riscado vira GRÁTIS, ficha de Ocupado
cam(M.agora - .2, 450, 1520, 1.35, .8);
tl.fromTo('#trib', { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: .3, ease: 'back.out(2)' }, M.agora);
tl.to('#f-man', { opacity: 1, duration: .3 }, M.manual5);
tl.to('#f-man', { opacity: 0, duration: .3 }, M.f[6] - .2);
tl.fromTo('#juiza', { x: 0 }, { x: VX2 - 1120, duration: .7, ease: 'power3.out' }, M.tribunal - .2);
tl.to('#partag', { opacity: 1, duration: .2 }, M.tribunal + .3);
tl.to('#risco', { scaleX: 1, duration: .25 }, M.juiza + .1);
tl.fromTo('#gratis', { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in' }, M.graca - .1);
tl.fromTo('#ocup', { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: .3, ease: 'bounce.out' }, M.graca + .2);
// 6 · a Fazenda (carta verde) produz três vezes: ao jogar, na primavera e no outono
cam(M.verde - .3, 300, 1480, 1.45, .8);
const est = [['AO JOGAR', M.verde + .1], ['PRIMAVERA', M.primavera], ['OUTONO', M.outono6]];
est.forEach(([n, t], i) => { if (i) tl.to('#se' + (i - 1), { opacity: 0, duration: .1 }, t);
  tl.fromTo('#se' + i, { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: .18, immediateRender: false }, t);
  tl.fromTo('#m2', { boxShadow: '0 0 0 0px rgba(140,220,90,0)' }, { boxShadow: '0 0 0 18px rgba(140,220,90,.85)', duration: .2, yoyo: true, repeat: 1, immediateRender: false }, t);
  tl.fromTo('#ppf', { opacity: 0, y: 30 }, { opacity: 1, y: -10, duration: .25, immediateRender: false }, t + .05);
  tl.to('#ppf', { opacity: 0, duration: .2 }, t + .55); });
tl.to('#se2', { opacity: 0, duration: .2 }, M.fazenda - .2);
tl.fromTo('#b3x', { opacity: 0, scale: .6 }, { opacity: 1, scale: 1, duration: .25, ease: 'back.out(2)' }, M.tres - .05);
tl.to('#b3x', { opacity: 0, duration: .25 }, M.f[7] - .15);
[0, 1, 2].forEach(i => { tl.set('#b' + i, { x: 890, y: 640, opacity: 1 }, M.fazenda + .2 + i * .35);
  tl.to('#b' + i, { x: 200 + i * 40, y: 1340, duration: .55, ease: 'power2.in' }, M.fazenda + .2 + i * .35); });
// 7 · o erro: trabalhadores presos nos locais; o relógio esvazia; voltam todos juntos
cam(M.f[7] - .2, 540, 1000, .95, .8);
tl.to('#t0', { x: 70 + 2 * 120 + 22 - 160, y: 750 - 1345, duration: .5, ease: 'power2.inOut' }, M.f[7]);
tl.fromTo('#selo-erro', { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: .2, ease: 'power4.in', immediateRender: false }, M.erro7);
tl.to('#selo-erro', { opacity: 0, duration: .2 }, M.erro7 + 1.0);
tl.to(['#t0', '#t1'], { rotation: 8, duration: .08, yoyo: true, repeat: 7 }, M.volta - .1);
tl.fromTo('#relogio', { opacity: 0, scale: .4 }, { opacity: 1, scale: 1, duration: .25, ease: 'back.out(2)', immediateRender: false }, M.trazer - .2);
tl.fromTo('#fatia', { scale: 1 }, { scale: 0, duration: 1.0, ease: 'power2.in', immediateRender: false }, M.turno7 - .3);
tl.to(['#t0', '#t1'], { x: 0, y: 0, duration: .6, ease: 'power2.inOut', stagger: .08 }, M.turno7 + .6);
tl.to('#relogio', { opacity: 0, duration: .3 }, M.estacao7 + .2);
// 8 · cada estação traz gente nova: 2 → 3 → 4 → 6
cam(M.f[8] - .2, 540, 650, 1.0, .8, 1180);
tl.fromTo('#n2', { opacity: 0 }, { opacity: 1, duration: .25 }, M.dois - .1);
const pass = [[3, M.dois + .6, ['#t2']], [4, M.dois + 1.1, ['#t3']], [6, M.seis - .05, ['#t4', '#t5']]];
const prev = { 3: '#n2', 4: '#n3', 6: '#n4' };
pass.forEach(([n, t, ids], i) => { tl.set(prev[n], { opacity: 0 }, t);
  tl.fromTo('#n' + n, { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: .2, immediateRender: false }, t);
  ids.forEach((id, j) => tl.to(id, { x: 320 + (i * 2 + j) * 80 - parseFloat(document.querySelector(id).style.left), y: 1345 - parseFloat(document.querySelector(id).style.top), duration: .55, ease: 'bounce.out' }, t)); });
cam(M.outono8 - .4, 540, 1100, .82, .9, 1250);
tl.to('#n6', { opacity: 0, duration: .3 }, M.f[9] - .2);
// 9 · quem começa: a pessoa mais humilde (manual, p. 6); a coroa cai sobre um bichinho
cam(M.f[9] - .1, 200, 1360, 1.6, .9);
tl.set('#coroa', { x: 150, y: 1100 }, M.humilde - .4);
tl.to('#coroa', { opacity: 1, y: 1300, duration: .5, ease: 'bounce.out' }, M.humilde - .4);
tl.to('#f-man2', { opacity: 1, duration: .3 }, M.humilde - .3);
tl.to('#f-man2', { opacity: 0, duration: .3 }, M.f[10] - .2);
['#t0', '#t1', '#t2', '#t3'].forEach((id, k) => tl.to(id + ' svg', { y: -34, duration: .16, yoyo: true, repeat: 1 }, M.quem9 + k * .07));
// 10 · a mesa inteira e o fecho
cam(M.f[10] - .2, 540, 960, .66, 1.4, 1060, 'power2.out');
tl.fromTo('#fim', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .5 }, M.segue);
// legenda karaokê no terço de cima
LEG.forEach((b, i) => { tl.set('#c' + i, { opacity: 1 }, b.ini); tl.set('#c' + i, { opacity: 0 }, b.fim);
  b.w.forEach(([t, s], j) => { tl.set('#c' + i + 'w' + j, { backgroundColor: '#E98B1E' }, Math.max(s, b.ini)); if (j + 1 < b.w.length) tl.set('#c' + i + 'w' + j, { backgroundColor: 'rgba(233,139,30,0)' }, Math.max(b.w[j + 1][1], b.ini)); }); });
tl.to({}, { duration: TOTAL }, 0);
window.__timelines = window.__timelines || {}; window.__timelines['video'] = tl;
"""
CONST = (f"const TOTAL={TOTAL}, CAPA_FIM={CAPA_FIM}, M={json.dumps(M)}, LEG={json.dumps(LEG, ensure_ascii=False)}, "
         f"VX0={VX(0)}, VY0={VY(0)}, CX2={CX(2)}, CY2={CY(2)}, VX2={VX(2)};")
SFX = [("pop", M["fofo"], .4), ("tombo", M["erro"], .55), ("cartas", M["par"] - .05, .5), ("pop", M["graveto"], .3), ("pop", M["cristal"], .3), ("pop", M["seixo"], .3), ("pop", M["fruto"], .3),
       ("pulo", M["trabalhador"], .45), ("madeira", M["recurso"] + .4, .4), ("cartas", M["carta4"], .45), ("carimbo", M["graca"] - .1, .5), ("brilho", M["verde"] + .1, .4), ("brilho", M["primavera"], .4),
       ("brilho", M["outono6"], .4), ("tombo", M["erro7"], .5), ("relogio", M["turno7"] - .3, .45), ("pulo", M["turno7"] + .6, .4), ("pulo", M["dois"] + .6, .35), ("pulo", M["seis"], .4), ("folhas", M["humilde"] - .4, .5), ("brilho", M["segue"], .35)]
sfx = "\n".join(f'<audio id="sx{n}" class="clip" data-start="{s:.3f}" data-duration="0.6" data-track-index="{40 + n}" data-volume="{v}" src="assets/audio/sfx/{f}.mp3"></audio>' for n, (f, s, v) in enumerate(SFX))

HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Como se joga Everdell?</title>
<script src="assets/lib/gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="video" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
<div id="cam" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="1">{MUNDO}</div>
<div id="tela" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="2" style="position:absolute;inset:0">{TELA}</div>
<audio id="voz" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-volume="1" src="assets/audio/narracao.wav"></audio>
<audio id="trilha" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="4" data-volume="1" data-fade-in="0.2" data-fade-out="1.5" src="assets/audio/trilha_mix.wav"></audio>
{sfx}
</div>
<script>{CONST}{JS}</script></body></html>"""
(P / "index.html").write_text(HTML, encoding="utf-8"); (P / "hyperframes.json").write_text('{ "name": "elite-como-se-joga-everdell" }\n')
print("ok", TOTAL, len(LEG), "blocos de legenda")
