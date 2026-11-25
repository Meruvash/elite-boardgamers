#!/usr/bin/env bash
# Um ciclo de um robô do Radar Black no servidor da Oracle Cloud (substitui tools/black/ciclo.sh, que rodava no GitHub
# Actions em laço e fazia um commit por ciclo; o repositório antigo foi desativado pelo GitHub em 24/11/2026).
#
# Aqui não há laço nem commit: o systemd chama este script no horário (tools/black/vps/systemd/), ele roda o robô uma
# vez, refaz a página e envia black/ e img/black/ para o bucket R2, de onde o site serve /black/.
# Os dados (conteudo/black/*.json) ficam só no disco do servidor. O git é usado apenas para ler o código novo.
#
# Uso: rodar.sh <normal|educado|ml|alertas>
set -u
# o corpo fica entre chaves para o bash ler tudo antes de executar: o systemd pode atualizar este arquivo
# (git checkout de tools/) enquanto um ciclo longo do educado ainda roda
{
ROBO="$1"
BASE="${ELITE_DIR:-/opt/elite/site}"
cd "$BASE" || exit 1
export PATH="/opt/elite/venv/bin:$PATH"

# um robô por vez em cada tipo, e nunca dois publicando ao mesmo tempo
exec 9>"/tmp/elite-radar-$ROBO.lock"
flock -n 9 || { echo "o robô $ROBO ainda está rodando; este ciclo fica para a próxima"; exit 0; }

LOG="/tmp/elite-radar-$ROBO.log"
INICIO=$(date -u +%Y-%m-%dT%H:%M:%S+00:00); T0=$SECONDS

# prova de vida pública (black/estado/<robo>.json), lida pela vigilância do Black no Claude; nunca impede o ciclo
estado() { python3 tools/black/vps/estado.py "$ROBO" "$INICIO" "$1" "$((SECONDS - T0))" "$LOG" || true; }

if [ "$ROBO" = "alertas" ]; then
  python3 tools/black/alertas.py --fila > >(tee "$LOG") 2>&1; RC=$?
  estado "$RC"
  python3 tools/black/vps/publicar_r2.py black/estado || true
  exit $RC
fi

# cópia dos dados antes do ciclo: JSON que o robô deixar quebrado volta a esta versão
COPIA="/opt/elite/copia/$ROBO"; rm -rf "$COPIA"; mkdir -p "$COPIA"; cp -a conteudo/black/. "$COPIA/"

{ case "$ROBO" in
  normal) timeout --kill-after=60 25m python3 tools/black/robo_normal.py ;;
  ml) timeout --kill-after=60 25m python3 tools/black/robo_ml.py ;;
  educado)
    acao=coletar
    # varredura completa do sitemap no domingo à tarde (UTC 14h a 16h)
    if [ "$(date -u +%u)" = "7" ] && [ "$(date -u +%H)" -ge 14 ] && [ "$(date -u +%H)" -le 16 ]; then acao=varrer; fi
    timeout --kill-after=60 4h python3 tools/black/robo_educado.py "$acao" ;;
  *) echo "robô desconhecido: $ROBO"; exit 1 ;;
esac; } > >(tee "$LOG") 2>&1
RC=$?
[ $RC -ne 0 ] && echo "o robô terminou com erro ou no prazo ($RC); publica o que já leu"

date -u +%Y-%m-%dT%H:%M:%S+00:00 > "conteudo/black/batimento_$ROBO.txt"
for f in conteudo/black/*.json; do
  python3 -c "import json,sys; json.load(open(sys.argv[1], encoding='utf-8'))" "$f" 2>/dev/null \
    || { echo "JSON quebrado, volta a cópia: $f"; cp -a "$COPIA/$(basename "$f")" "$f" 2>/dev/null || true; }
done

# publicação com um trava única: dois robôs não refazem a página nem enviam ao mesmo tempo
exec 8>/tmp/elite-radar-publicar.lock
flock 8
python3 tools/black/radar.py pagina >/dev/null || { echo "não consegui refazer a página"; RC=97; estado "$RC"; python3 tools/black/vps/publicar_r2.py black/estado; exit 1; }
estado "$RC"

# link de afiliado de terceiros nunca vai ao ar (pedido do usuário em 05/11/2026)
if ! python3 -c "import sys,pathlib; sys.path.insert(0,'tools'); import verificar_site as v; \
p=[str(f) for f in list(pathlib.Path('conteudo/black').rglob('*.json'))+list(pathlib.Path('black').rglob('*.*')) if f.is_file() and v.AFILIADO_PUBLICO.search(f.read_text(encoding='utf-8',errors='ignore'))]; \
print('\n'.join(p)); sys.exit(1 if p else 0)"; then
  echo "link de afiliado de terceiros nos dados: publicação suspensa neste ciclo"; RC=98; estado "$RC"
  python3 tools/black/vps/publicar_r2.py black/estado; exit 1
fi

python3 tools/black/vps/publicar_r2.py black img/black
exit $?
}
