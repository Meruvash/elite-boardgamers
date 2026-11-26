import sys, glob, os, json, numpy as np, trimesh
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
P, REL, MONT = sys.argv[1], sys.argv[2], sys.argv[3]
rel = json.load(open(REL))
qtd = {p['arquivo']: p['qtd'] for p in rel['pecas']}
desc = {p['arquivo']: p['descricao'] for p in rel['pecas']}
pos = {}
for m in rel['montagem']:
    pos.setdefault(m['nome'].replace('ORIGINAL ', ''), m)
ORIG = {'js500-personagens': 'obj_11_characters.stl', 'js500-pecas-de-mapa': 'obj_12_map-tiles-animals-misc-expansions.stl',
        'js500-abrigo-melhorias': 'obj_13_shelter-upgrades-herb-garden-pen-spyglass.stl', 'js500-recursos': 'obj_14_resources.stl',
        'js500-dados-determinacao': 'obj_15_dice-determination-black-white-blue.stl', 'js500-fichas': 'obj_16_tokens.stl',
        'js500-animais-vai-dentro-do-mapa': None}
DESC_O = {'js500-personagens': 'Fichas de personagem (3 camadas), peões, Sexta-feira, companheiros',
          'js500-pecas-de-mapa': 'Peças de ilha, caverna, clima, naufrágio; recebe a bandeja de animais',
          'js500-abrigo-melhorias': 'Melhorias de abrigo, horta, cercado, lunetas', 'js500-recursos': 'Recursos (madeira, comida, peles...)',
          'js500-dados-determinacao': 'Dados e fichas de determinação; marcadores preto/branco/azul', 'js500-fichas': 'Fichas diversas',
          'js500-animais-vai-dentro-do-mapa': 'Animais (encaixa dentro da bandeja de peças de mapa)'}
linhas = []
for pasta, grupo in [('1-teste', 'Teste'), ('2-novas', 'Nova'), ('3-originais-js500', 'js500')]:
    for f in sorted(glob.glob(f'{P}/{pasta}/*.stl')):
        m = trimesh.load(f); e = m.bounds[1] - m.bounds[0]
        n = os.path.basename(f); base = n[:-4]
        q = qtd.get(n, 1)
        if grupo == 'js500':
            d = DESC_O[base]; k = ORIG[base]
            mm = pos.get(k) if k else None
        else:
            d = desc.get(n, 'Peça de teste de encaixe' if grupo == 'Teste' else ''); mm = pos.get(base)
        onde = '-'
        if mm:
            x, y, z = mm['pos']; onde = f"x{x:.0f} y{y:.0f} z{z:.0f}" + (" (girada 90°)" if mm['girada_90'] else "")
        elif base.endswith('-tampa'):
            onde = 'encaixa na caixa de mesmo nome'
        elif base.startswith('divisoria'):
            onde = 'solta, dentro das bandejas em pé'
        elif 'animais' in base:
            onde = 'dentro da bandeja de peças de mapa'
        g = m.volume / 1000 * 1.24 * 0.95
        linhas.append(dict(grupo=grupo, arq=n, q=q, x=e[0], y=e[1], z=e[2], g=g * q, d=d, onde=onde, mesh=m))
tot_g = sum(l['g'] for l in linhas if l['grupo'] != 'Teste')
tot_p = sum(l['q'] for l in linhas if l['grupo'] != 'Teste')

