# Direção dos vídeos da Elite Boardgamers (desde 25/11/2026)

Pedido do editor (25/11/2026): aplicar aos vídeos de divulgação do eliteboardgamers.com.br tudo o que foi aprendido
nos vídeos do agro aprovados no Arcvalion (`Arcvalion_gospel/docs/video/`: `DIRECAO_VIDEO_AGRO.md`,
`PROMPT_VIDEO_AGRO.md`, `PAUTA_AGRO.md`, `TRILHA_AGRO.md` e os roteiros aprovados). Este arquivo diz o que vale igual,
o que muda para jogos de tabuleiro e o que não se aplica.

## 0. Portões (iguais aos do agro)
1. **Pauta pesquisada:** pelo menos 5 candidatas, de 3 eixos ou mais, com nota de 1 a 5 em cada critério. As 3
   melhores vão ao editor com recomendação.
2. **Fatos lidos na fonte**, com link e data. A fonte do próprio site vale para números do próprio site (radar,
   contagem de resenhas). Esses números mudam, então são conferidos de novo no dia do render.
3. **Roteiro na conversa → aprovação expressa.** Nada de voz, imagem ou render antes disso.
4. **Prévia de até 10 s → aprovação → vídeo completo.**
5. **Entrega:** MP4 1080×1080, `capa.jpg` (quadro 0), legenda do Instagram e título do YouTube com 2 alternativas.

## 1. Roteiro
- **Estrutura "Você sabia" em 10 batidas** (`PROMPT_VIDEO_AGRO.md`), cerca de 3,1 palavras/s: 45 a 55 s, 140 a 170
  palavras.
