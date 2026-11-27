# Pedido de liberação do robô do Black de Verdade (27/11/2026)

Mensagem para as lojas que passaram a bloquear o robô EliteBoardgamers depois do erro de 20/11/2026 (o robô
educado visitou as lojas a cada minuto, em vez de a cada 3 horas). Mandar pelo Instagram ou pelo e-mail de contato
de cada loja. Trocar [LOJA] pelo nome.

---

Olá, equipe da [LOJA]! Aqui é da Elite Boardgamers (eliteboardgamers.com.br).

Primeiro, um pedido de desculpas. Nosso radar de promoções, o Black de Verdade, mostra as ofertas de jogos de
tabuleiro das lojas brasileiras com link direto para a página do produto. No dia 20/11, um erro nosso fez o robô
visitar o site de vocês com muito mais frequência do que deveria, e o bloqueio que vocês aplicaram foi a reação
certa. O erro já foi corrigido: o robô volta a ler cada loja no máximo a cada 3 horas, com 6 segundos entre uma
página e outra e no máximo 60 páginas por dia.

Hoje a [LOJA] está aparecendo muito pouco no radar, justamente na semana da Black Friday, e a gente gostaria de
voltar a mandar clientes para vocês. Há dois jeitos, o que for mais confortável:

1. Liberar o robô no firewall: ele se identifica como "EliteBoardgamers/1.0
   (+https://eliteboardgamers.com.br/black/robo/)" e respeita o robots.txt de vocês.
2. Ou mandar o link do feed de produtos (o mesmo do Google Shopping). Aí lemos um arquivo só, uma vez por dia,
   todos os jogos de vocês entram no radar e o site de vocês não recebe nenhuma visita do robô.

O que ele faz e o que respeita está em https://eliteboardgamers.com.br/black/robo/. Se preferirem ficar de fora,
é só dizer.

Obrigado, e boas vendas na Black!
Elite Boardgamers

---

## Lojas que bloquearam (estado de 23/11/2026)

Atualização de 27/11/2026: Alquimistas dos Jogos, Place Games, Omniverse, TabuLoja, TabuleRIO, Taverna Real, PlayEasy,
Animus Ludere, Leão Livros, Cangaia Jogos, Meca dos Jogos, Espaço ARCS e Frodos BG já liberaram (o robô voltou a ler a
página delas). A lista que vale é tools/black/lojas_pausadas.txt, que se atualiza sozinha.

Masmorra, Alquimistas dos Jogos, Meeple BR, Galápagos (mundogalapagos), Dalaran, Taverna Real, Tschüss, Omniverse,
PlayEasy, Place Games, TabuleRIO, TabuLoja, Toca do Tabuleiro, Animus Ludere, Leão Livros, Cangaia Jogos, Meca dos
Jogos, Espaço ARCS, Frodos BG, Panda Board Games, Space Board Games, Expresso Board Games, Happy Nerd, Elfos & Cia,
Javali Jogos, Jogasampa, Border Jogos, Borba Games, Brinkz, Brinka Shop, Board Game Barato, Boargames, Immerstore,
Livtoys, Mosaico, Pouso Cultural, Reunion Jogos, ShopDG, Tio Gêra, York Jogos, Ludocafé, Adoleta Jogos, Game Hives,
Joy Joy Café, Vem pra Mesa.

Quem responder com o feed: o link entra em conteudo/black/feeds.json (no servidor) e a loja volta no ciclo seguinte.
Quem liberar o robô: não precisa mudar nada; o robô tenta de novo sozinho depois do descanso de 48 horas.
