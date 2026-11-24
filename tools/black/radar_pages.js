// Serve as páginas e imagens do Radar Black a partir do bucket R2 (binding RADAR), onde o servidor da Oracle Cloud
// publica cada ciclo dos robôs. Se o bucket não estiver ligado ou o arquivo não existir lá, cai na cópia estática do
// repositório (a última versão publicada pelo GitHub, de 24/11/2026). Ver tools/black/vps/LEIAME.md.

const TIPOS = {
  html: "text/html; charset=utf-8",
  json: "application/json; charset=utf-8",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  png: "image/png",
  webp: "image/webp",
  svg: "image/svg+xml",
  xml: "application/xml; charset=utf-8",
  txt: "text/plain; charset=utf-8",
};

export async function servirDoRadar(context) {
  const { request, env, next } = context;
  if (!env.RADAR || (request.method !== "GET" && request.method !== "HEAD")) return next();
  const url = new URL(request.url);
  let chave = decodeURIComponent(url.pathname).replace(/^\/+/, "");
  if (chave.endsWith("/") || !chave.split("/").pop().includes(".")) {
    if (!chave.endsWith("/")) return Response.redirect(url.origin + url.pathname + "/" + url.search, 301);
    chave += "index.html";
  }
  const obj = await env.RADAR.get(chave);
  if (!obj) return next();
  const ext = chave.split(".").pop().toLowerCase();
  const html = ext === "html";
  const headers = new Headers({
    "content-type": TIPOS[ext] || "application/octet-stream",
    "cache-control": html ? "public, max-age=60" : "public, max-age=86400",
    etag: obj.httpEtag,
  });
  return new Response(request.method === "HEAD" ? null : obj.body, { headers });
}
