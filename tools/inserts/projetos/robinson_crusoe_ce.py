"""Robinson Crusoe — Edição de Colecionador: insert "misto" para sleeves Bucaneiros PADRÃO
com espaço reservado para o tabuleiro por cima.

- Maços de JOGO deitados em bandejas que vão para a mesa (compra/descarte).
- Maços dos MISTÉRIOS em pé (estilo PengLord), com divisórias soltas, para guarda.
- Bandejas de componentes do insert original (js500 + remix Mistérios) reaproveitadas.

Planta (caixa 320 x 320, z para cima):
  Faixa de 246 mm (Y 0-246):
    X 0-151,2    pilha original personagens/peças/abrigo (0-51) + pilha recursos/dados/fichas (51-103)
                 + caixa longa com tampa (51-104)
    X 151,2-249,2 miniaturas (0-52) + componentes MT (52-63) + peças MT/animais + 2 bandejas de
                 cartas pequenas + caixa de promos (63-104)
    X 249,2-fim  2 bandejas em pé dos Mistérios (0-70) + caixa com tampa (70-104)
                 + 2 caixas com tampa no fundo (0-52, 52-104)
  Faixa do fundo (Y 246-fim): 3 posições de bandejas deitadas, 2 níveis de 52 mm.
  Camada plana (104-topo): tabuleiro dobrado, fichas de cenário/personagem, manual.
"""
import json
import os

from insertgen.cartas import Baralho, carregar_catalogo, sleeve_envelope
from insertgen.pecas import Params, bandeja_baralhos, bandeja_em_pe, bandeja_fichas, bloco_espaco, divisoria, gravar_topo

_BAR = {}
from insertgen.validar import Item

AQUI = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(AQUI, "robinson-crusoe-ce.json")

NIVEL = 52.0      # módulo de altura (as bandejas originais de 52 mm ditam)
TOPO = 2 * NIVEL  # 104: topo plano do insert, onde deita o tabuleiro
FAIXA = 246.0     # comprimento das peças originais; a faixa do fundo começa aqui


TERCEIROS = os.path.join(AQUI, "..", "dados", "terceiros", "penglord")


def penglord_ajustadas(comprimento_total):
    """As duas bandejas de miniaturas do PengLord (CC BY-NC-SA 4.0) encurtadas em Y para que, juntas,
    meçam `comprimento_total` (originais: 173,4 + 145 = 318,4 mm).

    Em vez de escalar (o que afinaria as paredes), retira fatias finas que passam só pelo MEIO dos
    compartimentos: as paredes continuam com a espessura original e cada compartimento perde um pouco.
    Cortes (Y no arquivo original): figuras = meio das 6 fileiras; acampamento = meio das 3 faixas."""
    import manifold3d as m3
    import numpy as np
    from insertgen import stl as stlio
    from insertgen.pecas import Peca
    cortes = {"mini_tray_-_large.stl": [14.75, 43.75, 72.75, 100.75, 129.75, 158.75],
              "mini_tray_-_camp.stl": [14.75, 45.0, 103.0]}
    nomes = [("mini_tray_-_large.stl", "penglord-miniaturas-figuras"),
             ("mini_tray_-_camp.stl", "penglord-miniaturas-acampamento")]
    malhas = {}
    for arq, _ in nomes:
        v, f = stlio.ler(os.path.join(TERCEIROS, arq))
        v = v - v.min(axis=0)
        malhas[arq] = m3.Manifold(m3.Mesh(vert_properties=v.astype(np.float32), tri_verts=f.astype(np.uint32)))
    total = sum(malhas[a].bounding_box()[4] for a, _ in nomes)
    tirar = max(0.0, total - comprimento_total)
    n_cortes = sum(len(c) for c in cortes.values())
    d = tirar / n_cortes
    out = []
    for arq, nome in nomes:
        sol = malhas[arq]
        for c in sorted(cortes[arq], reverse=True):
            if d <= 0:
                break
            baixo = sol.trim_by_plane((0, -1, 0), -c)          # mantém y <= c
            cima = sol.trim_by_plane((0, 1, 0), c + d).translate((0, -d, 0))  # y >= c+d, desce d
            sol = baixo + cima
        b = sol.bounding_box()
        pc = Peca(nome, sol, f"Bandeja do PengLord (CC BY-NC-SA 4.0) encurtada {d * len(cortes[arq]):.1f} mm "
                  f"no meio dos compartimentos (paredes intactas)",
                  medidas={"x": b[3] - b[0], "y": b[4] - b[1], "z": b[5] - b[2]})
        pc.notas.append(f"{len(cortes[arq])} cortes de {d:.2f} mm")
        out.append(pc)
    return out


ICONES = os.path.join(AQUI, "..", "dados", "icones")


def icones(tamanho=11.0):
    """Ícones disponíveis (recortados das fotos/manual ou desenhados). Faltando arquivo, o ícone fica de fora."""
    import json as _json
    from insertgen.icone import icone_de_foto
    cfg = _json.load(open(os.path.join(ICONES, "icones.json"), encoding="utf-8"))
    out = {}
    for k, v in cfg.items():
        if k.startswith("_"):
            continue
        if v.get("vetor") == "bau":
            from insertgen.icone import icone_bau
            out[k] = icone_bau(tamanho)
            continue
        arq = os.path.join(ICONES, v["foto"])
        if os.path.exists(arq):
            out[k] = icone_de_foto(arq, tuple(v["recorte"]), tamanho, **v.get("opcoes", {}))
    return out


def com_icone(texto, ic, *chaves):
    lst = [ic[k] for k in chaves if k in ic]
    return (texto, lst) if lst else texto


