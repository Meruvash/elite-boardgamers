#!/usr/bin/env python3
"""Agendador do Radar Black no Railway (pedido do usuário em 27/11/2026: um segundo servidor, que cobre o da Oracle).

Roda o tempo todo e chama tools/black/vps/rodar.sh nos mesmos intervalos do servidor da Oracle. Os dados ficam no
volume do Railway (/data); a página vai ao R2 com o prefixo v2/ e o site mostra a cópia mais nova entre os dois
servidores (tools/black/radar_pages.js). Código novo chega sozinho: o Railway refaz o serviço a cada push na main.

O robô de alertas não roda aqui (o da Oracle já manda; dois mandariam o mesmo aviso duas vezes).
"""
import os
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
                print(f"== ciclo do robô {robo}", flush=True)
                rodando[robo] = subprocess.Popen(["bash", str(APP / "tools/black/vps/rodar.sh"), robo], cwd=APP)
                proximo[robo] = agora + intervalo
        time.sleep(20)


if __name__ == "__main__":
    main()
