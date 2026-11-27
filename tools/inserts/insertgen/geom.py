"""Primitivas sólidas (manifold3d). Todas as funções devolvem Manifold em mm."""
import manifold3d as m3

SEG = 64  # segmentos por círculo completo


def caixa(x, y, z, pos=(0.0, 0.0, 0.0)):
    return m3.Manifold.cube((x, y, z)).translate(pos)


def retangulo_arred(x, y, r):
    """Seção retangular x*y com cantos de raio r, canto inferior em (0,0)."""
    r = max(0.0, min(r, x / 2 - 1e-3, y / 2 - 1e-3))
    if r <= 0:
        return m3.CrossSection.square((x, y))
    base = m3.CrossSection.square((x - 2 * r, y - 2 * r)).translate((r, r))
    return base.offset(r, m3.JoinType.Round, circular_segments=SEG)


def caixa_arred(x, y, z, r, pos=(0.0, 0.0, 0.0)):
    """Prisma com arestas verticais arredondadas (raio r)."""
    return retangulo_arred(x, y, r).extrude(z).translate(pos)


def cilindro(r, h, pos=(0.0, 0.0, 0.0), eixo="z"):
    c = m3.Manifold.cylinder(h, r, r, SEG)
    if eixo == "x":
        c = c.rotate((0, 90, 0))
    elif eixo == "y":
        c = c.rotate((-90, 0, 0))
    return c.translate(pos)


def cavidade_concha(x, y, z, r, pos=(0.0, 0.0, 0.0)):
    """Cavidade com fundo em concha: arestas do fundo e verticais com raio r.

    Fichas escorregam para fora com o dedo (boa para usar a bandeja na mesa).
    É o casco convexo de 4 esferas nos cantos do fundo + prisma arredondado acima.
    """
    r = max(0.0, min(r, x / 2 - 0.01, y / 2 - 0.01, z - 0.01))
    if r <= 0.05:
        return caixa(x, y, z, pos)
    esferas = [m3.Manifold.sphere(r, SEG).translate((cx, cy, r))
               for cx in (r, x - r) for cy in (r, y - r)]
    topo = caixa_arred(x, y, z - r, r, (0, 0, r))
    return m3.Manifold.batch_hull(esferas + [topo]).translate(pos)


def entalhe_dedo(largura, profundidade, espessura, pos, eixo="y"):
    """Recorte em U atravessando uma parede (para pegar cartas/fichas com o dedo).

    largura: abertura do U; profundidade: quanto desce a partir do topo;
    espessura: quanto atravessa (ao longo de `eixo`). pos = centro do topo do U,
    no início da travessia.
    """
    r = largura / 2
    h = max(profundidade - r, 0.0)
    sec = m3.CrossSection.square((largura, h + 50)).translate((-r, -h))
    sec = sec + m3.CrossSection.circle(r, SEG).translate((0, -h))
    u = sec.extrude(espessura)  # plano XY, extrudado em Z
    if eixo == "y":    # U no plano XZ, atravessa Y
        u = u.rotate((90, 0, 0)).mirror((0, 1, 0))
    elif eixo == "x":  # U no plano YZ, atravessa X
        u = u.rotate((90, 0, 0)).mirror((0, 1, 0)).rotate((0, 0, 90)).mirror((1, 0, 0))
    return u.translate(pos)


def uniao(lista):
    lista = [s for s in lista if s is not None]
    return m3.Manifold.batch_boolean(lista, m3.OpType.Add) if lista else m3.Manifold()


def bbox(solido):
    b = solido.bounding_box()
    return (b[0], b[1], b[2]), (b[3], b[4], b[5])


