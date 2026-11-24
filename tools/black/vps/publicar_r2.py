#!/usr/bin/env python3
"""Envia pastas do site para o bucket R2 do Radar Black, só os arquivos que mudaram.

Uso: publicar_r2.py <pasta> [<pasta> ...]   (caminhos relativos à raiz do site, ex.: black img/black)

Variáveis (em /etc/elite-radar.env): R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET (padrão
elite-radar). A chave do objeto é o próprio caminho (black/index.html), que é o que functions/ procura.
Compara o MD5 local com o ETag do R2 (igual ao MD5 em envios simples) e não reenvia o que não mudou.
"""
import hashlib
import mimetypes
import os
import sys
from pathlib import Path

import boto3

RAIZ = Path(__file__).resolve().parents[3]
BUCKET = os.environ.get("R2_BUCKET", "elite-radar")


def cliente():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )


def remotos(s3, prefixo):
    etags = {}
    for pagina in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefixo):
        for o in pagina.get("Contents", []):
            etags[o["Key"]] = o["ETag"].strip('"')
    return etags


def main(pastas):
    s3 = cliente()
    enviados = iguais = 0
    for pasta in pastas:
        etags = remotos(s3, pasta.rstrip("/") + "/")
        for arq in sorted((RAIZ / pasta).rglob("*")):
            if not arq.is_file() or arq.name.startswith("."):
                continue
            chave = arq.relative_to(RAIZ).as_posix()
            dados = arq.read_bytes()
            if etags.get(chave) == hashlib.md5(dados).hexdigest():
                iguais += 1
                continue
            tipo = mimetypes.guess_type(arq.name)[0] or "application/octet-stream"
            s3.put_object(Bucket=BUCKET, Key=chave, Body=dados, ContentType=tipo)
            enviados += 1
    print(f"R2: {enviados} arquivo(s) enviado(s), {iguais} sem mudança")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
