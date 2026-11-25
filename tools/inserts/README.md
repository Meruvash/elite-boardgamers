# insertgen: inserts de caixa em STL, com medidas exatas e validação

Gerador paramétrico de organizadores (inserts) para caixas de jogo. Você descreve a caixa, as cartas, os sleeves e
o que vai deitado por cima (tabuleiro, fichas, manual). O `gerar.py` monta as peças e só entrega STL que passou em
todas as checagens:

- **Malha fechada e orientada**: toda aresta tem par, o volume é positivo e não há triângulo degenerado. A checagem é
  feita no sólido e de novo no arquivo gravado, relido do disco.
- **Medida exata**: o tamanho gerado precisa bater com o declarado com tolerância de 0,01 mm. A peça fica apoiada em
  z = 0 e precisa caber na mesa da impressora (256 x 256 mm por padrão).
- **Parede mínima**: a checagem procura, fatia por fatia, qualquer parede mais fina que `parede_min` (1,2 mm). Foi ela
  que pegou o primeiro rebaixo de tampa, que estava com 1,0 mm.
- **Cartas cabem**: cada maço luvado é modelado como um bloco (sleeve x quantidade x espessura). Esse bloco não pode
  tocar o plástico nem passar da borda da bandeja.
- **Montagem**: nenhuma peça pode sair da caixa nem se sobrepor a outra. Peça empilhada precisa de pelo menos 60% da
  base apoiada. O volume do tabuleiro e da camada plana tem que ficar livre até a tampa.

Se qualquer checagem falhar, o comando termina com código 1 e lista o problema.

```
pip install -r tools/inserts/requirements.txt
python3 tools/inserts/gerar.py                    # gera tools/inserts/saida/robinson-crusoe-ce/
python3 -m unittest discover -s tools/inserts/tests -t tools/inserts
python3 -I tools/inserts/analisar_original.py insert.zip   # diagnostica um insert pronto
```

## Robinson Crusoe — Edição de Colecionador, com sleeves Bucaneiros

### O problema no insert original

O zip enviado é o insert **js500** (Printables 953093) mais o remix com Mistérios (Mystery Tales). O `analisar_original.py`
mede os poços de carta direto nos STLs:

| Bandeja original | Poço | Carta grande em Bucaneiros Padrão Euro | Resultado |
|---|---|---|---|
| `obj_5_cards-events-and-wreckage` | 93,0 mm | 95,0 mm (+1 de folga = 96) | **não cabe: faltam 3,0 mm** |
| `obj_6_Mystery Tales Cards` | 94,8 mm | 95,0 mm | **não cabe: faltam 1,2 mm** |
| `obj_8_cards-inventions...` (pequenas) | 74,0 mm | 71,0 mm (Mini Euro) | cabe |
| `obj_9_cards-beasts` (pequenas) | 50,0 mm | 47,5 mm | cabe |

O próprio autor do js500 diz que o projeto é para o **playmat de neoprene** e que o tabuleiro de papelão só cabe se a
tampa ficar levantada. Por isso o original também não tem espaço para o tabuleiro.

### A solução atual (versão 3): só o jogo base

Desde 25/11/2026 o projeto é só o jogo base da Edição de Colecionador: você não tem Mistérios, Livro de Aventuras,
Treasure Chest, torre nem miniaturas. Isso fica no JSON em `"extras": {"tem": false}`. Trocando para `true`, o gerador
volta para a versão 2, que tem 104 mm de altura. Com as estimativas atuais da camada plana, a versão 2 **não fecha a
tampa**; ela só serve se a caixa e a pilha medidas permitirem.

- **Altura**: o insert tem **78 mm**, em dois níveis de 52 + 26 mm. Sobram ~56 mm para a camada plana numa caixa de
  134 mm. O gerador também exige que feche no **pior caso de 127 mm** de altura interna: sobram 6 mm além dos 43 mm
  estimados para tabuleiro + fichas + manual + 2 cadernos.
