"""Peças paramétricas do insert.

Cada gerador devolve uma `Peca`: o sólido (manifold3d) já apoiado em z=0 e com
canto em (0,0,0), mais os "fantasmas": caixas que representam o conteúdo
(maço de cartas luvadas, fichas) e que a validação exige que caibam sem tocar
no plástico.
"""
from dataclasses import dataclass, field
import manifold3d as m3

from . import geom as g


@dataclass
class Peca:
    nome: str
    solido: m3.Manifold
    descricao: str = ""
    qtd: int = 1
    fantasmas: list = field(default_factory=list)   # [(rótulo, Manifold)]
    medidas: dict = field(default_factory=dict)      # medidas nominais declaradas (x, y, z)
    notas: list = field(default_factory=list)
    sem_texto: object = None  # sólido antes da gravação dos nomes (usado na checagem de parede fina)

    @property
    def tamanho(self):
        (x0, y0, z0), (x1, y1, z1) = g.bbox(self.solido)
        return (x1 - x0, y1 - y0, z1 - z0)


@dataclass
class Params:
    """Parâmetros de impressão e folgas (mm)."""
    parede: float = 2.0          # parede externa (5 linhas de 0,4)
    divisoria: float = 1.6       # parede interna entre poços
    piso: float = 1.2            # espessura do fundo
    raio_canto: float = 2.0      # arredondamento das arestas verticais externas
    folga_carta: float = 1.0     # folga por lado em volta da carta luvada (total 2,0)
    folga_maco: float = 1.5      # folga extra em cima do maço
    folga_tampa: float = 0.25    # folga por lado entre tampa e rebaixo
    tampa_esp: float = 1.6       # espessura da tampa embutida
    rebaixo: float = 0.8         # degrau interno onde a tampa assenta (parede restante >= 1,2)
    entalhe_larg: float = 24.0   # largura do entalhe de dedo das cartas
    raio_concha: float = 6.0     # raio do fundo em concha das fichas


