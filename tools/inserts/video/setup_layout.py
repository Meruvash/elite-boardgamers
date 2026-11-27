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
# --- em cima do tabuleiro ---
put('cartas-eventos', 112, 446, 90)                     # espaço do baralho de Eventos (canto sup. esq.)
for n, cx in (('cartas-aventura-construir', 292), ('cartas-aventura-coletar', 394), ('cartas-aventura-explorar', 484)):
    put(n, cx, 66, -90)                                  # espaços de ação na faixa de baixo, dados para baixo
# --- abaixo do tabuleiro: descartes de cada ação logo abaixo do seu monte, depois o monte de componentes ---
for n, cx in (('descarte-construir', 292), ('descarte-coletar', 394), ('descarte-explorar', 484)):
    put(n, cx, -60, -90)
fila(['ORIGINAL obj_14_resources.stl', 'ORIGINAL obj_16_tokens.stl', 'ORIGINAL obj_15_dice-determination-black-white-blue.stl',
      'caixa-a2', 'caixa-b1', 'caixa-b2'], 0, -130, rot=90)
# --- à esquerda: Mistério (compra e descarte), Eventos descartados, cartas pequenas (Feras/Invenções), ilha ---
fila(['cartas-misterio', 'descarte-misterio', 'descarte-eventos'], -160, 520, rot=90, para='y')
fila(['cartas-pequenas-retrato', 'ORIGINAL obj_12_map-tiles-animals-misc-expansions.stl', 'animais'], -360, 520, rot=0, para='y')
# --- acima: cenário, personagens, equipamento ---
fila(['FICHAS DE CENÁRIO', 'ORIGINAL obj_11_characters.stl', 'ORIGINAL obj_13_shelter-upgrades-herb-garden-pen-spyglass.stl'], 0, 860)
fila(['MANUAL', 'GUIAS'], 560, 860)
# --- à direita: expansões, miniaturas, caixas ---
fila(['cartas-animais-praia', 'cartas-expansoes-em-pe', 'caixa-pe-reserva'], 750, 520, para='y')
fila(['penglord-miniaturas-figuras', 'penglord-miniaturas-acampamento'], 820, 520)
fila(['caixa-c1', 'caixa-c2', 'caixa-d', 'caixa-e', 'caixa-funda', 'caixa-estreita', 'caixa-sobre-cartas-1', 'caixa-sobre-cartas-2'], 820, 330)
fica = [b for b in ordem if b not in alvo and b != 'TABULEIRO']
print('ficam na caixa:', fica)
json.dump(dict(alvo=alvo, caixa=[-820, 560]), open('setup.json', 'w'))
