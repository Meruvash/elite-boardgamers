#!/usr/bin/env python3
"""Folha de uma página (A4) com a ordem de guardar o insert na caixa.
Uso: python3 tools/inserts/folha_guardar.py [saida.pdf]"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
MONT = os.path.join(AQUI, "saida", "robinson-crusoe-ce", "montagem.png")

PASSOS = [
    ("1. FUNDO DA CAIXA", [
        "Esquerda: ABRIGO (bandeja mais fina) → PEÇAS DE MAPA (com a bandejinha de ANIMAIS dentro) → PERSONAGENS.",
        "Meio: MINIATURAS — figuras na frente, acampamento atrás.",
        "Direita, em pé, da frente para trás: CONSTRUIR·COLETAR → EXPLORAR·ANIMAIS → EXPANSÕES.",
        "Canto de trás, à esquerda: EVENTOS (deitada) e PEQUENAS (em pé) ao lado.",
    ]),
    ("2. SEGUNDO ANDAR", [
        "Sobre PERSONAGENS: FICHAS → DADOS·DETERMINAÇÃO por cima.",
        "Ao lado delas: caixa estreita NÚMEROS·CLIMA.",
        "Sobre as MINIATURAS (encostada à direita): RECURSOS.",
        "Sobre EVENTOS: MISTÉRIO.   Sobre o acampamento: DESCARTE EVENTOS.",
        "Sobre as 3 bandejas em pé: RESERVA 1 (frente) e RESERVA 2 (atrás).",
    ]),
    ("3. VULCÃO", [
        "BANDEJA DO VULCÃO por cima de RECURSOS + caixa estreita; placas da torre deitadas dentro.",
    ]),
    ("4. CAMADA DE CIMA (tudo fica no mesmo nível)", [
        "Sobre DADOS: DESCARTE CONSTRUIR, DESCARTE COLETAR, DESCARTE EXPLORAR (da frente para trás);",
        "   FERIMENTOS (caixa fina ao lado) e DESCOBERTA (atrás).",
        "Sobre o VULCÃO: DESCARTE MISTÉRIO e 1º JOGADOR·RODADA (frente), BASES DE LÍDER (atrás).",
        "Sobre RESERVA 1 e 2: DADOS EXTRAS (frente) e MARCADORES EXTRAS (atrás).",
        "Atrás, sobre MISTÉRIO/PEQUENAS: SLEEVES RESERVA.   Sobre DESCARTE EVENTOS: PROMOS.",
    ]),
    ("5. POR CIMA DE TUDO", [
        "TABULEIRO dobrado → FICHAS DE CENÁRIO → MANUAL → 2 GUIAS DA CAMPANHA. Feche a tampa.",
    ]),
]


NOMES = {
    "obj_13": "ABRIGO\n↓ PEÇAS DE MAPA\n↓ PERSONAGENS", "obj_12": "PEÇAS DE MAPA", "obj_11": "PERSONAGENS", "obj_16": "FICHAS\n↓ DADOS·DETERMIN.",
    "obj_15": "FICHAS\n↓ DADOS·DETERMIN.", "obj_14": "RECURSOS", "cartas-eventos": "EVENTOS", "cartas-pequenas-retrato": "PEQ.",
    "penglord-miniaturas-figuras": "MINIATURAS\nfiguras", "penglord-miniaturas-acampamento": "MINIATURAS\nacampamento",
    "cartas-aventura-construir-coletar": "CONSTRUIR\nCOLETAR", "cartas-aventura-explorar-animais": "EXPLORAR\nANIMAIS",
    "cartas-expansoes-em-pe": "EXPANSÕES", "caixa-estreita": "NÚM.\nCLIMA", "descarte-eventos": "DESC.\nEVENTOS",
    "cartas-misterio": "MISTÉRIO", "caixa-sobre-cartas-1": "RESERVA 1", "caixa-sobre-cartas-2": "RESERVA 2",
    "bandeja-vulcao": "VULCÃO\n(sobre RECURSOS\n+ NÚM.·CLIMA)", "descarte-construir": "DESC. CONSTRUIR", "descarte-coletar": "DESC. COLETAR",
    "descarte-explorar": "DESC. EXPLORAR", "caixa-a2": "DESCOBERTA", "caixa-a1": "FERIM.", "caixa-d": "SLEEVES RESERVA",
    "descarte-misterio": "DESC.\nMISTÉRIO", "caixa-b2": "BASES DE LÍDER\n+ FICHAS EXTRAS", "caixa-e": "PROMOS",
    "caixa-b1": "1º JOG.\nRODADA", "caixa-c1": "DADOS\nEXTRAS", "caixa-c2": "MARCAD.\nEXTRAS"}


def _nome(n):
    n = n.replace("ORIGINAL ", "")
    for k, v in NOMES.items():
        if n.startswith(k):
            return v
    return n


def _plantas(fig, ret):
    import json
    from matplotlib.patches import Rectangle
    rel = json.load(open(os.path.join(AQUI, "saida", "robinson-crusoe-ce", "relatorio.json"), encoding="utf-8"))
    itens = rel["montagem"]
    x0, y0, w, h = ret
    paineis = [("FUNDO (passo 1) — vista de cima", lambda z: z < 1),
               ("SEGUNDO ANDAR + VULCÃO (passos 2 e 3)", lambda z: 40 <= z < 80),
               ("CAMADA DE CIMA (passo 4)", lambda z: z >= 80)]
    lado = min(w / 3 - 0.01, h * 11.69 / 8.27)
    for i, (tit, filtro) in enumerate(paineis):
        ax = fig.add_axes([x0 + i * (w / 3), y0 + (h - lado * 8.27 / 11.69) / 2, lado, lado * 8.27 / 11.69])
        ax.add_patch(Rectangle((0, 0), 316, 316, fill=False, lw=1.5))
        sel = sorted([m for m in itens if filtro(m["pos"][2])], key=lambda m: m["pos"][2])
        def dentro(a, b):
            (ax_, ay, _), (aw, ah, _) = a["pos"], a["tam"]
            (bx, by, _), (bw, bh, _) = b["pos"], b["tam"]
            return ax_ >= bx - 0.5 and ay >= by - 0.5 and ax_ + aw <= bx + bw + 0.5 and ay + ah <= by + bh + 0.5
        # mostra só o que fica visível de cima (peças cobertas por outra mais alta no mesmo painel somem)
        vis = [m for m in sel if not any(o is not m and o["pos"][2] > m["pos"][2] and dentro(m, o) for o in sel)]
        for m in vis:
            (x, y, _), (tw, th, _) = m["pos"], m["tam"]
            nome = _nome(m["nome"])
            cor = "#c9c9c9" if m["origem"] == "original" or "MINIATURAS" in nome else (
                "#7fb0e0" if m["nome"].startswith(("cartas", "descarte")) else "#f0c070")
            ax.add_patch(Rectangle((x, y), tw, th, fc=cor, ec="k", lw=0.6))
            ax.text(x + tw / 2, y + th / 2, nome, ha="center", va="center", fontsize=5.6,
                    rotation=90 if th > 1.8 * tw and tw < 60 else 0)
        ax.text(158, -12, "FRENTE", ha="center", fontsize=6, weight="bold")
        ax.set_xlim(-3, 319); ax.set_ylim(-18, 319); ax.set_aspect("equal"); ax.axis("off")
        ax.set_title(tit, fontsize=7.5, weight="bold")


def main(saida):
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.text(0.06, 0.965, "Robinson Crusoe — como guardar o insert", fontsize=16, weight="bold")
    fig.text(0.06, 0.945, "Frente = lado mais perto de você com a caixa aberta (onde ficam as bandejas em pé à direita). "
             "Para jogar, é a ordem inversa.", fontsize=7.5, style="italic")
    y = 0.925
    for titulo, linhas in PASSOS:
        fig.text(0.06, y, titulo, fontsize=10.5, weight="bold", color="#7a3b0c")
        y -= 0.019
        for ln in linhas:
            fig.text(0.08, y, ln, fontsize=8.4)
            y -= 0.0165
        y -= 0.008
    _plantas(fig, [0.03, 0.03, 0.94, y - 0.04])
    fig.savefig(saida)
    print(saida)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "saida", "robinson-crusoe-ce", "COMO-GUARDAR.pdf"))