def texto_2d(linhas, larg_max, alt_max, tamanho=7.0, entrelinha=1.25):
    """Texto (uma ou mais linhas, centralizadas) como CrossSection, ajustado para caber em
    larg_max x alt_max (mm), com origem no centro. Fonte DejaVu Sans Bold (vem com o matplotlib)."""
    from matplotlib.textpath import TextPath
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(family="DejaVu Sans", weight="bold")
    if isinstance(linhas, str):
        linhas = [linhas]
    caminhos = [TextPath((0, 0), t, size=tamanho, prop=fp) for t in linhas]
    larg = max(c.get_extents().width for c in caminhos)
    alt_linha = tamanho * entrelinha
    alt = alt_linha * (len(linhas) - 1) + tamanho
    k = min(1.0, larg_max / larg, alt_max / alt)
    polys = []
    for i, c in enumerate(caminhos):
        e = c.get_extents()
        dx = -e.x0 - e.width / 2
        dy = (len(linhas) - 1 - i) * alt_linha - alt / 2 + tamanho * 0.12
        for pol in c.to_polygons():
            if len(pol) >= 3:
                polys.append([((x + dx) * k, (y + dy) * k) for x, y in pol])
    sec = m3.CrossSection(polys, m3.FillRule.EvenOdd)
    # funde contornos que só se encostam num ponto (ex.: cedilha do Ç), senão a malha fica com aresta dupla
    sec = sec.offset(0.05, m3.JoinType.Round, circular_segments=12).offset(-0.05, m3.JoinType.Round, circular_segments=12).simplify(0.02)
    # descarta pedacinhos menores que a impressora consegue fazer (< 0,3 mm²)
    partes = [q for q in sec.decompose() if q.area() >= 0.3]
    return m3.CrossSection.compose(partes) if partes else sec


def rotulo_2d(linhas, larg_max, alt_max, icones=None, gap=1.5):
    """Texto + ícones (CrossSections já centrados, tamanho em mm) num só desenho 2D centrado,
    ajustado para caber em larg_max x alt_max. Face alta: ícones em cima do texto; face baixa: ícones à esquerda."""
    if not icones:
        return texto_2d(linhas, larg_max, alt_max)
    n = len(icones)
    lado = max(max(b[2] - b[0], b[3] - b[1]) for b in (ic.bounds() for ic in icones))
    fila = m3.CrossSection()
    for i, ic in enumerate(icones):
        fila = fila + ic.translate((i * (lado + gap) - (n - 1) * (lado + gap) / 2, 0))
    fl, fa = n * lado + (n - 1) * gap, lado
    if alt_max >= 1.6 * fa:  # empilha: ícones em cima, texto embaixo
        txt = texto_2d(linhas, larg_max, alt_max - fa - gap)
        tb = txt.bounds()
        ta = tb[3] - tb[1]
        tot = fa + gap + ta
        sec = fila.translate((0, tot / 2 - fa / 2)) + txt.translate((0, -tot / 2 + ta / 2 - (tb[1] + tb[3]) / 2))
    else:  # lado a lado
        txt = texto_2d(linhas, larg_max - fl - gap, alt_max)
        tb = txt.bounds()
        tl = tb[2] - tb[0]
        tot = fl + gap + tl
        sec = fila.translate((-tot / 2 + fl / 2, 0)) + txt.translate((tot / 2 - tl / 2 - (tb[0] + tb[2]) / 2, 0))
    b = sec.bounds()
    k = min(1.0, larg_max / (b[2] - b[0]), alt_max / (b[3] - b[1]))
    return sec.scale((k, k))


def gravacao_face_y(linhas, x_centro, z_centro, larg_max, alt_max, prof=0.6, y_face=0.0, para_dentro=1, icones=None):
    """Sólido do texto para gravar (subtrair) numa face perpendicular a Y.
    para_dentro=+1: face em y=y_face com a peça do lado +Y (face 'da frente');
    para_dentro=-1: face em y=y_face com a peça do lado -Y (face 'de trás', texto espelhado para ler de fora)."""
    sec = rotulo_2d(linhas, larg_max, alt_max, icones)
    if para_dentro < 0:
        sec = sec.mirror((1, 0))
    s = sec.extrude(prof + 0.5).rotate((90, 0, 0))  # texto no plano XZ, ocupa y em [-(prof+0.5), 0]
    if para_dentro > 0:
        s = s.translate((x_centro, y_face + prof, z_centro))
    else:
        s = s.mirror((0, 1, 0)).translate((x_centro, y_face - prof, z_centro))
    return s