def bandeja_baralhos(nome, pocos, p: Params, altura=None, entalhe=True, furo_piso=26.0, descricao="",
                     girar_carta=False, ref=None, rotulo=None, parede_lateral=None, bolso_dados=0.0):
    """Bandeja de mesa para maços DEITADOS (cartas luvadas), poços em fila ao longo de Y.

    pocos: lista; cada item é uma lista de Baralho que divide o mesmo poço
    (normalmente um só) ou [] para poço de descarte vazio. O poço é a maior
    carta luvada + 2*folga_carta; a profundidade é o maior conteúdo + folga_maco
    (ou `altura` fixa, que precisa comportar).
    Entalhes de dedo nas duas laterais longas de cada poço (pinça o maço) e furo
    no piso para empurrar o maço por baixo. Na mesa ela é o próprio monte de
    compra/descarte; na caixa, empilha (o fundo de uma é a tampa da outra).
    """
    ref = [b for poco in pocos for b in poco] + ([ref] if ref is not None else [])
    if not ref:
        raise ValueError(f"{nome}: precisa de ao menos um baralho (ou ref=) para dimensionar o poço")
    ext = lambda b: tuple(reversed(b.externo)) if girar_carta else b.externo  # noqa: E731
    larg_c = max(ext(b)[0] for b in ref) + 2 * p.folga_carta
    comp_c = max(ext(b)[1] for b in ref) + 2 * p.folga_carta
    pilha = [sum(b.altura_pilha() for b in poco) for poco in pocos]
    prof_min = max(pilha) + p.folga_maco
    if altura is not None:
        if altura - p.piso < prof_min - 1e-6:
            raise ValueError(f"{nome}: altura {altura} não comporta {max(pilha):.1f} mm de cartas + folga + piso")
        prof = altura - p.piso
    else:
        prof = prof_min
    n = len(pocos)
    pl = p.parede if parede_lateral is None else parede_lateral  # paredes compridas (faces X)
    X = 2 * pl + larg_c
    yb = (bolso_dados + p.divisoria) if bolso_dados else 0.0     # bolso de dados na frente (Y=0)
    Y = 2 * p.parede + n * comp_c + (n - 1) * p.divisoria + yb
    Z = p.piso + prof
    corpo = g.caixa_arred(X, Y, Z, p.raio_canto)
    furos, fant = [], []
    if bolso_dados:
        furos.append(g.cavidade_concha(larg_c, bolso_dados, prof + 5, min(p.raio_concha, prof * 0.6),
                                       (pl, p.parede, p.piso)))
    for i, poco in enumerate(pocos):
        y0 = p.parede + yb + i * (comp_c + p.divisoria)
        furos.append(g.caixa_arred(larg_c, comp_c, prof + 1, 1.0, (pl, y0, p.piso)))
        cy = y0 + comp_c / 2
        if entalhe:
            prof_ent = max(min(prof * 0.7, prof - 2.5), 4.0)
            furos.append(g.entalhe_dedo(p.entalhe_larg, prof_ent, pl + 2, (-1, cy, Z), eixo="x"))
            furos.append(g.entalhe_dedo(p.entalhe_larg, prof_ent, pl + 2, (X - pl - 1, cy, Z), eixo="x"))
        if furo_piso:
            furos.append(g.cilindro(furo_piso / 2, p.piso + 2, (X / 2, cy, -1)))
        z = p.piso
        for b in poco:
            L, A = ext(b)
            h = b.altura_pilha()
            fant.append((b.nome, g.caixa(L, A, h, (pl + (larg_c - L) / 2, y0 + (comp_c - A) / 2, z))))
            z += h
    sol = corpo - g.uniao(furos)
    base = sol
    if rotulo:
        txt, ics = rotulo if isinstance(rotulo, tuple) else (rotulo, None)
        sol = _gravar_pontas(sol, txt, X, Y, Z, p.parede, icones=ics)
    rot = ["+".join(b.nome for b in poco) if poco else "descarte" for poco in pocos]
    pc = Peca(nome, sol, descricao or ("Poços: " + " | ".join(rot)), fantasmas=fant, medidas={"x": X, "y": Y, "z": Z})
    pc.sem_texto = base
    cap = int((prof - p.folga_maco) / ref[0].espessura_unit / 1.08)
    pc.notas.append(f"poço {larg_c:.1f} x {comp_c:.1f} x {prof:.1f} mm; cabem ~{cap} cartas luvadas por poço")
    pc.notas += [f"{r}: {s:.1f} mm de maço" for r, s in zip(rot, pilha)]
    return pc


def bandeja_fichas(nome, X, Y, Z, colunas, p: Params, tampa=True, descricao=""):
    """Bandeja de fichas com compartimentos em concha e (opcional) tampa embutida.

    colunas: lista de colunas (esq->dir); cada coluna = (fração_largura, [frações_altura...])
    — as frações são relativas e normalizadas. Ex.: [(1, [1, 1]), (2, [1])].
    Com tampa, a parede tem rebaixo interno; a tampa fica rente ao topo
    (bandejas empilham e viajam fechadas).
    Devolve (bandeja, tampa_ou_None).
    """
    corpo = g.caixa_arred(X, Y, Z, p.raio_canto)
    topo_util = Z - (p.tampa_esp if tampa else 0)
    prof = topo_util - p.piso
    if prof < 4:
        raise ValueError(f"{nome}: altura insuficiente para compartimentos")
    larg_int = X - 2 * p.parede - (len(colunas) - 1) * p.divisoria
    tot = sum(c[0] for c in colunas)
    furos = []
    x = p.parede
    for frac, linhas in colunas:
        w = larg_int * frac / tot
        alt_int = Y - 2 * p.parede - (len(linhas) - 1) * p.divisoria
        ty = sum(linhas)
        y = p.parede
        for fl in linhas:
            h = alt_int * fl / ty
            furos.append(g.cavidade_concha(w, h, prof + 5, min(p.raio_concha, prof * 0.6), (x, y, p.piso)))
            y += h + p.divisoria
        x += w + p.divisoria
    tp = None
    if tampa:
        # rebaixo: abre a parede por dentro (parede - rebaixo fica de pé) na altura da tampa
        ins = p.parede - p.rebaixo
        furos.append(g.caixa_arred(X - 2 * ins, Y - 2 * ins, p.tampa_esp + 1, max(p.raio_canto - ins, 0.5),
                                   (ins, ins, topo_util)))
        tx, ty_ = X - 2 * ins - 2 * p.folga_tampa, Y - 2 * ins - 2 * p.folga_tampa
        placa = g.caixa_arred(tx, ty_, p.tampa_esp, max(p.raio_canto - ins - p.folga_tampa, 0.5))
        # furo de dedo para levantar a tampa
        placa = placa - g.cilindro(7, p.tampa_esp + 2, (tx / 2, 0, -1))
        tp = Peca(nome + "-tampa", placa, f"Tampa embutida de {nome}",
                  medidas={"x": tx, "y": ty_, "z": p.tampa_esp})
        # entalhe na bandeja alinhado ao furo da tampa (dedo passa por baixo)
        furos.append(g.cilindro(7, Z, (X / 2, ins + p.folga_tampa, topo_util - 3)))
    sol = corpo - g.uniao(furos)
    return Peca(nome, sol, descricao, medidas={"x": X, "y": Y, "z": Z}), tp


