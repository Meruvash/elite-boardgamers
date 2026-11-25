"""Especial /resenhas/perfis-de-jogador/: jogos para ficar de olho em cada perfil de jogador.

Uso: python3 tools/build_perfis.py   (também roda no fim de build_home.py)
Dados em conteudo/perfis_jogador.json. Jogo com resenha nossa ("resenha": "<slug>") usa capa, tagline e fichinhas
da própria resenha e leva até ela; os outros ("ludopedia": <id>) usam a capa em img/perfis/<id>.jpg e a frase do JSON,
sem link. Nada de nota, preço ou edição nacional aqui: isso é com a resenha.
"""
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo  # noqa: E402
from build_guias import CSS_GUIA, fatos  # noqa: E402
from build_home import pagina  # noqa: E402
from build_review import ROOT, SITE, nome_br, versao  # noqa: E402
from filtros_resenha import derivar  # noqa: E402
from layout import cabecalho, rodape, trilha  # noqa: E402

e = html.escape
SLUG = "resenhas/perfis-de-jogador"

CSS = """<style>
.perfis-idx{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.perfis-idx a{font-size:.9rem;font-weight:700;padding:6px 12px;border:1px solid var(--paper-line);border-radius:999px;background:#fff;color:var(--paper-ink);text-decoration:none}
.perfis-idx a:hover{border-color:var(--gold)}
.bloco.perfil>h2{display:flex;gap:10px;align-items:center;justify-content:flex-start}.perfil .em{font-size:1.5rem;line-height:1}
.perfil>p{max-width:68ch;margin:6px 0 12px}
.jogos-g>li>div.sem-link{display:grid;grid-template-columns:96px 1fr;gap:14px;align-items:start;padding:12px;border:1px solid var(--paper-line);border-radius:12px;background:#fff}
.jogos-g .sem-res{font-size:.8rem;font-weight:700;color:var(--paper-muted);margin-top:8px}
.jogos-g .rel{font-size:.85rem;margin-top:6px}.jogos-g .rel a{font-weight:700;color:var(--link)}
@media (max-width:480px){.jogos-g>li>div.sem-link{grid-template-columns:72px 1fr;gap:12px}}
</style>"""


def resenha(slug):
    return json.loads((ROOT / "conteudo" / f"{slug}.json").read_text(encoding="utf-8"))


def cartao(j, pre):
    if j.get("resenha"):
        c = resenha(j["resenha"])
        capa = ROOT / c["slug"] / "capa.jpg"
        return (f'<li><a href="{pre}{c["slug"]}/"><img src="{pre}{c["slug"]}/capa.jpg{versao(capa)}" width="96" height="96" alt="" loading="lazy">'
                f'<div><h3>{e(nome_br(c))}</h3><p class="tg">{e(c["tagline"])}</p><ul class="fx">{fatos(derivar(c), c)}</ul>'
                f'<p class="sem-res" style="color:var(--link)">Ler a nossa resenha →</p></div></a></li>')
    capa = ROOT / "img" / "perfis" / f'{j["ludopedia"]}.jpg'
    img = (f'<img src="{pre}img/perfis/{j["ludopedia"]}.jpg{versao(capa)}" width="96" height="96" alt="" loading="lazy">'
           if capa.exists() else '<span></span>')
    rel = ""
    if j.get("relacionada"):
        c = resenha(j["relacionada"])
        rel = f'<p class="rel">Do mesmo universo: <a href="{pre}{c["slug"]}/">nossa resenha de {e(nome_br(c))}</a></p>'
    return (f'<li><div class="sem-link">{img}<div><h3>{e(j["nome"])}</h3><p class="tg">{e(j["frase"])}</p>{rel}'
            f'<p class="sem-res">Ainda sem resenha no site</p></div></div></li>')


def build():
    d = json.loads((ROOT / "conteudo" / "perfis_jogador.json").read_text(encoding="utf-8"))
    pre = "../../"
    url = f"{SITE}/{SLUG}/"
    idx = "".join(f'<a href="#{p["id"]}">{p["emoji"]} {e(p["nome"])}</a>' for p in d["perfis"])
    secoes = "".join(
        f'<section class="bloco perfil" id="{p["id"]}"><h2><span class="em" aria-hidden="true">{p["emoji"]}</span>{e(p["nome"])}</h2>'
        f'<p>{e(p["texto"])}</p><ol class="jogos-g">{"".join(cartao(j, pre) for j in p["jogos"])}</ol></section>'
        for p in d["perfis"])
    corpo = f"""{cabecalho(pre, "Resenhas", sub=True)}
<main id="conteudo" class="in"><div class="nota guia">
 {trilha(("Início", pre), ("Resenhas", f"{pre}resenhas/"), ("Perfis de jogador", ""))}
 <article class="bloco">
  <h1>{e(d["titulo"])}</h1>
  <p class="lide">{e(d["lide"])}</p>
  <nav class="perfis-idx" aria-label="Perfis">{idx}</nav>
 </article>
 {secoes}
 <section class="bloco"><p class="criterio">Quer escolher por critério (jogadores, duração, peso)? Use a <a class="mais-g" href="{pre}resenhas/">busca de resenhas</a> ou o <a class="mais-g" href="{pre}jogos-de-tabuleiro/">guia de jogos de tabuleiro</a>.</p></section>
</div></main>
{rodape(pre)}"""
    itens, vistos = [], set()
    for p in d["perfis"]:
        for j in p["jogos"]:
            nome = nome_br(resenha(j["resenha"])) if j.get("resenha") else j["nome"]
            if nome in vistos:
                continue
            vistos.add(nome)
            it = {"@type": "ListItem", "position": len(itens) + 1, "name": nome}
            if j.get("resenha"):
                it["url"] = f"{SITE}/{j['resenha']}/"
            itens.append(it)
    ld = seo.script({"@type": "ItemList", "@id": f"{url}#lista", "name": d["titulo_seo"], "numberOfItems": len(itens),
                     "itemListElement": itens},
                    seo.trilha(("Início", f"{SITE}/"), ("Resenhas", f"{SITE}/resenhas/"), ("Perfis de jogador", url)))
    descr = ("Do conquistador ao jogador de galera: 12 perfis de jogador de tabuleiro e os jogos para ficar de olho em "
             "cada um, com link para as nossas resenhas.")
    destino = ROOT / SLUG
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "index.html").write_text(
        pagina(f'{d["titulo_seo"]} | Elite Boardgamers', descr, url, f"{SITE}/resenhas/capa.jpg", pre, corpo,
               head_extra="\n" + CSS_GUIA + "\n" + CSS, jsonld=ld), encoding="utf-8")
    return url


if __name__ == "__main__":
    print("ok", build())