def carregar(config=CONFIG):
    with open(config, encoding="utf-8") as fh:
        return json.load(fh)


def _montar_completo(cfg, p=None):
    """Versão 2 (com extras: Mistérios, miniaturas). Devolve (pecas, itens, reservas, contexto)."""
    p = p or Params()
    lay = cfg.get("layout", {})
    cat = carregar_catalogo()
    sl = {t: sleeve_envelope(cat, d["usar"], d["compativel_com"]) for t, d in cfg["sleeves"].items()}
    bar = {}
    for k, d in cfg["baralhos"].items():
        c = cfg["cartas"][d["tipo"]]
        bar[k] = Baralho(k, c["tamanho"], d["qtd"], c["espessura"], sl[d["tipo"]])
    B = lambda *ks: [bar[k] for k in ks]  # noqa: E731
    gc = cfg["cartas"]["grande"]
    ref_g = Baralho("ref", gc["tamanho"], 0, gc["espessura"], sl["grande"])
    orig_t = cfg["originais_reaproveitados"]

    pecas, itens = [], []

    def add(peca, pos, rot90=0):
        if peca not in pecas:
            pecas.append(peca)
        it = Item(peca.nome, peca.tamanho, pos, peca.solido, rot90=rot90)
        itens.append(it)
        return it

    def orig(nome, pos, rot90=0):
        it = Item("ORIGINAL " + nome, orig_t[nome], pos, None, rot90=rot90, origem="original")
        itens.append(it)
        return it

    def tampada(nome, X, Y, Z, colunas, desc):
        t, tp = bandeja_fichas(nome, X, Y, Z, colunas, p, descricao=desc)
        pecas.append(tp)
        return t

    def deitada(nome, pocos, alt, desc):
        return bandeja_baralhos(nome, pocos, p, altura=alt, descricao=desc, ref=ref_g)

    # ---------- coluna esquerda: pilhas originais ----------
    z = 0.0
    for n in ("obj_13_shelter-upgrades-herb-garden-pen-spyglass.stl",
              "obj_12_map-tiles-animals-misc-expansions.stl", "obj_11_characters.stl"):
        z = orig(n, (0, 0, z)).caixa[1][2]
    topo_A, A_x = z, orig_t["obj_11_characters.stl"][0]
    for n in ("obj_16_tokens.stl", "obj_15_dice-determination-black-white-blue.stl", "obj_14_resources.stl"):
        z = orig(n, (0, 0, z)).caixa[1][2]
    B_x = orig_t["obj_14_resources.stl"][0]
    add(tampada("caixa-longa", A_x - B_x, FAIXA, TOPO - topo_A, [(1, [1, 1, 1])],
                "Caixa longa com tampa: fichas de descoberta / marcadores extras"), (B_x, 0, topo_A))

    # ---------- coluna do meio: miniaturas e Mistérios ----------
    mini = orig("obj_3_Player Miniatures", (A_x, 0, 0), rot90=1)
    larg_mt = max(mini.tam[0], orig_t["obj_20_Mystery Tales Tiles"][0])
    mtc = orig("obj_17_Mystery Tales Components", (A_x, 0, NIVEL))
    z_mt = mtc.caixa[1][2]
    tiles = orig("obj_20_Mystery Tales Tiles", (A_x, 0, z_mt))
    orig("obj_19_animals.stl", (A_x, 0, tiles.caixa[1][2]))
    y_peq = orig_t["obj_19_animals.stl"][1]
    alt_peq = (TOPO - z_mt) / 2
    peq1 = bandeja_baralhos("cartas-pequenas-base", [B("invencoes", "mt-invencoes"), B("equipamento", "mt-equipamento")],
                            p, altura=alt_peq, girar_carta=True,
                            descricao="Cartas pequenas: Invenções (+MT) | Equipamento inicial (+MT)")
    peq2 = bandeja_baralhos("cartas-pequenas-feras-mt", [B("feras"), B("mt-pequenas")], p, altura=alt_peq,
                            girar_carta=True, descricao="Cartas pequenas: Feras | pequenas dos Mistérios")
    add(peq1, (A_x, y_peq, z_mt))
    add(peq2, (A_x, y_peq, z_mt + alt_peq))
    y_promo = y_peq + peq1.tamanho[1]
    add(tampada("caixa-promos", larg_mt, mtc.caixa[1][1] - y_promo, TOPO - z_mt, [(1, [1])],
                "Caixa com tampa: lunetas, promos, peças soltas"), (A_x, y_promo, z_mt))

    # ---------- coluna direita: Mistérios em pé ----------
    col_x = A_x + larg_mt
    alt_pe = lay.get("altura_bandeja_em_pe", 70.0)
    par_pe = lay.get("parede_em_pe", 1.6)
    fm_pe = lay.get("folga_maco_em_pe", 1.5)
    pe1 = bandeja_em_pe("cartas-mt-em-pe-1", B("mt-eventos", "mt-misterio", "mt-insanidade"), p, alt_pe, parede=par_pe,
                        folga_maco=fm_pe, descricao="Mistérios em pé: Eventos | Mistério | Insanidade (2 divisórias)")
    pe2 = bandeja_em_pe("cartas-mt-em-pe-2", B("mt-aventura", "mt-outros"), p, alt_pe, parede=par_pe,
                        folga_maco=fm_pe, descricao="Mistérios em pé: Aventura | outros (1 divisória)")
    larg_col = max(pe1.tamanho[0], pe2.tamanho[0])
    if pe2.tamanho[0] < larg_col:  # mesma largura nas duas, para a caixa de cima apoiar por igual
        pe2 = bandeja_em_pe("cartas-mt-em-pe-2", B("mt-aventura", "mt-outros"), p, alt_pe, parede=par_pe,
                            folga_maco=fm_pe + larg_col - pe2.tamanho[0],
                            descricao="Mistérios em pé: Aventura | outros (1 divisória)")
    add(pe1, (col_x, 0, 0))
    add(pe2, (col_x, pe1.tamanho[1], 0))
    y_pe = pe1.tamanho[1] + pe2.tamanho[1]
    div = divisoria("divisoria-em-pe", pe1.tamanho[1] - 2 * par_pe, alt_pe - p.piso)
    div.qtd = 3
    pecas.append(div)
    add(tampada("caixa-sobre-mt", larg_col, y_pe, TOPO - alt_pe, [(1, [1]), (1, [1])],
                "Caixa com tampa sobre os Mistérios: dados de resina, cápsulas, extras"), (col_x, 0, alt_pe))
    add(tampada("caixa-dados-extras", larg_col, FAIXA - y_pe, NIVEL, [(1, [1])],
                "Dados extras (com tampa)"), (col_x, y_pe, 0))
    add(tampada("caixa-descoberta", larg_col, FAIXA - y_pe, NIVEL, [(1, [1, 1])],
                "Fichas de descoberta (com tampa, 2 compartimentos)"), (col_x, y_pe, NIVEL))

    # ---------- faixa do fundo: bandejas de jogo deitadas ----------
    mis = deitada("cartas-misterio", [B("misterio")], NIVEL,
                  "Mistério (compra). Na mesa, ao lado do tabuleiro.")
    con = deitada("cartas-aventura-construir", [B("aventura-construir")], NIVEL / 2, "Aventura — Construir")
    col = deitada("cartas-aventura-coletar", [B("aventura-coletar")], NIVEL / 2, "Aventura — Coletar")
    exp = deitada("cartas-aventura-explorar", [B("aventura-explorar")], NIVEL / 2, "Aventura — Explorar")
    esp = deitada("cartas-especiais", [B("especiais")], NIVEL / 2,
                  "Naufrágio, Arrumar acampamento, Sexta-feira, Cão, promos")
    eve = deitada("cartas-eventos", [B("eventos"), []], NIVEL, "Eventos: compra | descarte")
    d1 = deitada("cartas-descarte-aventura", [[]], NIVEL / 2, "Descarte vazio (aventura), vai para a mesa")
    d2 = deitada("cartas-descarte-misterio", [[]], NIVEL / 2, "Descarte vazio (mistério), vai para a mesa")
    passo = mis.tamanho[1]  # bandeja girada 90°: o comprimento vira a largura
    for i, (baixo, cima) in enumerate([(mis, None), (col, con), (esp, exp)]):
        add(baixo, (i * passo, FAIXA, 0), rot90=1)
        if cima is not None:
            add(cima, (i * passo, FAIXA, baixo.tamanho[2]), rot90=1)
    add(eve, (0, FAIXA, NIVEL), rot90=1)
    add(d1, (2 * passo, FAIXA, NIVEL), rot90=1)
    add(d2, (2 * passo, FAIXA, NIVEL + d1.tamanho[2]), rot90=1)

    return _fechar(cfg, p, pecas, itens, sl, bar)