def bloco_espaco(nome, X, Y, Z, p: Params, descricao="Calço", entalhes=False):
    """Calço/bandeja rasa oca (só paredes e piso). Com entalhes=True, ganha um entalhe de dedo no meio de
    cada parede curta (Y=0 e Y=máx) para tirar da caixa."""
    corpo = g.caixa_arred(X, Y, Z, p.raio_canto)
    oco = g.caixa_arred(X - 2 * p.parede, Y - 2 * p.parede, Z, 1.0, (p.parede, p.parede, p.piso))
    furos = [oco]
    if entalhes:
        prof = max(Z - p.piso - 2.0, 4.0)
        furos.append(g.entalhe_dedo(30.0, prof, p.parede + 2, (X / 2, -1, Z), eixo="y"))
        furos.append(g.entalhe_dedo(30.0, prof, p.parede + 2, (X / 2, Y - p.parede - 1, Z), eixo="y"))
    return Peca(nome, corpo - g.uniao(furos), descricao, medidas={"x": X, "y": Y, "z": Z})


def bandeja_em_pe(nome, baralhos, p: Params, altura, parede=1.6, folga_comp=1.0, folga_maco=1.5,
                  esp_divisoria=1.2, descricao="", retrato=False, parede_y=None, rotulo=None):
    """Bandeja de guarda com cartas EM PÉ apoiadas no lado comprido (estilo PengLord).

    O lado comprido da carta luvada fica ao longo de Y (poço = comprimento + 2*folga_comp);
    os maços ficam enfileirados ao longo de X, separados por divisórias soltas
    (`divisoria()`), uma entre cada par de maços. A parede da frente e a de trás têm
    um recorte grande para ver e puxar as cartas.
    """
    L = max(b.externo[0] for b in baralhos)   # altura da carta em pé
    A = max(b.externo[1] for b in baralhos)   # comprimento, deitado ao longo de Y
    if retrato:  # carta em pé apoiada no lado CURTO (mais alta, ocupa menos comprimento)
        L, A = A, L
    n_div = len(baralhos) - 1
    interno_x = sum(b.altura_pilha() for b in baralhos) + n_div * esp_divisoria + folga_maco
    comp = A + 2 * folga_comp
    py = parede if parede_y is None else parede_y
    X, Y, Z = interno_x + 2 * parede, comp + 2 * py, altura
    if Z - p.piso < L + 0.5:
        raise ValueError(f"{nome}: altura {Z} baixa para carta em pé de {L:.1f} mm")
    corpo = g.caixa_arred(X, Y, Z, p.raio_canto)
    furos = [g.caixa_arred(interno_x, comp, Z, 0.8, (parede, py, p.piso))]
    larg_rec = min(comp - 24, 60.0)
    prof_rec = Z * 0.5
    furos.append(g.entalhe_dedo(larg_rec, prof_rec, parede + 2, (-1, Y / 2, Z), eixo="x"))
    furos.append(g.entalhe_dedo(larg_rec, prof_rec, parede + 2, (X - parede - 1, Y / 2, Z), eixo="x"))
    sol = corpo - g.uniao(furos)
    base = sol
    if rotulo:
        txt, ics = rotulo if isinstance(rotulo, tuple) else (rotulo, None)
        sol = _gravar_pontas(sol, txt, X, Y, Z, py, icones=ics)
    fant, x = [], parede + folga_maco / 2
    for i, b in enumerate(baralhos):
        h = b.altura_pilha()
        fant.append((b.nome, g.caixa(h, A, L, (x, py + folga_comp, p.piso))))
        x += h + esp_divisoria
    pc = Peca(nome, sol, descricao or ("Em pé: " + " | ".join(b.nome for b in baralhos)),
              fantasmas=fant, medidas={"x": X, "y": Y, "z": Z})
    pc.sem_texto = base
    pc.notas.append(f"poço {interno_x:.1f} x {comp:.1f} mm, carta em pé de {L:.1f} mm; {n_div} divisória(s) solta(s)")
    pc.notas += [f"{b.nome}: {b.altura_pilha():.1f} mm de maço" for b in baralhos]
    return pc