- **Fundo**: 318,4 x 318,4 mm, o mesmo tamanho comprovado pelo js500.
- **Cartas** (tamanho oficial da Portal, 58 x 88 e 44 x 68), com sleeve Bucaneiros PADRÃO e MINI EURO:
  - grandes deitadas em bandejas que vão para a mesa (poço de 68,4 x 93,4 mm):
    - Eventos, com compra e descarte na mesma peça;
    - Mistério;
    - 3 Aventuras;
    - Especiais;
    - 3 descartes vazios;
  - pequenas em pé numa bandeja com 2 divisórias soltas.
- **Componentes**: as 6 bandejas originais de componentes ficam lado a lado no fundo.
  - O `obj_19_animals` é a bandeja removível que **encaixa dentro** do `obj_12`, como no js500.
  - Não imprima as dos Mistérios nem a de miniaturas: `obj_3`, `obj_17` e `obj_20`.
- **Caixas com tampa** completam o topo. A de 122,8 x 246 mm fica livre para os extras no futuro.

![montagem](saida/robinson-crusoe-ce/montagem.png)

### Antes de imprimir: meça 5 números

Ninguém publicou estes dados. Os valores em `projetos/robinson-crusoe-ce.json` estão marcados `"status": "estimado"`.

1. **Caixa por dentro**: largura, profundidade e altura útil com a tampa fechada. O padrão é 320 x 320 x 134. Pela
   Portal a caixa tem 33 x 33 x 14 cm por fora, e o insert original ocupa 318,4 mm.
2. **Camada plana**: espessura do tabuleiro dobrado + fichas de cenário + fichas de personagem + manual. O padrão é
   28 mm, e cabem até 30 mm se a altura interna for 134.
3. **Sleeve Bucaneiros**: largura e altura por fora, medidas num sleeve com carta dentro. Preencha `"medido"` em
   `dados/sleeves_bucaneiros.json`, porque a Bucaneiros só informa o tamanho da carta.
4. **Carta**: tamanho e espessura. Meça 10 cartas empilhadas e divida por 10.
5. **Quantidade de cartas** de cada maço, sobretudo as dos Mistérios: as fontes divergem sobre quais são pequenas.

Depois rode `gerar.py` de novo. Se algo deixar de caber, ele diz o que e por quanto.

### O que imprimir

- **Antes de tudo:** imprima as peças de `saida/teste-encaixe/` (`python3 tools/inserts/gerar_teste.py`). São um poço
  deitado, uma bandeja em pé, um poço de carta pequena e uma tampa, com as mesmas folgas do insert. Confira o encaixe
  com o seu sleeve e ajuste `Params` se precisar.
- Os **19 STLs** de `saida/robinson-crusoe-ce/`. A `divisoria-pequenas` sai em **2 cópias**; o resto, 1 de cada (as
  quantidades estão no `relatorio.json`).
- As 7 bandejas originais de componentes: `obj_11` a `obj_16` e `obj_19` (que vai dentro do `obj_12`).
- PLA ou PETG, camada de 0,2 mm, sem suporte, com a boca para cima. As bandejas em pé têm parede de 1,2 mm: use 3
  perímetros.

## Estrutura

```
insertgen/geom.py      primitivas (caixa arredondada, cavidade em concha, entalhe de dedo)
insertgen/cartas.py    sleeves (catálogo Bucaneiros), carta luvada, altura do maço
insertgen/pecas.py     bandeja de baralhos, bandeja de fichas com tampa, calço
insertgen/validar.py   malha, medidas, parede fina, conteúdo cabe, montagem
insertgen/previa.py    planta, corte e vista 3D (PNG)
insertgen/stl.py       STL binário só com numpy
projetos/              um arquivo .py (layout) + .json (medidas) por jogo
dados/                 catálogo de sleeves
```

Para outro jogo, copie `projetos/robinson_crusoe_ce.py` e o JSON dele, troque as medidas e o layout e aponte o
`gerar.py` para o novo projeto.