def _fechar(cfg, p, pecas, itens, sl, bar):
    X, Y, Z = (cfg["caixa_interna"][k] for k in "xyz")
    cp = cfg["camada_plana"]
    espessura_plana = sum(i["espessura"] for i in cp["itens"]) + cp["folga_tampa"]
    topo = max(it.caixa[1][2] for it in itens)
    reservas = [("tabuleiro + camada plana", ((0, 0, Z - espessura_plana), (X, Y, Z)))]
    zmin = cfg["caixa_interna"].get("z_minimo_provavel")
    if zmin:  # a tampa precisa fechar também no pior caso de altura da caixa
        reservas.append((f"tabuleiro + camada plana (caixa de {zmin:.0f} mm)",
                         ((0, 0, zmin - espessura_plana), (X, Y, zmin))))
    ctx = {"z_minimo": zmin, "folga_pior_caso": (zmin - topo - espessura_plana) if zmin else None,"topo_insert": topo, "espessura_plana": espessura_plana, "espaco_tabuleiro": Z - topo,
           "folga_sobrando": Z - topo - espessura_plana, "sleeves": sl, "baralhos": bar, "params": p}
    return pecas, itens, reservas, ctx


def montar(cfg, p=None):
    """Escolhe a versão pelo conteúdo da caixa: só o jogo base (padrão) ou com extras."""
    ex = cfg.get("extras", {})
    if ex.get("misterios") or ex.get("tem"):
        return _montar_completo(cfg, p)
    if ex.get("penglord_minis"):
        return _montar_v5(cfg, p)
    if ex.get("miniaturas"):
        return _montar_v4(cfg, p)
    return _montar_base(cfg, p)