- **Sem frase-fórmula repetida.** Nenhuma das já usadas no agro ("Parece erro. Mas não é.", "E é justamente aí que a
  história fica ainda mais estranha…") nem de vídeo anterior da Elite. Compare com `docs/video/roteiros/` antes de
  entregar.
- **Gancho com número ou consequência concreta para quem joga e compra jogo.** A pergunta é "o que muda pra quem vai
  comprar ou jogar?" antes de "o que o site tem?".
- **Uma voz só** (narrador). Segunda voz só se o formato exigir.
- **Batida 10 = fechamento da marca**, no lugar da conclusão do advogado: "Elite Boardgamers", o que a pessoa ganha
  seguindo e o endereço. Sem promessa que o site não cumpre.
- **Nada inventado.** Opinião só como pergunta. Prêmio, nota e preço sempre com fonte e data, como nas resenhas
  (`PADRAO_EDITORIAL.md`).
- **Datas relativas** ("nesta semana", "sexta") só com a data de publicação combinada. A entrega lista as frases que
  dependem do dia.

## 2. Imagem
**Regra de proporção do agro, igual:** pelo menos **70% do tempo é pintura animada ou tipografia animada**. Print do
site é prova curta: no máximo **3 inserções de até 2,5 s**, de preferência como cartão pequeno sobre a pintura
(o celular entra, o número acende, sai).

### 2.1 Pinturas: mestres em domínio público que pintaram jogos
O hobby tem uma tradição própria na pintura antiga, o que dá à Elite um banco de estilos que o agro não tinha. Sempre
**composição nova feita em código**, nunca cópia do quadro, com o crédito "PINTURA FEITA EM CÓDIGO, À MANEIRA DE …".

| Assunto | Estilo de referência (domínio público) |
|---|---|
| Mesa de jogo, amigos reunidos, abertura e fechamento | Cézanne, "Os Jogadores de Cartas" (1890–95); Jan Steen (festas de família) |
| Trapaça, preço enganoso, "pegadinha" | Caravaggio, "Os Trapaceiros" (c. 1594); Georges de La Tour, "O Trapaceiro com o Ás de Ouros" (c. 1635) |
| Estratégia, duelo, jogo para dois | Sofonisba Anguissola, "A Partida de Xadrez" (1555); Lucas van Leyden, "Os Jogadores de Xadrez" (c. 1508) |
| Família, crianças, jogo leve | Bruegel, "Jogos Infantis" (1560); Chardin, "O Castelo de Cartas" (c. 1737) |
| Casa, estante, luz de fim de tarde | Vermeer (interiores com janela) |
| Loja, mercado, vitrine | Pissarro e Caillebotte (ruas e comércio de Paris) |

**Não usar:** artistas vivos, obras protegidas, estúdios e marcas (Ghibli, Pixar etc.), Portinari e Tarsila. Arte de
caixa de jogo só como foto oficial de divulgação, com crédito, nunca redesenhada.

### 2.2 Gente na pintura
Como no agro: **de costas, de perfil ao longe ou pequena na cena.** Mãos, cartas, dados e peças em close funcionam
muito bem e dispensam rosto. Nada de rosto de frente.

### 2.3 Movimento
Toda pintura se mexe: vela tremendo, dado rolando, carta virando, fumaça, cortina, relógio. Aproximação na abertura,
afastamento no fechamento, corte seco no tempo da fala, uma imagem por item quando a fala lista coisas.

### 2.4 Capa no quadro 0
Igual ao agro: a pintura de abertura viva e pronta no quadro 0, sem fade do preto. Etiqueta pequena com o assunto,
gancho de 2 a 4 palavras gigantes (Inter Black, ~160 px, branco com contorno escuro) e uma linha de reforço. Texto só na
metade de cima, legível a 200 px. Exportar `capa.jpg`.

### 2.5 Identidade fixa da Elite (troca a paleta do agro pela da marca)
- 1080×1080, 30 fps.
- **Legenda** de 1 a 3 palavras, Inter 900 com 54 px, sincronizada palavra por palavra, **preto sobre caixa dourada**
  (o dourado da coroa do selo) no lugar do amarelo do agro. Mesma posição: um pouco abaixo do centro.
- Fundo de cartão e tipografia sobre o grafite do site (`#0f1115` / `#171a20`), texto `#eceff3`, verde de destaque
  `#3ddc84` só para "desconto real" e "vale a pena".
- Títulos em serifa (Newsreader, itálico na palavra-chave), metadados em IBM Plex Mono.
- **Selo "ELITE BOARDGAMERS" com a coroa** no canto inferior (pequeno, como marca d'água) e grande só na cartela final.
- Fonte no rodapé sempre que houver número (mono, ≥ 22 px).
- Nenhuma imagem gerada por IA.

### 2.6 Dados em aquarela
Quando houver série de números (preço ao longo dos meses, ranking), vale o gráfico de caderno do agro (p5.brush,
`Arcvalion_gospel/tools/video/agro-arte/aquarela/`): linha em aquarela, rótulos a lápis, valor escrito à mão.

## 3. Voz e som
- Narrador "Marcio – Viral Hook Narrator" (ElevenLabs `plASsyS7JE6GCAvx9uIc`), `eleven_multilingual_v2` (o `v3` puxou
  sotaque de Portugal). Pausas acima de 0,3 s encurtadas e narrador 8% mais rápido.
- **Toda fala transcrita e comparada com o roteiro**; palavra trocada → nova semente. Atenção à pronúncia de nomes em
  inglês ("Boardgamers", nomes de jogos).
- **Trilha original e instrumental**, sem nome de artista ou música no prompt, conferida com 0 palavras na
  transcrição. O modão do agro não serve aqui. Estilos para alternar (decisão nossa):
  - `taverna`: alaúde, flauta doce e pandeiro leve, clima de mesa de jogo antiga;
  - `bossa-lounge`: violão de bossa, contrabaixo e vassourinha, clima de noite de jogo em casa.
- **Mixagem do agro corrigida em 12/11:** trilha normalizada antes (`loudnorm=I=-30:TP=-6:LRA=11`), volume 1 na
  composição, entrega a −14,5 LUFS e −1,5 dBTP.

## 4. Pauta: eixos da Elite (rodízio)
| Eixo | Assunto |
|---|---|
| A. Preço e compra | Black de Verdade, cupons, alertas, lançamentos com preço |
| B. Confiança | só jogos premiados, nota com fonte, "nada além do que a pesquisa sustenta" |
| C. Escolha | perfis de jogador, jogo para 2, para família, para presente |
| D. Aprender | Como jogar |
| E. Notícias | o que acontece no hobby no Brasil, lançamentos em português |

Nunca dois vídeos seguidos no mesmo eixo. Registre cada vídeo em `docs/video/PAUTAS_USADAS.md` e as cenas em
`docs/video/CENAS_USADAS.md`; nenhuma imagem se repete entre vídeos.

## 5. Entrega
Como no agro, mais: legenda do Instagram (gancho na 1ª linha, números só da fonte, pergunta para comentários, "link na
bio", fontes com data e 8 a 10 hashtags) e título do YouTube (até 100 caracteres, gancho nos primeiros 60, sem caixa
alta inteira).
