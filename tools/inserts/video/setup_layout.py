"""Onde cada peça fica na mesa no setup (manual oficial, p. 4-5). Tabuleiro 720 x 520 mm em x 0..720, y 0..520.
Espaços do tabuleiro medidos na ilustração do manual (endireitada pelos 4 cantos do tabuleiro, ±10 mm)."""
import json, numpy as np
d = json.load(open('cena.json'))
grp, ordem = {}, []
for o in d['objs']:
    base = o['nome'].split(':')[0]
    if base.endswith('-tampa'): base = base[:-6]
    v = np.array(o['v']).reshape(-1, 3)
    if base not in grp: grp[base] = [v.min(0), v.max(0)]; ordem.append(base)
    else: grp[base][0] = np.minimum(grp[base][0], v.min(0)); grp[base][1] = np.maximum(grp[base][1], v.max(0))
alvo = {}
def tam(n, rot=0):
    t = grp[n][1] - grp[n][0]
    return (t[1], t[0]) if rot % 180 else (t[0], t[1])
def put(n, cx, cy, rot=0):
    c = (grp[n][0] + grp[n][1]) / 2
    alvo[n] = dict(c=[float(c[0]), float(c[1]), float(grp[n][0][2])], fim=[cx, cy, 2.0], rot=rot)
def fila(nomes, x, y, rot=0, gap=14, para='x'):
    for n in nomes:
        w, h = tam(n, rot)
        if para == 'x': put(n, x + w / 2, y - h / 2, rot); x += w + gap
        else: put(n, x + w / 2, y - h / 2, rot); y -= h + gap
# Regra: só vai para a mesa o que se usa na partida; caixas de guarda, enchimentos, miniaturas e expansões ficam na caixa.
# --- em cima do tabuleiro ---
put('cartas-eventos', 112, 446, 90)                     # espaço do baralho de Eventos (canto sup. esq.)
for n, cx in (('cartas-aventura-construir', 292), ('cartas-aventura-coletar', 394), ('cartas-aventura-explorar', 484)):
    put(n, cx, 66, -90)                                  # espaços de ação, dados para baixo
# --- logo abaixo do tabuleiro: só os descartes de cada ação ---
for n, cx in (('descarte-construir', 292), ('descarte-coletar', 394), ('descarte-explorar', 484)):
    put(n, cx, -58, -90)
# --- à esquerda (como no manual): ficha de cenário, Mistério, Feras/Invenções, peças de ilha ---
put('FICHAS DE CENÁRIO', -125, 372)
fila(['cartas-misterio', 'descarte-misterio'], -250, 205, rot=90)
fila(['descarte-eventos'], -250, 95, rot=90)
put('cartas-pequenas-retrato', -60, 60)
put('ORIGINAL obj_12_map-tiles-animals-misc-expansions.stl', -110, -140, 90)
# --- à direita: recursos, fichas e dados (o que todo mundo pega durante a partida) ---
fila(['ORIGINAL obj_14_resources.stl', 'ORIGINAL obj_16_tokens.stl'], 740, 520, gap=10)
fila(['ORIGINAL obj_15_dice-determination-black-white-blue.stl', 'ORIGINAL obj_13_shelter-upgrades-herb-garden-pen-spyglass.stl'],
     740, 260, rot=90, gap=10, para='y')
put('caixa-a2', 590, -70, 90)
put('caixa-b1', 660, -110)
fica = [b for b in ordem if b not in alvo and b != 'TABULEIRO']
fica_set = fica
print('ficam na caixa:', fica)
json.dump(dict(alvo=alvo, caixa=[-900, 700], fica=fica), open('setup.json', 'w'))
