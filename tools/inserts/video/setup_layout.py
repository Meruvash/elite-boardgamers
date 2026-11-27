import json, numpy as np
d = json.load(open('cena.json'))
grp = {}
ordem = []
for o in d['objs']:
    base = o['nome'].split(':')[0]
    if base.endswith('-tampa'): base = base[:-6]
    v = np.array(o['v']).reshape(-1, 3)
    if base not in grp:
        grp[base] = [v.min(0), v.max(0)]; ordem.append(base)
    else:
        grp[base][0] = np.minimum(grp[base][0], v.min(0)); grp[base][1] = np.maximum(grp[base][1], v.max(0))
def tam(b): return grp[b][1] - grp[b][0]
def achar(prefixo): return [b for b in ordem if b.startswith(prefixo)]
alvo = {}
GAP = 18
def fila(nomes, x0, y0, eixo='x', alinhar='min'):
    x, y = x0, y0
    for n in nomes:
        t = tam(n)
        if eixo == 'x':
            pos = (x, y if alinhar == 'min' else y - t[1]); x += t[0] + GAP
        else:
            pos = (x if alinhar == 'min' else x - t[0], y - t[1]); y -= t[1] + GAP
        alvo[n] = [pos[0] - grp[n][0][0], pos[1] - grp[n][0][1], -grp[n][0][2] + 2.0]
BW, BH = 720, 520
# em cima do tabuleiro: Eventos, Mistério e descartes
fila(['cartas-eventos', 'descarte-eventos', 'cartas-misterio', 'descarte-misterio', 'cartas-pequenas-retrato'], 0, BH + 40)
# à direita: aventuras em pé + descartes
fila(['cartas-aventura-construir-coletar', 'descarte-construir', 'descarte-coletar', 'cartas-aventura-explorar-animais',
      'descarte-explorar', 'cartas-expansoes-em-pe'], BW + 40, BH, eixo='y')
# embaixo, fila 1: componentes de jogo
fila(['ORIGINAL obj_14_resources.stl', 'ORIGINAL obj_16_tokens.stl', 'ORIGINAL obj_15_dice-determination-black-white-blue.stl',
      'ORIGINAL obj_13_shelter-upgrades-herb-garden-pen-spyglass.stl', 'animais'], 0, -40, alinhar='max')
# embaixo, fila 2: caixas pequenas + miniaturas
cx = [b for b in ordem if b.startswith('caixa-')]
# quebra em linhas de até 760 mm
linhas, atual, larg = [], [], 0
for b in sorted(cx, key=lambda n: -tam(n)[1]):
    w = tam(b)[0]
    if atual and larg + w > 760: linhas.append(atual); atual, larg = [], 0
    atual.append(b); larg += w + GAP
linhas.append(atual)
y = -330
for ln in linhas:
    fila(ln, 0, y, alinhar='max'); y -= max(tam(b)[1] for b in ln) + GAP
fila(achar('penglord'), -40 - 113.6 * 2 - GAP, -40, alinhar='max')
# à esquerda do tabuleiro (preparação): personagens, peças de mapa, fichas de cenário, manual, guias
fila(['ORIGINAL obj_11_characters.stl', 'ORIGINAL obj_12_map-tiles-animals-misc-expansions.stl'], -40, BH, eixo='x', alinhar='min') if False else None
alvo_tmp=None
fila(['ORIGINAL obj_11_characters.stl'], -40-151.2-GAP-151.2, BH+40)
fila(['ORIGINAL obj_12_map-tiles-animals-misc-expansions.stl'], -40-151.2, BH+40)
fila(['FICHAS DE CENÁRIO', 'MANUAL', 'GUIAS'], -320, BH + 40, eixo='y', alinhar='max')
fica = [b for b in ordem if b not in alvo and b != 'TABULEIRO']
print('ficam na caixa:', fica)
json.dump(dict(alvo=alvo, caixa=[-1150, 80]), open('setup.json', 'w'))
