# Radar Black no Railway

Segundo servidor dos robôs (27/11/2026), ao lado do da Oracle. Os dois publicam no mesmo bucket R2: a Oracle na raiz,
o Railway em `v2/`. O site (tools/black/radar_pages.js) mostra, arquivo por arquivo, a cópia mais nova; se um servidor
parar, o outro segue no ar sozinho. Página com menos de 30 ofertas não é publicada pelo Railway.

- Configuração: `railway.json` (raiz) e `tools/black/railway/Dockerfile`.
- Agendador: `agendador.py` (normal e ml a cada 30 min, educado a cada 3 h; alertas só na Oracle).
- Volume: montar em `/data` (dados dos robôs entre um ciclo e outro).
- Lojas que bloquearam: `tools/black/lojas_pausadas.txt` (nenhum servidor visita até a loja liberar).

## Variáveis (aba Variables do serviço)

| Nome | Valor |
|---|---|
| R2_ACCOUNT_ID | 0b88cc2d6b58c936265686f078d9969f |
| R2_ACCESS_KEY_ID | chave do R2 (Cloudflare → R2 → Manage API tokens) |
| R2_SECRET_ACCESS_KEY | segredo do R2 |
| R2_BUCKET | elite-radar |
| ML_CLIENT_ID | App ID do Mercado Livre |
| ML_CLIENT_SECRET | Secret Key do Mercado Livre |
| KEEPA_KEY | (opcional) chave do Keepa |

Não ponha NTFY_TOKEN nem TELEGRAM_BOT_TOKEN aqui: os alertas saem só da Oracle, para não chegarem em dobro.