with PdfPages(sys.argv[4]) as pdf:
    # página 1
    fig = plt.figure(figsize=(8.27, 11.69)); fig.text(0.07, 0.95, 'Insert Robinson Crusoe — Edição de Colecionador (Conclave) + Everything New', fontsize=13, weight='bold')
    txt = f"""DOCUMENTO DE IMPRESSÃO — todas as medidas em milímetros

CAIXA (medida com régua e trena): 315,5 x 315,5 mm por dentro, 138 mm de altura útil.
INSERT MONTADO: 314 x 314 mm de fundo, 100 mm de altura. Por cima: tabuleiro dobrado + fichas
de cenário + manual + 2 guias (~24 mm). Sobram ~11 mm até a tampa.
CARTAS: grandes 58 x 88 no sleeve Bucaneiros CHIMERA (luvada ~62 x 90,5, medida com régua);
pequenas 44 x 68 no sleeve Bucaneiros MINI EURO.

CONFIGURAÇÃO DO FATIADOR (vale para todas as peças)
 - Material: PLA ou PETG       - Bico: 0,4 mm       - Camada: 0,2 mm (texto gravado sai nítido)
 - Paredes/perímetros: 3        - Topo/fundo: 4 camadas       - Preenchimento: 15% (grade ou giroide)
 - Suporte: NÃO                 - Adesão: saia (skirt); brim só se a peça descolar
 - Escala: 100% — NÃO redimensionar, NÃO girar em pé. Os arquivos já estão na posição certa:
   apoiados na mesa, com a boca/abertura para cima. Medidas exatas: qualquer escala estraga o encaixe.
 - Mesa mínima: 256 x 256 mm (a maior peça mede 151,2 x 246 mm)
 - Tolerância esperada: ±0,2 mm. Se a impressora sai "gorda" (peças maiores que o arquivo),
   calibre antes; as caixas encostam umas nas outras e a folga total na caixa é 1,5 mm por lado.

ORDEM DE IMPRESSÃO
 1. Pasta 1-teste (5 peças pequenas, < 1 h). O cliente confere se a carta luvada entra e sai
    sem dobrar o canto e se a tampa de teste encaixa. Só seguir depois disso.
 2. penglord-miniaturas-figuras.stl — o cliente confere as miniaturas.
 3. Todo o resto das pastas 2-novas e 3-originais-js500 (quantidades na tabela).

TOTAL (sem os testes): {tot_p} peças, ~{tot_g/1000:.1f} kg de filamento (estimativa pelo volume
das peças; o fatiador dá o valor exato).
QUANTIDADES QUE NÃO SÃO 1: divisoria-grandes = 5 cópias; divisoria-pequenas = 2 cópias.
"""
    fig.text(0.07, 0.90, txt, fontsize=8.6, va='top', family='DejaVu Sans Mono'); pdf.savefig(fig); plt.close(fig)
    # tabelas
    por_pag = 17
    for i in range(0, len(linhas), por_pag):
        fig = plt.figure(figsize=(11.69, 8.27)); ax = fig.add_axes([0.02, 0.02, 0.96, 0.9]); ax.axis('off')
        fig.text(0.02, 0.95, 'Lista de peças — arquivo, quantidade, medida externa (X x Y x Z mm), filamento e posição na caixa', fontsize=11, weight='bold')
        dados = [[l['grupo'], l['arq'], str(l['q']), f"{l['x']:.1f} x {l['y']:.1f} x {l['z']:.1f}", f"{l['g']:.0f} g",
                  l['onde'], (l['d'][:62] + '…') if len(l['d']) > 63 else l['d']] for l in linhas[i:i + por_pag]]
        t = ax.table(cellText=dados, colLabels=['Pasta', 'Arquivo', 'Qtd', 'Medida X x Y x Z', 'Filam.', 'Posição na caixa', 'Para quê'],
                     loc='upper left', colWidths=[0.05, 0.25, 0.03, 0.12, 0.05, 0.16, 0.34], cellLoc='left')
        t.auto_set_font_size(False); t.set_fontsize(6.6); t.scale(1, 1.75)
        pdf.savefig(fig); plt.close(fig)
    # montagem
    fig = plt.figure(figsize=(11.69, 8.27)); ax = fig.add_axes([0, 0.05, 1, 0.88]); ax.imshow(plt.imread(MONT)); ax.axis('off')
    fig.text(0.02, 0.95, 'Onde vai cada peça (planta de cima por nível e corte de frente). Posições x/y/z da tabela em mm, a partir do canto da caixa.', fontsize=10, weight='bold')
    pdf.savefig(fig); plt.close(fig)
    # vistas 3D
    luz = np.array([0.3, -0.5, 0.8]); luz /= np.linalg.norm(luz)
    for i in range(0, len(linhas), 12):
        fig = plt.figure(figsize=(11.69, 8.27)); fig.suptitle('Como cada peça deve ficar na mesa da impressora (abertura para cima)', fontsize=11, weight='bold')
        for j, l in enumerate(linhas[i:i + 12]):
            m = l['mesh'].copy(); m.apply_translation(-m.bounds[0])
            if len(m.faces) > 30000: m = m.simplify_quadric_decimation(face_count=30000)
            ax = fig.add_subplot(3, 4, j + 1, projection='3d'); tri = m.vertices[m.faces]
            k = np.clip(m.face_normals @ luz, 0.15, 1)
            ax.add_collection3d(Poly3DCollection(tri, facecolors=np.c_[0.3 + 0.6 * k, 0.45 + 0.5 * k, 0.6 + 0.4 * k, np.ones(len(k))], linewidths=0))
            M = max(m.bounds[1]); ax.set_xlim(0, M); ax.set_ylim(0, M); ax.set_zlim(0, M); ax.view_init(40, -60); ax.set_axis_off()
            ax.set_title(f"{l['arq']}  (x{l['q']})\n{l['x']:.1f} x {l['y']:.1f} x {l['z']:.1f} mm", fontsize=7)
        pdf.savefig(fig); plt.close(fig)
print(len(linhas), 'arquivos;', tot_p, 'peças;', round(tot_g), 'g')
