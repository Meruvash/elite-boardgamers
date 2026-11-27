#!/usr/bin/env bash
# Configura as chaves do Mercado Livre no servidor do Radar Black e destrava a atualização de código.
# Feito para quem não usa terminal: um comando só, que pergunta as duas chaves e faz o resto.
# Uso (dentro do servidor):
#   curl -fsSL https://raw.githubusercontent.com/Meruvash/elite-boardgamers/main/tools/black/vps/configurar_ml.sh -o /tmp/ml.sh && sudo bash /tmp/ml.sh
set -u
ENV=/etc/elite-radar.env
SITE=/opt/elite/site

[ "$(id -u)" = 0 ] || { echo "Rode com sudo: sudo bash /tmp/ml.sh"; exit 1; }
[ -f "$ENV" ] || { echo "Não achei $ENV. O radar foi instalado neste servidor?"; exit 1; }

echo
echo "== 1/3 Chaves do Mercado Livre"
echo "Pegue no site: https://developers.mercadolivre.com.br/devcenter (a sua aplicação)."
read -r -p "Cole o App ID e aperte Enter: " ID < /dev/tty
read -r -s -p "Cole a Secret Key e aperte Enter (ela não aparece na tela): " SEG < /dev/tty
echo
ID=$(printf '%s' "$ID" | tr -d '[:space:]'); SEG=$(printf '%s' "$SEG" | tr -d '[:space:]')
if [ -z "$ID" ] || [ -z "$SEG" ]; then echo "Alguma chave veio vazia; nada foi mudado."; exit 1; fi

# testa antes de gravar
COD=$(curl -s -o /dev/null -w '%{http_code}' -X POST https://api.mercadolibre.com/oauth/token \
  -d grant_type=client_credentials --data-urlencode "client_id=$ID" --data-urlencode "client_secret=$SEG")
if [ "$COD" != 200 ]; then
  echo "O Mercado Livre recusou essas chaves (resposta $COD). Confira se copiou o App ID e a Secret Key certos."
  exit 1
fi
cp -a "$ENV" "$ENV.bak"
grep -v -E '^(ML_CLIENT_ID|ML_CLIENT_SECRET)=' "$ENV.bak" > "$ENV.novo"
printf 'ML_CLIENT_ID=%s\nML_CLIENT_SECRET=%s\n' "$ID" "$SEG" >> "$ENV.novo"
mv "$ENV.novo" "$ENV"; chown root:elite "$ENV"; chmod 640 "$ENV"
echo "ok: chaves aceitas pelo Mercado Livre e gravadas."

echo
echo "== 2/3 Atualização do código dos robôs"
git config --system --add safe.directory "$SITE" 2>/dev/null || true
chown -R elite:elite "$SITE"
if sudo -u elite git -C "$SITE" fetch -q --depth 1 origin main 2>/tmp/ml-git.txt \
   && sudo -u elite git -C "$SITE" checkout -q origin/main -- tools 2>>/tmp/ml-git.txt; then
  echo "ok: código novo baixado."
  cp "$SITE"/tools/black/vps/systemd/* /etc/systemd/system/ && systemctl daemon-reload
else
  echo "A atualização falhou. Mande este erro para o Claude:"; cat /tmp/ml-git.txt
fi

echo
echo "== 3/3 Teste do robô do Mercado Livre (pode levar alguns minutos)"
systemctl start elite-radar@ml
journalctl -u elite-radar@ml -n 8 --no-pager | grep -E "Mercado Livre|R2:|erro|Error" || true
echo
echo "Pronto. Se apareceu 'ok Mercado Livre', está funcionando."
