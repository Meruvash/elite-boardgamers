#!/usr/bin/env python3
"""Agendador do Radar Black no Railway (pedido do usuário em 27/11/2026: um segundo servidor, que cobre o da Oracle).

Roda o tempo todo e chama tools/black/vps/rodar.sh nos mesmos intervalos do servidor da Oracle. Os dados ficam no
volume do Railway (/data); a página vai ao R2 com o prefixo v2/ e o site mostra a cópia mais nova entre os dois
servidores (tools/black/radar_pages.js). Código novo chega sozinho: o Railway refaz o serviço a cada push na main.

O robô de alertas não roda aqui (o da Oracle já manda; dois mandariam o mesmo aviso duas vezes).
"""
import os
import re
import urllib.request
from urllib.parse import urlparse
import shutil
import subprocess
import time
from pathlib import Path

APP = Path(__file__).resolve().parents[3]
DADOS = Path(os.environ.get("DADOS", "/data"))
# robô: intervalo em segundos (iguais aos timers do systemd em tools/black/vps/systemd/)
AGENDA = {"normal": 30 * 60, "ml": 30 * 60, "educado": 3 * 60 * 60}
PASTAS = {"conteudo/black": "black-dados", "black": "black-site", "img/black": "black-img"}


def preparar():
    """Liga as pastas de dados ao volume; na primeira vez, copia o que veio no repositório."""
    DADOS.mkdir(parents=True, exist_ok=True)
    for rel, nome in PASTAS.items():
        destino, origem = DADOS / nome, APP / rel
        if not destino.exists():
            shutil.copytree(origem, destino) if origem.is_dir() else destino.mkdir(parents=True)
            print(f"volume: {rel} copiado do repositório")
        if origem.is_symlink():
            continue
        if origem.exists():
            shutil.rmtree(origem)
        origem.parent.mkdir(parents=True, exist_ok=True)
        origem.symlink_to(destino)


def liberadas():
    """Lojas que o servidor da Oracle voltou a ler direto (cartão "página da loja" no site): já liberaram o robô.
    Vão para conteudo/black/lojas_liberadas.txt e saem da lista de pausa (tools/black/lojas.py)."""
    try:
        req = urllib.request.Request("https://eliteboardgamers.com.br/black/",
                                     headers={"User-Agent": "EliteBoardgamers/1.0 (+https://eliteboardgamers.com.br/black/robo/)"})
        html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    except Exception as ex:  # noqa: BLE001
        print(f"aviso: não li a página para ver lojas liberadas ({ex})", flush=True)
        return
    doms = set()
    for cartao in html.split('class="of-img"')[1:]:
        if "página da loja" in cartao:
            m = re.search(r'class="of-btn" href="([^"]+)"', cartao)
            if m:
                doms.add(urlparse(m.group(1)).netloc.lower())
    arq = APP / "conteudo/black/lojas_liberadas.txt"
    antes = set(arq.read_text(encoding="utf-8").split()) if arq.exists() else set()
    if doms - antes:
        arq.write_text("\n".join(sorted(antes | doms)) + "\n", encoding="utf-8")
        print("lojas liberadas:", ", ".join(sorted(doms - antes)), flush=True)


def main():
    preparar()
    os.environ["ELITE_DIR"] = str(APP)
    proximo = {r: time.time() + i * 120 for i, r in enumerate(AGENDA)}  # espalha a primeira rodada
    rodando = {}
    print("agendador do Radar Black no ar:", ", ".join(f"{r} a cada {s // 60} min" for r, s in AGENDA.items()), flush=True)
    while True:
        agora = time.time()
        for robo, intervalo in AGENDA.items():
            p = rodando.get(robo)
            if p and p.poll() is None:
                continue  # ciclo anterior ainda roda: nunca dois do mesmo robô
            if p:
                print(f"robô {robo} terminou com código {p.returncode}", flush=True)
                rodando.pop(robo)
            if agora >= proximo[robo]:
                if robo == "educado":
                    liberadas()
                print(f"== ciclo do robô {robo}", flush=True)
                rodando[robo] = subprocess.Popen(["bash", str(APP / "tools/black/vps/rodar.sh"), robo], cwd=APP)
                proximo[robo] = agora + intervalo
        time.sleep(20)


if __name__ == "__main__":
    main()
