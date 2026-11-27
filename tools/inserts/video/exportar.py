import sys, os, json, numpy as np, trimesh
sys.path.insert(0, '/home/user/elite-boardgamers/tools/inserts')
from projetos import robinson_crusoe_ce as rc
from insertgen import geom as g
from insertgen.stl import malha
from insertgen.pecas import Params
sys.path.insert(0, '/home/user/elite-boardgamers/tools/inserts')
from folha_guardar import _nome
S = '/tmp/claude-0/-home-user/d4bfdcd9-138d-5f4d-abb8-a8c8576edf03/scratchpad'
cfg = rc.carregar(); pecas, itens, reservas, ctx = rc.montar(cfg)
pmap = {p.nome: p for p in pecas}
ORIG = {'obj_13': 'js500-abrigo-melhorias', 'obj_12': 'js500-pecas-de-mapa', 'obj_11': 'js500-personagens',
        'obj_16': 'js500-fichas', 'obj_15': 'js500-dados-determinacao', 'obj_14': 'js500-recursos'}
p = Params()

def dec(v, f, alvo):
    m = trimesh.Trimesh(v, f, process=False)
    if len(m.faces) > alvo:
        m = m.simplify_quadric_decimation(face_count=alvo)
    return np.asarray(m.vertices), np.asarray(m.faces)

def coloca(v, rot90, pos):
    v = v - v.min(axis=0)
    if rot90 % 2:
        v = np.c_[-v[:, 1], v[:, 0], v[:, 2]]; v = v - v.min(axis=0)
    return v + np.array(pos)

objs = []
def add(nome, rotulo, v, f, cor, passo, opac=1.0):
    objs.append(dict(nome=nome, rotulo=rotulo, cor=cor, passo=passo, opac=opac,
                     v=np.round(v, 2).ravel().tolist(), f=f.ravel().astype(int).tolist()))

def passo_de(z):
    return 1 if z < 1 else (2 if z < 70 else (3 if z < 80 else 4))

CINZA, AZUL, LARANJA = '#b8b8b8', '#4f8fd0', '#e8a83c'
for it in sorted(itens, key=lambda i: (round(i.pos[2]), i.pos[0], i.pos[1])):
    nome = it.nome
    rot = _nome(nome).split('\n')[0]
    z = it.pos[2]
    if nome.startswith('ORIGINAL'):
        k = nome.split()[1][:6]
        fn = f'{S}/pacote/robinson-crusoe-insert/3-originais-js500/{ORIG[k]}.stl'
        m = trimesh.load(fn); v, f = dec(m.vertices, m.faces, 12000)
        add(nome, rot, coloca(v, it.rot90, it.pos), f, CINZA, passo_de(z))
        if k == 'obj_12':
            m = trimesh.load(f'{S}/pacote/robinson-crusoe-insert/3-originais-js500/js500-animais-vai-dentro-do-mapa.stl')
            v, f = dec(m.vertices, m.faces, 3000)
            v = v - v.min(axis=0) + np.array([it.pos[0] + 151.2 - 91.2 - 2, it.pos[1] + 2, it.pos[2] + 22 - 13])
            add('animais', 'ANIMAIS', v, f, '#a0a0a0', passo_de(z))
        continue
    pc = pmap.get(nome)
    if pc is None:
        continue
    v, f = malha(pc.solido); v, f = dec(v, f, 15000)
    cor = CINZA if nome.startswith('penglord') else (AZUL if nome.startswith(('cartas', 'descarte')) else LARANJA)
    add(nome, rot, coloca(v, it.rot90, it.pos), f, cor, passo_de(z))
    for lab, fant in pc.fantasmas:  # maços de cartas / placas do vulcão
        fv, ff = malha(fant)
        cor_f = '#7a4a2a' if 'vulcão' in lab else '#efe6cf'
        add(nome + ':' + lab, '', coloca_f := None or fv, ff, cor_f, passo_de(z)) if False else None
        # aplica a mesma rotação/posição da peça (fantasma está em coords da peça)
        (x0, y0, _), _ = g.bbox(pc.solido)
        fv2 = fv - np.array([x0, y0, 0])
        if it.rot90 % 2:
            w = pc.tamanho[1]; fv2 = np.c_[w - fv2[:, 1], fv2[:, 0], fv2[:, 2]]
        add(nome + ':' + lab, '', fv2 + np.array(it.pos), ff, cor_f, passo_de(z))
    tp = pmap.get(nome + '-tampa')
    if tp is not None:
        tv, tf = malha(tp.solido); tv, tf = dec(tv, tf, 6000)
        off = p.parede - p.rebaixo + p.folga_tampa
        tv = tv - tv.min(axis=0) + np.array([it.pos[0] + off, it.pos[1] + off, it.pos[2] + pc.tamanho[2] - p.tampa_esp])
        add(nome + '-tampa', '', tv, tf, '#f3c46a', passo_de(z))
# pilha do tabuleiro
Z0 = ctx['topo_insert']
camadas = [('TABULEIRO', 16, '#c9b27a'), ('FICHAS DE CENÁRIO', 4, '#8a5a3a'), ('MANUAL', 2, '#dcd2b0'), ('GUIAS', 4, '#5e7b4e')]
z = Z0
for nm, e, cor in camadas:
    b = trimesh.creation.box(extents=(277 if nm == 'TABULEIRO' else 290, 239 if nm == 'TABULEIRO' else 290, e))
    b.apply_translation((156.25, 156.25, z + e / 2))
    add(nm, nm, b.vertices, b.faces, cor, 5); z += e
cx = cfg['caixa_interna']
json.dump(dict(objs=objs, caixa=[cx['x'], cx['y'], cx['z']], ocup=312.5), open(f'{S}/video/cena.json', 'w'))
print(len(objs), 'objetos', sum(len(o['f']) // 3 for o in objs), 'triângulos', os.path.getsize(f'{S}/video/cena.json') // 1e6, 'MB')
