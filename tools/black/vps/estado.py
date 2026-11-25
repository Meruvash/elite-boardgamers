#!/usr/bin/env python3
"""Grava black/estado/<robo>.json: a prova de vida pública de cada robô do Radar Black.

Uso (chamado por rodar.sh no fim de cada ciclo):
  estado.py <robo> <inicio_iso> <codigo_saida> <duracao_s> <arquivo_de_log>

O arquivo vai ao R2 junto com a página e fica em eliteboardgamers.com.br/black/estado/<robo>.json. A tarefa de
vigilância do Black (rotina agendada no Claude) lê esses arquivos para saber, sem acesso ao servidor, se cada robô
rodou, quando, se deu erro e quantas ofertas a página tem. Links são tirados das linhas de log (nada de URL de loja
ou de afiliado num arquivo público).
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
URL = re.compile(r"https?://\S+")


def contar_ofertas():
    try:
        html = (RAIZ / "black" / "index.html").read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    return html.count('class="of-btn"')


def main(robo, inicio, codigo, duracao, log):
    try:
        linhas = Path(log).read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        linhas = []
    cauda = [URL.sub("<link>", l)[:300] for l in linhas if l.strip()][-15:]
    estado = {
        "robo": robo,
        "inicio": inicio,
        "fim": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "duracao_s": int(duracao),
        "codigo_saida": int(codigo),
        "ok": int(codigo) == 0,
        "bloqueios": sum(1 for l in linhas if re.search(r"(?i)bloquead|\b(401|403|429)\b", l)),
        "cartoes_na_pagina": contar_ofertas(),
        "log": cauda,
    }
    destino = RAIZ / "black" / "estado"
    destino.mkdir(parents=True, exist_ok=True)
    (destino / f"{robo}.json").write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    main(*sys.argv[1:])
