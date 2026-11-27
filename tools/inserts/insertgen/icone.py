"""Ícone tirado de foto: recorta o símbolo claro de uma carta, contorna e vira CrossSection (mm).

Só lê pixels de imagem (nada é executado). Fluxo:
  foto -> recorte quadrado em volta do ícone -> tons de cinza -> limiar (símbolo claro sobre fundo escuro)
  -> mantém o maior componente perto do centro -> contorno (matplotlib) -> polígonos -> escala p/ `tamanho` mm.
"""
import numpy as np
import manifold3d as m3


def icone_de_foto(caminho, recorte, tamanho=12.0, limiar=None, claro=True, raio_util=0.62, simplificar=0.15,
                  engrossar=0.0, min_frac=0.25):
    from PIL import Image, ImageOps, ImageFilter
    from scipy import ndimage
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    im = ImageOps.exif_transpose(Image.open(caminho)).convert("L").crop(recorte)
    im = im.resize((400, int(400 * im.height / im.width)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2))
    a = np.asarray(im, dtype=float)
    h, w = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    dentro = (xx - w / 2) ** 2 + (yy - h / 2) ** 2 < (raio_util * min(w, h) / 2) ** 2
    if limiar is None:
        limiar = (np.percentile(a[dentro], 90) + np.percentile(a[dentro], 30)) / 2
    m = (a > limiar) if claro else (a < limiar)
    m &= dentro
    lab, n = ndimage.label(m)
    if n == 0:
        raise ValueError("nenhum símbolo encontrado no recorte")
    tam = ndimage.sum(m, lab, range(1, n + 1))
    cen = ndimage.center_of_mass(m, lab, range(1, n + 1))
    perto = [((cy - h / 2) ** 2 + (cx - w / 2) ** 2) ** 0.5 < 0.35 * min(w, h) for cy, cx in cen]
    maior = max(t for t, ok in zip(tam, perto) if ok) if any(perto) else tam.max()
    manter = [i + 1 for i, (t, ok) in enumerate(zip(tam, perto)) if ok and t >= min_frac * maior]
    m = np.isin(lab, manter)
    m = ndimage.binary_fill_holes(m) if False else m
    cs = plt.contour(np.pad(m.astype(float), 2), levels=[0.5])
    polys = []
    for caminho_ in cs.allsegs[0]:
        if len(caminho_) >= 8:
            polys.append([(x, -y) for x, y in caminho_])
    plt.close("all")
    sec = m3.CrossSection(polys, m3.FillRule.EvenOdd)
    b = sec.bounds()
    k = tamanho / max(b[2] - b[0], b[3] - b[1])
    sec = sec.translate((-(b[0] + b[2]) / 2, -(b[1] + b[3]) / 2)).scale((k, k))
    if engrossar:
        sec = sec.offset(engrossar, m3.JoinType.Round, circular_segments=16)
    sec = sec.simplify(simplificar)
    # garante traço mínimo imprimível (0,8 mm): abre e fecha
    return sec


def icone_bau(tamanho=12.0):
    """Baú do tesouro desenhado em vetor, no estilo do ícone 'Treasure card' do manual:
    tampa abaulada, corpo, duas tiras verticais, junta da tampa e fechadura.
    As tiras/junta ficam em relevo (sem gravação), com 0,9 mm para a impressora reproduzir."""
    L, Hc, Ht = 12.0, 6.0, 4.5          # largura, altura do corpo, altura da tampa
    corpo = m3.CrossSection.square((L, Hc))
    r = 2.2
    tampa = m3.CrossSection.batch_hull([
        m3.CrossSection.square((L, 0.01)).translate((0, Hc)),
        m3.CrossSection.circle(r, 48).translate((r, Hc + Ht - r)),
        m3.CrossSection.circle(r, 48).translate((L - r, Hc + Ht - r))])
    bau = corpo + tampa
    t = 0.9
    linhas = (m3.CrossSection.square((L + 2, t)).translate((-1, Hc - t / 2))                       # junta
              + m3.CrossSection.square((t, Hc + Ht + 2)).translate((L * 0.27 - t / 2, -1))        # tira esq.
              + m3.CrossSection.square((t, Hc + Ht + 2)).translate((L * 0.73 - t / 2, -1)))       # tira dir.
    fechadura = m3.CrossSection.square((2.2, 2.6)).translate((L / 2 - 1.1, Hc - 2.2))
    furo = m3.CrossSection.circle(0.45, 24).translate((L / 2, Hc - 1.2))
    sec = (bau - linhas - fechadura) + (fechadura - m3.CrossSection.square((1.4, 1.8)).translate((L / 2 - 0.7, Hc - 1.8))) 
    sec = sec - furo
    b = sec.bounds()
    k = tamanho / max(b[2] - b[0], b[3] - b[1])
    return sec.translate((-(b[0] + b[2]) / 2, -(b[1] + b[3]) / 2)).scale((k, k))
