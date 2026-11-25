# Radar Black no servidor da Oracle Cloud

Desde 24/11/2026 os robôs do Radar Black não rodam mais no GitHub Actions. Lá eles rodavam em laço quase 24 horas por
dia e faziam um commit a cada ciclo (cerca de 700 por semana); o repositório antigo, Meruvash/Golden-Geek, foi
desativado pelo GitHub por violação dos termos de uso, provavelmente por isso. Os workflows antigos estão em
`docs/workflows-desligados/` e não devem ser religados.

## Como funciona agora

```
servidor Oracle (systemd)            Cloudflare R2 (bucket elite-radar)        site (Cloudflare Pages)
  robô normal  a cada 30 min  ─┐                                               /black/ e /img/black/ passam por
  robô ml      a cada 30 min   ├─► refaz black/ e img/black ─► envia só o ─►    functions/, que lê do R2; sem o
  robô educado a cada 3 h     ─┘   (dados ficam no disco)      que mudou        bucket, mostra a cópia do repositório
  alertas      a cada 15 min
```

- Nenhum robô faz commit. O repositório guarda só código e conteúdo editorial.
- O servidor lê o código novo de `tools/` antes de cada ciclo (`git fetch` no repositório público, sem senha).
- Os dados (`conteudo/black/*.json`) vivem só no servidor, em `/opt/elite/site/conteudo/black/`.
- Arquivos: `rodar.sh` (um ciclo), `publicar_r2.py` (envio ao R2), `systemd/` (agenda), `instalar.sh` (instalação).

## Passo a passo (uma vez)

### 1. Cloudflare R2 (conta Andersonrgk, a do domínio)
1. dash.cloudflare.com → R2 Object Storage → ativar (o plano gratuito vai até 10 GB; o Cloudflare pede um cartão).
2. Create bucket → nome `elite-radar`.
3. R2 → Manage API tokens → Create API token → permissão **Object Read & Write**, só no bucket `elite-radar`.
   Guarde o **Access Key ID** e o **Secret Access Key** (aparecem uma vez só).
4. Ligar o bucket ao site: Workers & Pages → eliteboardgamers → Settings → Bindings → Add → R2 bucket,
   nome da variável **RADAR**, bucket `elite-radar`, em Production. (Ou peça ao Claude, que faz pela API.)

### 2. Servidor na Oracle Cloud
1. Crie a conta em cloud.oracle.com (plano Always Free; pede cartão, mas não cobra o que é gratuito).
2. Compute → Instances → Create instance:
   - Image: **Canonical Ubuntu 24.04**
   - Shape: **VM.Standard.A1.Flex** (Ampere), 1 OCPU e 6 GB de memória bastam
   - Baixe a chave SSH que a Oracle gera (Save private key).
3. Quando a instância estiver "Running", copie o IP público e entre:
   `ssh -i chave.key ubuntu@IP`
4. Instale:
   `curl -fsSL https://raw.githubusercontent.com/Meruvash/elite-boardgamers/main/tools/black/vps/instalar.sh | sudo bash`
5. Cole as chaves: `sudo nano /etc/elite-radar.env` (R2 do passo 1, Mercado Livre, Keepa, Telegram, Bluesky, ntfy:
   as mesmas que estavam nos segredos do repositório antigo).
6. Teste um ciclo: `sudo systemctl start elite-radar@normal && journalctl -u elite-radar@normal -n 30`
   A última linha deve ser `R2: N arquivo(s) enviado(s)`. Abra eliteboardgamers.com.br/black/ e confira a hora.
7. Ligue a agenda:
   `sudo systemctl enable --now elite-radar-normal.timer elite-radar-ml.timer elite-radar-educado.timer elite-radar-alertas.timer`

## Dia a dia

- Ver a agenda: `systemctl list-timers 'elite-radar*'`
- Ver o último ciclo de um robô: `journalctl -u elite-radar@ml -n 50`
- Pausar tudo: `sudo systemctl stop 'elite-radar-*.timer'`
- Mudar a frequência: edite `tools/black/vps/systemd/*.timer` no repositório e, no servidor,
  `sudo cp /opt/elite/site/tools/black/vps/systemd/* /etc/systemd/system/ && sudo systemctl daemon-reload`

## Saúde dos robôs (visível de fora do servidor)

Desde 25/11/2026 cada ciclo grava `black/estado/<robo>.json` (início, fim, duração, código de saída, quantos cartões a
página tem, quantas linhas de bloqueio e as últimas linhas do log, sem links) e envia ao R2 junto com a página:

- https://eliteboardgamers.com.br/black/estado/normal.json (e `ml.json`, `educado.json`, `alertas.json`)

A tarefa agendada "Elite: vigilância do Black de Verdade" (no Claude, de 2 em 2 horas) lê esses arquivos e a hora
"Atualizado em" da página. Se algum robô parar ou der erro repetido, ela corrige o código em `tools/black/` e publica
na main; o servidor pega o código novo no ciclo seguinte (o `git fetch` de `tools/` antes de cada ciclo). O que exige
mexer no próprio servidor (chaves, systemd, disco) ela não alcança e avisa no celular.

## Cuidados (para não repetir o bloqueio)

- Não volte a publicar dados do Radar por commit, nem rodar os robôs no GitHub Actions.
- Mantenha os intervalos: em 20/11/2026 um erro fez o robô educado visitar as lojas a cada minuto e 27 lojas e o
  Compara Jogos bloquearam o robô. O `flock` em `rodar.sh` impede dois ciclos do mesmo robô ao mesmo tempo.
- Fora da Black Friday, dá para espaçar o normal e o ml para 1 hora.
