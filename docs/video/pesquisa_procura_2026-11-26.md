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