def _montar_base(cfg, p=None):
    """Versão 3: só o jogo base da Edição de Colecionador (sem Mistérios, miniaturas, Treasure Chest,
    Livro de Aventuras). Insert mais baixo (78 mm) para sobrar altura ao tabuleiro e aos cadernos.

    Planta (Y 0-246 = peças originais de 246 mm; Y 246-318,4 = faixa do fundo):
      X 0-151,2    pilha original personagens/peças/abrigo (0-51) + bandejas de carta de mesa (51-78)
      X 151,2-274  pilha original recursos/dados/fichas (0-52) + caixa com tampa (52-78)
      X 274-318,4  cartas pequenas em pé (0-52) + caixa com tampa (0-52) + caixa longa (52-78)
      Faixa do fundo: Eventos compra|descarte e Mistério (0-52), 3 Aventuras (52-78)
    """
    p = p or Params()
    lay = cfg.get("layout", {})
    cat = carregar_catalogo()
    sl = {t: sleeve_envelope(cat, d["usar"], d["compativel_com"]) for t, d in cfg["sleeves"].items()}
    bar = {}
    for k, d in cfg["baralhos"].items():
        c = cfg["cartas"][d["tipo"]]
        bar[k] = Baralho(k, c["tamanho"], d["qtd"], c["espessura"], sl[d["tipo"]])
    B = lambda *ks: [bar[k] for k in ks]  # noqa: E731
    gc = cfg["cartas"]["grande"]
    ref_g = Baralho("ref", gc["tamanho"], 0, gc["espessura"], sl["grande"])
    orig_t = cfg["originais_reaproveitados"]
    MEIO = NIVEL / 2
    topo = NIVEL + MEIO  # 78

    pecas, itens = [], []

    def add(peca, pos, rot90=0):
        if peca not in pecas:
            pecas.append(peca)
        it = Item(peca.nome, peca.tamanho, pos, peca.solido, rot90=rot90)
        itens.append(it)
        return it

    def orig(nome, pos):
        it = Item("ORIGINAL " + nome, orig_t[nome], pos, None, origem="original")
        itens.append(it)
        return it

    def tampada(nome, X, Y, Z, colunas, desc):
        t, tp = bandeja_fichas(nome, X, Y, Z, colunas, p, descricao=desc)
        pecas.append(tp)
        return t

    def deitada(nome, pocos, alt, desc):
        return bandeja_baralhos(nome, pocos, p, altura=alt, descricao=desc, ref=ref_g)

    # pilhas originais lado a lado no fundo
    z = 0.0
    for n in ("obj_13_shelter-upgrades-herb-garden-pen-spyglass.stl",
              "obj_12_map-tiles-animals-misc-expansions.stl", "obj_11_characters.stl"):
        z = orig(n, (0, 0, z)).caixa[1][2]
    topo_A, A_x = z, orig_t["obj_11_characters.stl"][0]
    z = 0.0
    for n in ("obj_16_tokens.stl", "obj_15_dice-determination-black-white-blue.stl", "obj_14_resources.stl"):
        z = orig(n, (A_x, 0, z)).caixa[1][2]
    topo_B, B_x = z, A_x + orig_t["obj_14_resources.stl"][0]

    # faixa do fundo: jogo deitado
    eve = deitada("cartas-eventos", [B("eventos"), []], NIVEL, "Eventos: compra | descarte")
    mis = deitada("cartas-misterio", [B("misterio")], NIVEL, "Mistério (compra)")
    add(eve, (0, FAIXA, 0), rot90=1)
    x_mis = eve.tamanho[1]
    add(mis, (x_mis, FAIXA, 0), rot90=1)
    passo = mis.tamanho[1]
    for i, k in enumerate(("aventura-construir", "aventura-coletar", "aventura-explorar")):
        add(deitada("cartas-" + k, [B(k)], MEIO, "Aventura — " + k.split("-")[1].capitalize()),
            (i * passo, FAIXA, NIVEL), rot90=1)

    # sobre a pilha A: bandejas de mesa de meia altura (2 x 2) + caixa com tampa no resto
    alt_A = topo - topo_A
    sobre = [deitada("cartas-especiais", [B("especiais")], alt_A,
                     "Naufrágio, Arrumar acampamento, Sexta-feira, Cão"),
             deitada("cartas-descarte-aventura", [[]], alt_A, "Descarte de aventura (vazio, vai para a mesa)"),
             deitada("cartas-descarte-misterio", [[]], alt_A, "Descarte de mistério (vazio, vai para a mesa)"),
             deitada("cartas-descarte-extra", [[]], alt_A, "Descarte extra / maço do cenário (vazio)")]
    lx, ly = sobre[0].tamanho[0], sobre[0].tamanho[1]
    for i, pc in enumerate(sobre):
        add(pc, ((i % 2) * lx, (i // 2) * ly, topo_A))
    add(tampada("caixa-sobre-personagens", A_x, FAIXA - 2 * ly, alt_A, [(1, [1]), (1, [1])],
                "Caixa com tampa: marcadores e peças soltas"), (0, 2 * ly, topo_A))
    add(tampada("caixa-sobre-recursos", B_x - A_x, FAIXA, topo - topo_B, [(1, [1, 1]), (1, [1, 1])],
                "Caixa com tampa (4 compartimentos): espaço livre para os extras no futuro"), (A_x, 0, topo_B))

    # coluna direita: cartas pequenas em pé + caixas
    larg_d = cfg["caixa_interna"].get("ocupacao_comprovada", {}).get("x", 318.4) - B_x
    par_pe = lay.get("parede_em_pe", 1.2)
    peq = bandeja_em_pe("cartas-pequenas-em-pe", B("invencoes", "equipamento", "feras"), p, NIVEL, parede=par_pe,
                        descricao="Cartas pequenas em pé: Invenções | Equipamento inicial | Feras (2 divisórias)")
    peq = bandeja_em_pe("cartas-pequenas-em-pe", B("invencoes", "equipamento", "feras"), p, NIVEL, parede=par_pe,
                        folga_maco=1.5 + larg_d - peq.tamanho[0],
                        descricao="Cartas pequenas em pé: Invenções | Equipamento inicial | Feras (2 divisórias)")
    add(peq, (B_x, 0, 0))
    div = divisoria("divisoria-pequenas", peq.tamanho[1] - 2 * par_pe, NIVEL - p.piso)
    div.qtd = 2
    pecas.append(div)
    add(tampada("caixa-dados-fichas", larg_d, FAIXA - peq.tamanho[1], NIVEL, [(1, [1, 1])],
                "Caixa com tampa: dados e fichas soltas"), (B_x, peq.tamanho[1], 0))
    add(tampada("caixa-longa", larg_d, FAIXA, MEIO, [(1, [1, 1, 1])],
                "Caixa longa com tampa: fichas de descoberta / marcadores"), (B_x, 0, NIVEL))
    return _fechar(cfg, p, pecas, itens, sl, bar)


def _montar_v4(cfg, p=None):
    """Versão 4: jogo base + Everything New (miniaturas, cartas extras, vulcão desmontado),
    sem Mistérios nem Livro de Aventuras. Caixa ~127 mm de altura interna.

    As três bandejas originais de 52 mm (personagens/peças, recursos/fichas, miniaturas) não cabem
    lado a lado; em vez de empilhar uma inteira sobre a outra (104 mm), as três bandejas finas de
    recursos/dados/fichas são distribuídas por cima:
      X 0-151,2    obj_13+obj_12+obj_11 (0-51) + fichas obj_16 + dados obj_15 (51-83) + caixa estreita
      X 151,2-249  miniaturas obj_3 (0-52) + recursos obj_14 (52-72) + bolsão do vulcão (72-86)
      X 249-318,4  maço das expansões, cartas pequenas em pé, caixa (0-52) + caixa longa (52-86)
      Faixa do fundo: Eventos compra|descarte e Mistério (0-52), 3 Aventuras (52-86)
    """
    p = p or Params()
    lay = cfg.get("layout", {})
    cat = carregar_catalogo()
    sl = {t: sleeve_envelope(cat, d["usar"], d["compativel_com"]) for t, d in cfg["sleeves"].items()}
    bar = {}
    for k, d in cfg["baralhos"].items():
        c = cfg["cartas"][d["tipo"]]
        bar[k] = Baralho(k, c["tamanho"], d["qtd"], c["espessura"], sl[d["tipo"]])
    B = lambda *ks: [bar[k] for k in ks]  # noqa: E731
    gc = cfg["cartas"]["grande"]
    ref_g = Baralho("ref", gc["tamanho"], 0, gc["espessura"], sl["grande"])
    orig_t = cfg["originais_reaproveitados"]
    TOPO4 = lay.get("topo_v4", 86.0)
    X_OK = cfg["caixa_interna"].get("ocupacao_comprovada", {}).get("x", 318.4)

    pecas, itens = [], []

    def add(peca, pos, rot90=0):
        if peca not in pecas:
            pecas.append(peca)
        it = Item(peca.nome, peca.tamanho, pos, peca.solido, rot90=rot90)
        itens.append(it)
        return it

    def orig(nome, pos, rot90=0):
        it = Item("ORIGINAL " + nome, orig_t[nome], pos, None, rot90=rot90, origem="original")
        itens.append(it)
        return it

    def tampada(nome, X, Y, Z, colunas, desc):
        t, tp = bandeja_fichas(nome, X, Y, Z, colunas, p, descricao=desc)
        pecas.append(tp)
        return t

    def deitada(nome, pocos, alt, desc):
        return bandeja_baralhos(nome, pocos, p, altura=alt, descricao=desc, ref=ref_g)

    # coluna A: personagens/peças/abrigo + fichas + dados
    z = 0.0
    for n in ("obj_13_shelter-upgrades-herb-garden-pen-spyglass.stl",
              "obj_12_map-tiles-animals-misc-expansions.stl", "obj_11_characters.stl",
              "obj_16_tokens.stl", "obj_15_dice-determination-black-white-blue.stl"):
        z = orig(n, (0, 0, z)).caixa[1][2]
    topo_A, A_x = z, orig_t["obj_11_characters.stl"][0]
    B_x = orig_t["obj_14_resources.stl"][0]
    add(tampada("caixa-estreita", A_x - B_x, FAIXA, TOPO4 - 51.0, [(1, [1, 1, 1])],
                "Caixa estreita com tampa (marcadores, fichas extras)"), (B_x, 0, 51.0))

    # coluna das miniaturas + recursos por cima + bolsão do vulcão
    mini = orig("obj_3_Player Miniatures", (A_x, 0, 0), rot90=1)
    col_x = mini.caixa[1][0]
    rec = orig("obj_14_resources.stl", (A_x, 0, NIVEL))
    vx, vy, vz = cfg["componentes_soltos"]["vulcao_placas"]["mm"]
    itens.append(Item("PLACAS DO VULCÃO (deitadas, sem bandeja)", (vx, vy, vz), (A_x, 0, rec.caixa[1][2]),
                      None, origem="componente"))

    # coluna direita (0-52): maço das expansões, cartas pequenas em pé, caixa
    larg_d = X_OK - col_x
    exp = deitada("cartas-expansoes", [B("praia", "tracos", "tracos-secretos", "moral-dramatica")], NIVEL,
                  "Procurando na Praia + Traços + Traços Secretos + Moral Dramática (maços empilhados)")
    add(exp, (col_x, 0, 0))
    par_pe = lay.get("parede_em_pe", 1.2)
    peq = bandeja_em_pe("cartas-pequenas-em-pe", B("invencoes", "equipamento", "feras"), p, NIVEL, parede=par_pe,
                        descricao="Cartas pequenas em pé: Invenções | Equipamento inicial | Feras (2 divisórias)")
    add(peq, (col_x, exp.tamanho[1], 0))
    div = divisoria("divisoria-pequenas", peq.tamanho[1] - 2 * par_pe, NIVEL - p.piso)
    div.qtd = 2
    pecas.append(div)
    y_cx = exp.tamanho[1] + peq.tamanho[1]
    add(tampada("caixa-dados-extras", larg_d, FAIXA - y_cx, NIVEL, [(1, [1])],
                "Caixa com tampa: dados de madeira extras, especiais"), (col_x, y_cx, 0))
    x_longa = rec.caixa[1][0]
    add(tampada("caixa-longa", X_OK - x_longa, FAIXA, TOPO4 - NIVEL, [(1, [1, 1, 1])],
                "Caixa longa com tampa: fichas de descoberta / marcadores"), (x_longa, 0, NIVEL))

    # faixa do fundo
    eve = deitada("cartas-eventos", [B("eventos"), []], NIVEL, "Eventos: compra | descarte")
    mis = deitada("cartas-misterio", [B("misterio", "especiais")], NIVEL,
                  "Mistério (compra); as cartas Especiais ficam por baixo")
    add(eve, (0, FAIXA, 0), rot90=1)
    add(mis, (eve.tamanho[1], FAIXA, 0), rot90=1)
    passo = mis.tamanho[1]
    an = bar["animais"]
    terco = -(-an.qtd // 3)
    for i, k in enumerate(("aventura-construir", "aventura-coletar", "aventura-explorar")):
        parte = Baralho(f"animais ({k.split('-')[1]})", an.carta, terco, an.espessura_carta, an.sl)
        add(deitada("cartas-" + k, [B(k) + [parte]], TOPO4 - NIVEL,
                    "Aventura — " + k.split("-")[1].capitalize() + " (as de Animais podem ir misturadas)"),
            (i * passo, FAIXA, NIVEL), rot90=1)
    return _fechar(cfg, p, pecas, itens, sl, bar)


def _montar_v5(cfg, p=None):
    """Versão 5: o que os projetos publicados já resolvem + o espaço do tabuleiro.

    - Componentes: bandejas originais js500/Hooper (obj_11..obj_16; obj_19 dentro do obj_12).
    - Miniaturas: as duas bandejas do PengLord (figuras + acampamento + companheiros + itens), 113,6 x 318,4.
    - Cartas: geradas para Bucaneiros CHIMERA / MINI EURO. Eventos e Mistério deitados (vão para a mesa);
      Aventuras, Animais e expansões em pé com divisórias (estilo PengLord); pequenas em pé, de retrato.
    - Topo plano a 86 mm; por cima, tabuleiro + fichas de cenário + manual + guias.
      X 0-151,2      obj_13+12+11 (0-51) + fichas obj_16 + dados obj_15 (51-83) + caixa estreita
      X 151,2-264,8  miniaturas PengLord (0-51,2) + recursos obj_14 (51,2-71,2) + placas do vulcão (71,2-85,2)
      X 264,8-318,4  3 bandejas de cartas em pé (0-64) + caixa com tampa (64-86)
      Faixa sob a coluna 1 (Y 246-318,4): Eventos (0-52), Mistério (52-86), cartas pequenas em pé
    """
    p = p or Params()
    lay = cfg.get("layout", {})
    cat = carregar_catalogo()
    sl = {t: sleeve_envelope(cat, d["usar"], d["compativel_com"]) for t, d in cfg["sleeves"].items()}
    bar = {}
    for k, d in cfg["baralhos"].items():
        c = cfg["cartas"][d["tipo"]]
        bar[k] = Baralho(k, c["tamanho"], d["qtd"], c["espessura"], sl[d["tipo"]])
    B = lambda *ks: [bar[k] for k in ks]  # noqa: E731
    gc = cfg["cartas"]["grande"]
    ref_g = Baralho("ref", gc["tamanho"], 0, gc["espessura"], sl["grande"])
    orig_t = cfg["originais_reaproveitados"]
    T = lay.get("topo_v4", 86.0)
    XY = cfg["caixa_interna"].get("ocupacao_maxima", 318.4)
    par_pe = lay.get("parede_em_pe", 1.2)

    pecas, itens = [], []

    def add(peca, pos, rot90=0):
        if peca not in pecas:
            pecas.append(peca)
        it = Item(peca.nome, peca.tamanho, pos, peca.solido, rot90=rot90)
        itens.append(it)
        return it

    def orig(nome, pos):
        it = Item("ORIGINAL " + nome, orig_t[nome], pos, None, origem="original")
        itens.append(it)
        return it

    def tampada(nome, X, Y, Z, colunas, desc):
        c = cfg.get("conteudo_bandejas", {}).get(nome, {})
        t, tp = bandeja_fichas(nome, X, Y, Z, colunas, p, descricao=c.get("descricao", desc))
        if c.get("rotulo"):
            gravar_topo(tp, c["rotulo"])
        pecas.append(tp)
        return t

    # coluna 1: componentes js500
    z = 0.0
    for n in ("obj_13_shelter-upgrades-herb-garden-pen-spyglass.stl",
              "obj_12_map-tiles-animals-misc-expansions.stl", "obj_11_characters.stl",
              "obj_16_tokens.stl", "obj_15_dice-determination-black-white-blue.stl"):
        z = orig(n, (0, 0, z)).caixa[1][2]
    A_x = orig_t["obj_11_characters.stl"][0]
    B_w = orig_t["obj_14_resources.stl"][0]

    # coluna 2: miniaturas PengLord (encurtadas em Y para caber na caixa) + recursos + vulcão
    pl = penglord_ajustadas(XY)
    for pc in pl:
        pecas.append(pc)
    ml = add(pl[0], (A_x, 0, 0))
    add(pl[1], (A_x, ml.caixa[1][1], 0))
    col3 = A_x + pl[0].tamanho[0]
    x_rec = col3 - B_w  # recursos avança sobre a coluna 1, na faixa livre ao lado das fichas/dados
    rec = orig("obj_14_resources.stl", (x_rec, 0, ml.caixa[1][2]))
    vx, vy, vz = cfg["componentes_soltos"]["vulcao_placas"]["mm"]
    z_rec = rec.caixa[1][2]
    VY = lay.get("vulcao_y", 158.0)  # placas ~122 x 150 mm: não precisa dos 246 inteiros
    bv = bloco_espaco("bandeja-vulcao", col3 - B_w, VY, T - z_rec, p, entalhes=True,
                      descricao="Bandeja rasa onde as placas do vulcão ficam deitadas (apoia a camada de cima)")
    from insertgen import geom as _g
    bv.fantasmas.append(("placas do vulcão", _g.caixa(vx, vy, vz, (p.parede + 1, p.parede + 1, p.piso))))
    pecas.append(bv)
    itens.append(Item(bv.nome, bv.tamanho, (B_w, 0, z_rec), bv.solido))
    # no espaço que sobrou ao lado do vulcão: Feras e Equipamento inicial em bandejas baixas, separadas
    xb = B_w
    for nome, k, rot in (("cartas-feras", "feras", "FERAS"), ("cartas-equipamento", "equipamento", ["EQUIPAMENTO", "INICIAL"])):
        tb = bandeja_baralhos(nome, [B(k)], p, altura=T - z_rec, parede_lateral=lay.get("parede_lateral_deitadas", 1.2),
                              rotulo=rot, descricao=f"{rot if isinstance(rot, str) else ' '.join(rot)} (cartas pequenas, "
                                                     f"deitadas). Vai para o lado do tabuleiro.")
        add(tb, (xb, VY + (FAIXA - VY - tb.tamanho[1]) / 2, z_rec))
        xb += tb.tamanho[0]
    add(tampada("caixa-estreita", x_rec - B_w, FAIXA, z_rec - 51.0, [(1, [1, 1, 1])],
                "Caixa estreita com tampa: bases de Líder, marcador de 1º jogador, extras"), (B_w, 0, 51.0))

    # coluna 3: cartas em pé
    larg3 = XY - col3
    alt_pe = lay.get("altura_em_pe_v5", 64.0)

    IC = icones()
    PY = 2.0  # paredes curtas mais grossas nas bandejas em pé, para gravar o nome

    def em_pe(nome, decks, desc, rotulo):
        pc = bandeja_em_pe(nome, decks, p, alt_pe, parede=par_pe, descricao=desc, parede_y=PY)
        return bandeja_em_pe(nome, decks, p, alt_pe, parede=par_pe, folga_maco=1.5 + larg3 - pc.tamanho[0],
                             descricao=desc, parede_y=PY, rotulo=rotulo)
    an = bar["animais"]
    # v6: as Aventuras saíram daqui (vão em bandejas próprias que ficam em cima do tabuleiro)
    pes = [em_pe("cartas-animais-praia", [an] + B("praia"),
                 "Em pé: Animais | Procurando na Praia (1 divisória)", ["ANIMAIS", "PRAIA"]),
           em_pe("cartas-expansoes-em-pe", B("tracos", "tracos-secretos", "moral-dramatica"),
                 "Em pé: Traços | Traços Secretos | Moral Dramática (2 divisórias)", ["EXPANSÕES"])]
    y = 0.0
    for pc in pes:
        add(pc, (col3, y, 0))
        y += pc.tamanho[1]
    res3 = tampada("caixa-pe-reserva", larg3, pes[0].tamanho[1], alt_pe, [(1, [1])],
                   "Caixa com tampa (reserva) no lugar da 3ª bandeja em pé")
    add(res3, (col3, y, 0))
    y += res3.tamanho[1]
    div = divisoria("divisoria-grandes", pes[0].tamanho[1] - 2 * PY, alt_pe - p.piso)
    div.qtd = 3
    pecas.append(div)
    for i in range(2):  # duas metades: inteira passaria da mesa da impressora
        add(tampada(f"caixa-sobre-cartas-{i + 1}", larg3, y / 2, T - alt_pe, [(1, [1])],
                    "Caixa com tampa sobre as cartas em pé (dados de madeira extras, fichas)"),
            (col3, i * y / 2, alt_pe))

    # faixa sob a coluna 1: Eventos (0-52) e Mistério (52-86) deitados; pequenas em pé de retrato
    PL = lay.get("parede_lateral_deitadas", 1.2)
    eve = bandeja_baralhos("cartas-eventos", [B("eventos")], p, altura=NIVEL, ref=ref_g, parede_lateral=PL, rotulo=com_icone("EVENTOS", IC, "eventos"),
                           descricao="Eventos (compra). Vai para a mesa.")
    mis = bandeja_baralhos("cartas-misterio", [B("misterio", "especiais")], p, altura=T - NIVEL, ref=ref_g,
                           parede_lateral=PL,
                           rotulo=com_icone("MISTÉRIO", IC, "misterio"),
                           descricao="Mistério (compra), com as Especiais por baixo. Vai para a mesa.")
    add(eve, (0, FAIXA, 0), rot90=1)
    add(mis, (0, FAIXA, NIVEL), rot90=1)
    peq = bandeja_em_pe("cartas-pequenas-retrato", B("invencoes"), p, T, parede=par_pe,
                        retrato=True, parede_y=PY, rotulo="INVENÇÕES",
                        folga_maco=32.0 - 2 * par_pe - bar["invencoes"].altura_pilha(),  # base larga: não tomba
                        descricao="Baralho de Invenções em pé (de retrato)")
    add(peq, (eve.tamanho[1], FAIXA, 0), rot90=1)
    # coluna vazia ao lado das cartas pequenas: caixa funda com tampa (também apoia a camada de cima)
    yf = FAIXA + peq.tamanho[0]
    add(tampada("caixa-funda", peq.tamanho[1], XY - yf, T, [(1, [1])],
                "Caixa funda com tampa ao lado das cartas pequenas"), (eve.tamanho[1], yf, 0))
    # (sem divisórias: a bandeja de cartas pequenas agora só leva as Invenções)
    global _BAR
    _BAR = bar
    if lay.get("descartes", True):
        _camada_descartes(cfg, p, add, pecas, itens, ref_g, T, A_x, B_w, x_rec, col3, XY, eve, peq, tampada, IC)
    return _fechar(cfg, p, pecas, itens, sl, bar)


def _camada_descartes(cfg, p, add, pecas, itens, ref_g, T, A_x, B_w, x_rec, col3, XY, eve, peq, tampada, IC=None):
    """Versão 6. Camada de cima (até TOPO_DESC):
    - 3 bandejas de Aventura (Construir, Coletar, Explorar) com bolso para os 3 dados da ação: vão para os
      espaços de ação na faixa de baixo do tabuleiro;
    - descartes de Construir/Coletar/Explorar, de Mistério e caixas com tampa;
    - descarte de Eventos no vão sobre o acampamento do PengLord."""
    lay = cfg.get("layout", {})
    TD = lay.get("topo_descartes", 105.0)
    PL = lay.get("parede_lateral_deitadas", 1.2)
    IC = IC or {}
    cont = cfg.get("conteudo_bandejas", {})
    bar = {k: v for k, v in []}

    def desc(nome, rot, alt, chave):
        return bandeja_baralhos(nome, [[]], p, altura=alt, ref=ref_g, rotulo=com_icone(rot, IC, chave),
                                parede_lateral=PL, descricao=f"Descarte ({rot[-1].lower()}). Vai para a mesa.")

    def aberta(nome, X, Y, Z, desc_):
        c = cont.get(nome, {})
        cols = c.get("colunas") or ([(1, [1])] if min(X, Y) < 60 else [(1, [1, 1]), (1, [1, 1])])
        t, tp = bandeja_fichas(nome, X, Y, Z, [tuple(cc) for cc in cols], p, tampa=True,
                               descricao=c.get("descricao", desc_))
        if c.get("rotulo"):
            gravar_topo(tp, c["rotulo"])
        pecas.append(tp)
        return t

    # 1) descarte de Eventos no vão sobre o acampamento do PengLord
    z_pl = 51.2
    d_ev = desc("descarte-eventos", ["DESCARTE", "EVENTOS"], T - z_pl, "eventos")
    add(d_ev, (A_x + (col3 - A_x - d_ev.tamanho[1]) / 2, FAIXA, z_pl), rot90=1)

    # 2) região A (componentes js500, topo 83): 3 bandejas de Aventura com bolso de dados + DESCOBERTA
    zA, hA = 83.0, TD - 83.0
    y = 0.0
    for k, rot in (("aventura-construir", "CONSTRUIR"), ("aventura-coletar", "COLETAR"),
                   ("aventura-explorar", "EXPLORAR")):
        chave = rot.lower()
        tb = bandeja_baralhos("cartas-" + k, [[_BAR[k]]], p, altura=hA, ref=ref_g, parede_lateral=PL,
                              bolso_dados=lay.get("bolso_dados", 20.0), rotulo=com_icone(rot, IC, chave),
                              descricao=f"Aventura — {rot.capitalize()} + os 3 dados da ação. Vai para o espaço "
                                        f"da ação na faixa de baixo do tabuleiro.")
        add(tb, (0, y, zA), rot90=1)
        y += tb.tamanho[0]
    add(aberta("caixa-a2", B_w, FAIXA - y, hA, "Caixa com tampa"), (0, y, zA))

    # 3) região B+C (caixa estreita + vulcão, topo 86): 3 descartes de Aventura + 2 caixas
    zB, hB = T, TD - T
    y = 0.0
    for nome, rot, ch in (("descarte-construir", "CONSTRUIR", "construir"), ("descarte-coletar", "COLETAR", "coletar"),
                          ("descarte-explorar", "EXPLORAR", "explorar")):
        d = desc(nome, ["DESCARTE", rot], hB, ch)
        add(d, (B_w, y, zB), rot90=1)
        y += d.tamanho[0]
    xa = B_w + d.tamanho[1]
    add(aberta("caixa-b1", col3 - xa, y, hB, "Caixa com tampa"), (xa, 0, zB))
    add(aberta("caixa-b2", col3 - B_w, FAIXA - y, hB, "Caixa com tampa"), (B_w, y, zB))

    # 4) coluna 3 (topo 86): 2 caixas
    y3 = max(it.caixa[1][1] for it in itens if it.caixa[0][0] >= col3 - 0.01 and it.caixa[0][2] < 1)
    for i in range(2):
        add(aberta(f"caixa-c{i + 1}", XY - col3, y3 / 2, hB, "Caixa com tampa"), (col3, i * y3 / 2, zB))

    # 5) faixa do fundo (topo 86): descarte de Mistério + caixa d; caixa e sobre o descarte de Eventos
    d_mi = desc("descarte-misterio", ["DESCARTE", "MISTÉRIO"], hB, "misterio")
    add(d_mi, (0, FAIXA, zB), rot90=1)
    xf = eve.tamanho[1] + peq.tamanho[1]
    add(aberta("caixa-d", xf - d_mi.tamanho[1], XY - FAIXA, hB, "Caixa com tampa"), (d_mi.tamanho[1], FAIXA, zB))
    add(aberta("caixa-e", col3 - A_x, XY - FAIXA, hB, "Caixa com tampa"), (A_x, FAIXA, zB))
