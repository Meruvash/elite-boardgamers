# Pesquisa de procura: qual jogo está sendo mais buscado (26/11/2026)

Pedido do editor: "Pesquisa um jogo que está sendo bastante procurado."

## Fontes e o que deu
- **BoardGameGeek (API "hot")** e **Ludopedia:** recusam acesso automatizado (HTTP 401 e 403). Não trocamos o user-agent.
- **Virlo** (vídeo curto): o acervo não tem vídeos de jogo de tabuleiro em português desde 01/10; a busca voltou futebol.
- **Google Trends Brasil, últimos 3 meses** (pytrends). Volume de nicho é baixo e o Trends zera o que fica abaixo do
  limite; por isso a comparação é entre termos completos, nunca o nome solto:
  - "Flip 7" era o celular Galaxy Z Flip 7; "Azul jogo" era Baleia Azul e jogo de jantar; "Dixit" puxa "Dixit Dominus";
    "Catan" puxa um político. Esses termos soltos foram descartados.
  - Média das últimas 2 semanas × 2 semanas de 3 meses atrás (escala 0–100 dentro de cada grupo):

| Termo | Grupo 1 | Grupo 2 |
|---|---|---|
| azul jogo de tabuleiro | 46 (antes 0) | 5 (antes 0) |
| coup jogo de cartas / jogo coup | 42 (antes 0) | 31 (antes 0) |
| dixit jogo | — | 32 (antes 0) |
| ticket to ride | — | 30 (antes 9) |
| perfil jogo de tabuleiro | 22 (antes 0) | — |
| catan jogo de tabuleiro | 22 (antes 0) | — |
| combate jogo de tabuleiro | 3 (antes 0) | — |

  - Em "jogo de cartas", **"jogo de cartas coup" aparece entre as buscas em alta** (+40%).
  - "Perfil" tem pico sazonal em dezembro (2025: 43 em dez., 0 em nov.): é presente de Natal.
- **Autocomplete do YouTube** ("como jogar …"): aparecem azul, catan, ticket to ride, kingdomino, dixit e coup.

## Conclusão
Todos sobem com a chegada do Natal. O sinal mais consistente nas três medições é **Coup** (alto nos dois grupos, em alta
em "jogo de cartas", no autocomplete e com guia no site). Depois, **Ticket to Ride** (único com base anterior e alta de ~3×)
e **Dixit**. Azul continua forte em volume, mas sem alta própria.

## Refeita a pedido do editor: só board game de hobby, só Google (26/11/2026)
"Esses jogos aí são muito merda. Eu quero jogo de board game de verdade… autocomplete do Google, Google Trends."

1. **Autocomplete do Google** (pt-BR): sementes do nicho ("board game", "melhores board games", "board game devir",
   "board game galápagos"…) e varredura por letra ("board game a…z", "boardgame a…z", "jogo de tabuleiro a…z"). Saíram
   títulos de hobby como Nemesis, Everdell, Heat, Root, Valheim, Zombicide, Arkham Horror, Gloomhaven, SETI, Mistborn,
   Brass, Agricola, Scythe e Dead by Daylight.
2. **Google Trends Brasil, 12 meses, semanal**, 28 títulos em lotes de 4 com a mesma âncora (Terraforming Mars), para
   ficarem na mesma escala. Volume = média das últimas 4 semanas ÷ âncora; crescimento = últimas 4 semanas × as 4 semanas de
   3 meses atrás.

| Jogo | Volume (× âncora) | Últ. 4 sem. × 3 meses atrás | Observação |
|---|---|---|---|
| Catan | 26,1 | 52 × 49 | contaminado (deputado João Henrique Catan) |
| Zombicide | 8,7 | 59 × 70 | nome único; em queda leve |
| Carcassonne | 4,8 | 10 × 14 | também é cidade |
| **Everdell** | 4,6 | 57 × 79 | nome único; expansões novas em alta (Emerland, Newleaf) |
| Arkham Horror | 4,2 | 28 × 27 | estável |
| Gloomhaven | 3,5 | 41 × 58 | inclui o jogo digital |
| Spirit Island | 3,1 | 52 × 45 | inflado por "spirit island gpo" (Roblox) e pelo digital |
| Frosthaven | 3,0 | 46 × 0 | puxado pela versão digital (steam, pc, ps5) |
| **Ark Nova** | 2,0 | **35 × 11 (3,3×)** | nome único; o maior crescimento real; no YouTube, "ark nova como jogar" é a 2ª sugestão |

Termos com "board game" no fim (Nemesis, Heat, Root, SETI…) saem com volume quase nulo porque o público busca o nome
solto, que é ambíguo. Eles não entram na comparação.

**Conclusão:** Ark Nova é o que mais cresce (3,3× em 3 meses) com nome sem ambiguidade e "como jogar" no autocomplete do
YouTube. Everdell e Zombicide têm mais volume, com expansões puxando a busca.
