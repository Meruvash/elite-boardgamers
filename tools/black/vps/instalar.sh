#!/usr/bin/env bash
# Instala os robôs do Radar Black num servidor Ubuntu (Oracle Cloud, plano gratuito). Rode como root, uma vez:
#   curl -fsSL https://raw.githubusercontent.com/Meruvash/elite-boardgamers/main/tools/black/vps/instalar.sh | sudo bash
# Depois preencha /etc/elite-radar.env e ligue os timers (o fim do script diz como). Rodar de novo é seguro.
set -euo pipefail
REPO="https://github.com/Meruvash/elite-boardgamers"

apt-get update -q
apt-get install -y -q git python3 python3-venv python3-dev build-essential libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev

id elite >/dev/null 2>&1 || useradd --system --create-home --home-dir /opt/elite --shell /usr/sbin/nologin elite
mkdir -p /opt/elite/copia

if [ ! -d /opt/elite/site/.git ]; then
  # o site inteiro vem junto porque a página do Radar usa o layout e os dados de conteudo/black como ponto de partida
  git clone --depth 1 "$REPO" /opt/elite/site
fi

[ -d /opt/elite/venv ] || python3 -m venv /opt/elite/venv
/opt/elite/venv/bin/pip install -q --upgrade pip
/opt/elite/venv/bin/pip install -q requests Pillow beautifulsoup4 lxml feedparser price-parser protego cryptography boto3

chown -R elite:elite /opt/elite
chmod +x /opt/elite/site/tools/black/vps/rodar.sh
sudo -u elite git -C /opt/elite/site config user.name "Radar Black (servidor)"
sudo -u elite git -C /opt/elite/site config user.email "radar@eliteboardgamers.com.br"

if [ ! -f /etc/elite-radar.env ]; then
  cat > /etc/elite-radar.env <<'EOF'
# Chaves dos robôs do Radar Black. Só root e o usuário elite leem este arquivo.
# Preencha o que você usa; robô sem a chave dele pula essa parte e segue.

# Cloudflare R2 (obrigatório: é por aqui que a página /black/ chega ao site)
R2_ACCOUNT_ID=0b88cc2d6b58c936265686f078d9969f
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET=elite-radar

# Mercado Livre (API oficial)
ML_CLIENT_ID=
ML_CLIENT_SECRET=

# Keepa (Amazon)
KEEPA_KEY=

# Telegram (canal de alertas e leitura de canais públicos)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CANAL=
TELEGRAM_API_ID=
TELEGRAM_API_HASH=
TELEGRAM_SESSAO=

# Bluesky e ntfy
BSKY_USUARIO=
BSKY_SENHA_APP=
NTFY_TOKEN=
EOF
fi
chown root:elite /etc/elite-radar.env
chmod 640 /etc/elite-radar.env

cp /opt/elite/site/tools/black/vps/systemd/* /etc/systemd/system/
systemctl daemon-reload

cat <<'EOF'

Instalado. Falta:
  1. sudo nano /etc/elite-radar.env      (cole as chaves; sem as do R2 a página não chega ao site)
  2. Teste um ciclo:   sudo systemctl start elite-radar@normal && journalctl -u elite-radar@normal -n 30
  3. Ligue a agenda:   sudo systemctl enable --now elite-radar-normal.timer elite-radar-ml.timer elite-radar-educado.timer elite-radar-alertas.timer
  4. Confira:          systemctl list-timers 'elite-radar*'
EOF
