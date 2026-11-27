const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const dir = __dirname;
const srv = http.createServer((q, r) => { const f = path.join(dir, decodeURIComponent(q.url.split('?')[0])); 
  const t = f.endsWith('.js') ? 'text/javascript' : f.endsWith('.json') ? 'application/json' : 'text/html';
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); } else { r.writeHead(200, {'content-type': t}); r.end(d); } }); }).listen(8765);
(async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  p.on('console', m => console.log('page:', m.text())); p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('http://localhost:8765/cena.html'); await p.waitForFunction('window.pronto===true', null, { timeout: 120000 });
  const dur = await p.evaluate('window.DURACAO'); const fps = +(process.argv[2] || 30); const n = Math.ceil(dur * fps);
  const so = process.argv[3]; fs.mkdirSync(path.join(dir, 'frames'), { recursive: true });
  console.log('duração', dur, 'frames', n);
  const lista = so ? so.split(',').map(Number) : [...Array(n).keys()];
  for (const i of lista) { await p.evaluate(t => window.renderFrame(t), i / fps);
    await p.screenshot({ path: path.join(dir, 'frames', String(i).padStart(5, '0') + '.png') }); if (i % 100 == 0) console.log('frame', i); }
  await b.close(); srv.close();
})();