def divisoria(nome, comp_poco, altura_util, esp=1.2, folga=0.5):
    """Divisória solta para bandeja em pé: impressa deitada, com furo para o dedo."""
    X, Y = comp_poco - 2 * folga, altura_util - folga
    placa = g.caixa_arred(X, Y, esp, 3.0)
    placa = placa - g.cilindro(9, esp + 2, (X / 2, Y, -1))
    return Peca(nome, placa, "Divisória solta entre maços em pé", medidas={"x": X, "y": Y, "z": esp})


def _gravar_pontas(sol, rotulo, X, Y, Z, parede, prof=0.6, icones=None):
    """Grava o nome nas duas paredes curtas (faces y=0 e y=Y), legível de fora.
    A gravação deixa parede - prof de espessura (o validador exige >= 1,2 mm)."""
    if parede - prof < 1.2 - 1e-6:
        raise ValueError(f"parede de {parede} mm fina demais para gravar {prof} mm de texto")
    larg = X - 2 * max(4.0, parede + 2.5)
    alt = min(Z * 0.62, 30.0 if icones else 16.0)
    zc = Z * 0.45
    if Z > 1.8 * X and not icones:  # face alta e estreita: texto em pé, letra bem maior
        sec = g.texto_2d(rotulo, Z * 0.8, X - 2 * max(3.0, parede + 1.5)).rotate(90)
        cortes = []
        for yf, d in ((0.0, +1), (Y, -1)):
            s2 = (sec.mirror((1, 0)) if d < 0 else sec).extrude(prof + 0.5).rotate((90, 0, 0))
            s2 = s2.translate((X / 2, yf + prof, Z / 2)) if d > 0 else s2.mirror((0, 1, 0)).translate((X / 2, yf - prof, Z / 2))
            cortes.append(s2)
        return sol - (cortes[0] + cortes[1])
    t1 = g.gravacao_face_y(rotulo, X / 2, zc, larg, alt, prof, 0.0, +1, icones)
    t2 = g.gravacao_face_y(rotulo, X / 2, zc, larg, alt, prof, Y, -1, icones)
    return sol - (t1 + t2)


def gravar_topo(pc, linhas, prof=0.5, margem=4.0):
    """Grava texto na face de cima de uma peça plana (tampa), legível de cima. Texto longo em peça
    estreita é girado 90°. Guarda o sólido sem texto para a checagem de parede."""
    (x0, y0, z0), (x1, y1, z1) = g.bbox(pc.solido)
    w, h = x1 - x0, y1 - y0
    girar = h > 1.8 * w
    lw, lh = (h - 2 * margem, w - 2 * margem) if girar else (w - 2 * margem, h - 2 * margem)
    sec = g.rotulo_2d(linhas, lw, min(lh, 20.0))
    if girar:
        sec = sec.rotate(90)
    cut = sec.extrude(prof + 0.5).translate(((x0 + x1) / 2, (y0 + y1) / 2 + (0 if girar else 2.0), z1 - prof))
    pc.sem_texto = pc.solido
    pc.solido = pc.solido - cut
    return pc
