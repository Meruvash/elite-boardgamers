// Cenas do vídeo "50% de quê?" (Black de Verdade, Elite Boardgamers) — pintadas em código, sem imagem gerada por IA.
// Motor: huashu-art-motion (MIT). Recorte quadrado central (x 420..1500 de 1920x1080). Composições novas,
// à maneira de mestres em domínio público; figuras sempre de costas ou pequenas, sem rosto de frente:
//   el_caravaggio — Caravaggio, "Os Trapaceiros" (c. 1594): mesa de cartas na luz em diagonal, etiqueta "−50%" balançando
//   el_latour     — Georges de La Tour (c. 1635–45): vela única, pena escrevendo o preço "de" na etiqueta; depois a lupa
//   el_grafico    — caderno de campo em aquarela: o preço ao longo dos meses, a média real e a régua de −20%
//   el_cezanne    — Cézanne, "Os Jogadores de Cartas" (1890–95): dois jogadores de costas, louros sobre a mesa
//   el_pissarro   — Pissarro, bulevares de Paris (1897): vitrine de loja de rua com caixas de jogo
//   el_steen      — Jan Steen, festas de família (c. 1660–70): roda de amigos em volta da mesa, de costas
//   el_vermeer    — Vermeer, interiores com janela à esquerda: um celular acende na mesa
//   el_chardin    — Chardin, "O Castelo de Cartas" (c. 1737): o castelo sobe andar por andar
//   el_caillebotte— Caillebotte, "Rua de Paris, Dia de Chuva" (1877): figura de costas leva caixas de jogo empilhadas
//   el_mesa_dia   — a mesa da abertura, agora de dia, com um jogo montado e uma cadeira vazia
(() => {
  const W = 1920, H = 1080, { clamp, lerp, rng, ss } = U, P = PAINT, M = MEDIUM, TAU = Math.PI * 2;
  const poly = (g, pts) => { g.beginPath(); pts.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.closePath(); };
  const grad = (g, x0, y0, x1, y1, stops) => { const gr = g.createLinearGradient(x0, y0, x1, y1); stops.forEach(([o, c]) => gr.addColorStop(o, c)); return gr; };
  const radg = (g, x, y, r0, r1, stops) => { const gr = g.createRadialGradient(x, y, r0, x, y, r1); stops.forEach(([o, c]) => gr.addColorStop(o, c)); return gr; };
  const tela = (c, id, cor, a = 0.17) => { c.save(); c.globalCompositeOperation = 'multiply'; c.globalAlpha = a; c.drawImage(P.texture(id, cor, { scale: 0.006, amt: 14, grain: 8, seed: 53 }), 0, 0); c.restore(); };
  const ease = (a, b, t) => ss(a, b, t);
  // figura de costas: ombros, costas e cabeça vistas por trás (chapéu opcional)
  function costas(g, x, y, s, cor, cabelo, chapeu, pena) {
    g.fillStyle = cor; g.beginPath(); g.moveTo(x - 120 * s, y + 260 * s); g.quadraticCurveTo(x - 130 * s, y + 40 * s, x - 70 * s, y + 10 * s);
    g.quadraticCurveTo(x, y - 10 * s, x + 70 * s, y + 10 * s); g.quadraticCurveTo(x + 130 * s, y + 40 * s, x + 120 * s, y + 260 * s); g.closePath(); g.fill();
    g.fillStyle = cabelo; g.beginPath(); g.ellipse(x, y - 40 * s, 46 * s, 54 * s, 0, 0, TAU); g.fill();
    if (chapeu) { g.fillStyle = chapeu; g.beginPath(); g.ellipse(x, y - 78 * s, 92 * s, 22 * s, -0.08, 0, TAU); g.fill(); g.beginPath(); g.ellipse(x, y - 100 * s, 50 * s, 34 * s, 0, 0, TAU); g.fill();
      if (pena) { g.fillStyle = pena; g.beginPath(); g.moveTo(x + 30 * s, y - 118 * s); g.quadraticCurveTo(x + 120 * s, y - 190 * s, x + 150 * s, y - 120 * s); g.quadraticCurveTo(x + 100 * s, y - 140 * s, x + 40 * s, y - 100 * s); g.fill(); } }
  }
  function carta(g, x, y, w, h, rot, face) {
    g.save(); g.translate(x, y); g.rotate(rot); g.fillStyle = 'rgba(0,0,0,.35)'; g.fillRect(-w / 2 + 6, -h / 2 + 8, w, h);
    g.fillStyle = face ? '#f2ead6' : '#8a2a22'; g.fillRect(-w / 2, -h / 2, w, h);
    if (face) { g.fillStyle = face; g.beginPath(); g.moveTo(0, -h * .22); g.lineTo(w * .2, 0); g.lineTo(0, h * .22); g.lineTo(-w * .2, 0); g.fill(); }
    else { g.strokeStyle = '#e8c070'; g.lineWidth = 3; g.strokeRect(-w / 2 + 7, -h / 2 + 7, w - 14, h - 14); }
    g.restore();
  }
  function etiqueta(c, x, y, rot, txt, esc = 1) {        // etiqueta de papel presa por barbante
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(esc, esc);
    c.strokeStyle = '#d8c8a0'; c.lineWidth = 3; c.beginPath(); c.moveTo(0, -120); c.lineTo(0, -8); c.stroke();
    c.fillStyle = 'rgba(0,0,0,.35)'; poly(c, [[-62, 6], [62, 6], [62, 166], [-62, 166]]); c.fill();
    c.fillStyle = '#f3e7c8'; poly(c, [[-30, -10], [30, -10], [58, 18], [58, 160], [-58, 160], [-58, 18]]); c.fill();
    c.fillStyle = '#5a4a30'; c.beginPath(); c.arc(0, 8, 7, 0, TAU); c.fill();
    if (txt) { c.fillStyle = '#b8241c'; c.font = 'italic 900 40px Georgia, serif'; c.textAlign = 'center'; c.fillText(txt, 0, 100); }
    c.restore();
  }

  // ---------------------------------------------------------------- Caravaggio: a mesa dos trapaceiros
  SCENES['el_caravaggio'] = (() => {
    let plate, built = false;
    function build() {
      const a = P.canvas(), g = a.getContext('2d'), r = rng(901);
      g.fillStyle = grad(g, 0, 0, W, H, [[0, '#4a3a26'], [0.45, '#1e160e'], [1, '#0a0806']]); g.fillRect(0, 0, W, H);
      g.fillStyle = radg(g, 700, 260, 40, 900, [[0, 'rgba(255,220,160,.55)'], [0.5, 'rgba(160,110,60,.18)'], [1, 'rgba(0,0,0,0)']]); g.fillRect(0, 0, W, H);
      // mesa com tapete turco
      g.fillStyle = grad(g, 0, 620, 0, H, [[0, '#7a3a1e'], [0.5, '#5a2414'], [1, '#2a0e08']]); poly(g, [[300, 640], [1620, 640], [1760, H], [160, H]]); g.fill();
      g.strokeStyle = '#c8962e'; g.lineWidth = 9; g.beginPath(); g.moveTo(290, 700); g.lineTo(1630, 700); g.stroke();
      for (let i = 0; i < 26; i++) { g.fillStyle = ['#1e3a5a', '#c8962e', '#7a1e18'][i % 3]; const x = 340 + i * 50; poly(g, [[x, 720], [x + 22, 745], [x, 770], [x - 22, 745]]); g.fill(); }
      // cartas espalhadas e moedas
      [[760, 880, .3, '#b8241c'], [880, 905, -.15, 0], [1010, 870, .5, '#1a1a1a'], [1150, 910, -.4, 0], [1240, 860, .1, '#b8241c']].forEach(([x, y, ro, f]) => carta(g, x, y, 96, 140, ro, f));
      for (let i = 0; i < 9; i++) { const x = 600 + r() * 120, y = 940 + r() * 40; g.fillStyle = grad(g, x - 20, y, x + 20, y, [[0, '#f4d27a'], [1, '#8a6420']]); g.beginPath(); g.ellipse(x, y, 22, 9, 0, 0, TAU); g.fill(); }
      // dois jogadores de costas: veludo vermelho com chapéu de pena; gibão listrado
      costas(g, 560, 420, 1.25, '#8a1e1a', '#2a1a10', '#1a1410', '#f2ead6');
      g.fillStyle = 'rgba(255,230,190,.35)'; g.beginPath(); g.ellipse(500, 520, 40, 120, -0.3, 0, TAU); g.fill();      // luz no ombro
      costas(g, 1360, 440, 1.2, '#c8a050', '#3a2414', null, null);
      g.strokeStyle = '#5a3a1a'; g.lineWidth = 16; for (let k = 0; k < 6; k++) { g.beginPath(); g.moveTo(1250 + k * 40, 470); g.lineTo(1240 + k * 44, 760); g.stroke(); }
      // pilha de cartas no centro (onde pende a etiqueta)
      for (let k = 0; k < 7; k++) carta(g, 960, 760 - k * 5, 110, 160, 0.02 * k, 0);
      return M.broken(a, { cell: 7, len: 16, wid: 6, passes: 2, angle: (x, y) => -0.7 + Math.sin(y * 0.005) * 0.4, seed: 91, jit: 12, skip: 0.04, sat: 1.12, warm: [255, 210, 150], cool: [60, 50, 80] });
    }
    function draw(c, lt) {
      if (!built) { plate = build(); built = true; }
      const t = Math.max(0, lt);
      c.drawImage(plate, 0, 0);
      // a mão de trás passa uma carta por baixo da mesa (a trapaça)
      const k = ease(2.2, 4.4, t), hx = lerp(1450, 1210, k), hy = lerp(990, 900, k);
      c.save(); c.fillStyle = '#c8a050'; c.beginPath(); c.ellipse(hx + 80, hy + 40, 70, 34, -0.4, 0, TAU); c.fill();
      c.fillStyle = '#e0b48a'; c.beginPath(); c.ellipse(hx, hy, 40, 24, -0.3, 0, TAU); c.fill(); c.restore();
      carta(c, hx - 30, hy - 30, 80, 118, -0.6 + k * 0.3, '#b8241c');
      // a etiqueta balança sobre a pilha
      etiqueta(c, 960, 560, Math.sin(t * 2.1) * 0.12 + Math.sin(t * 0.7) * 0.05, '−50%', 1.25);
      // poeira na luz
      const r = rng(5 + Math.floor(t * 8)); c.fillStyle = 'rgba(255,230,180,.5)';
      for (let i = 0; i < 40; i++) { const x = 500 + r() * 600 + Math.sin(t + i) * 10, y = 120 + r() * 500; c.fillRect(x, y, 2, 2); }
      tela(c, 'canvas_el1', '#e8dcc8');
    }
    return { draw };
  })();

  // ---------------------------------------------------------------- La Tour: a vela e a pena
  SCENES['el_latour'] = (() => {
    let plate, built = false; const VX = 760, VY = 520;
    function build() {
      const a = P.canvas(), g = a.getContext('2d');
      g.fillStyle = '#0a0705'; g.fillRect(0, 0, W, H);
      g.fillStyle = grad(g, 0, 700, 0, H, [[0, '#3a2414'], [1, '#140c06']]); g.fillRect(0, 700, W, H - 700);
      // vela grossa
      g.fillStyle = grad(g, VX - 34, 0, VX + 34, 0, [[0, '#c8a878'], [0.5, '#f4e2c0'], [1, '#a08060']]); g.fillRect(VX - 34, VY + 20, 68, 230);
      g.fillStyle = '#5a3a20'; g.beginPath(); g.ellipse(VX, VY + 250, 90, 22, 0, 0, TAU); g.fill();
      // manga de veludo e mão segurando a pena (vinda da direita)
      g.fillStyle = '#6a1e18'; poly(g, [[1700, 520], [1520, 600], [1300, 760], [1360, 860], [1600, 760], [1760, 700]]); g.fill();
      g.fillStyle = '#f0e0c8'; g.beginPath(); g.ellipse(1290, 790, 54, 34, -0.5, 0, TAU); g.fill();
      // papel da etiqueta sobre a mesa
      g.save(); g.translate(1060, 860); g.rotate(-0.08); g.fillStyle = '#f3e7c8'; poly(g, [[-200, -60], [170, -60], [230, 0], [170, 60], [-200, 60]]); g.fill(); g.restore();
      return M.broken(a, { cell: 6, len: 14, wid: 5, passes: 2, angle: (x, y) => Math.atan2(y - VY, x - VX) + Math.PI / 2, seed: 81, jit: 10, skip: 0.03, sat: 1.15, warm: [255, 200, 120], cool: [40, 30, 50] });
    }
    function draw(c, lt) {
      if (!built) { plate = build(); built = true; }
      const t = Math.max(0, lt), apaga = ease(8.6, 9.8, t);
      const fl = 1 + Math.sin(t * 13) * 0.04 + Math.sin(t * 29) * 0.03;
      c.fillStyle = '#140c06'; c.fillRect(0, 0, W, H); c.save(); c.translate(0, -170);   // a mesa sobe para a legenda não cobrir a etiqueta
      c.drawImage(plate, 0, 0);
      // o texto escrito pela pena, letra a letra; depois o número sobe (o preço "de" inflado)
      const txt = 'de R$ 400', n = Math.floor(clamp((t - 0.6) / 2.2, 0, 1) * txt.length);
      c.save(); c.translate(1040, 880); c.rotate(-0.08); c.fillStyle = '#2a1a10'; c.font = 'italic 700 74px Georgia, serif'; c.textAlign = 'left';
      c.fillText(txt.slice(0, n), -170, 18);
      const sobe = ease(3.4, 4.4, t); if (sobe > 0) { c.strokeStyle = '#b8241c'; c.lineWidth = 7; c.beginPath(); c.moveTo(-10, 0); c.lineTo(-10 + 170 * sobe, 0); c.stroke();
        c.globalAlpha = sobe; c.fillStyle = '#b8241c'; c.fillText('600', 0, -48 - 20 * sobe); }
      c.restore();
      // pena acompanha a escrita
      const px = 1040 - 170 + Math.min(n, txt.length) * 34 + (t > 3.4 ? 120 * sobe : 0), py = 860 - (t > 3.4 ? 60 * sobe : 0) + Math.sin(t * 18) * 4 * (n < txt.length ? 1 : 0);
      c.save(); c.strokeStyle = '#f2ead6'; c.lineWidth = 5; c.beginPath(); c.moveTo(px, py); c.lineTo(px + 160, py - 260); c.stroke();
      c.fillStyle = 'rgba(242,234,214,.85)'; c.beginPath(); c.moveTo(px + 60, py - 90); c.quadraticCurveTo(px + 230, py - 230, px + 170, py - 300); c.quadraticCurveTo(px + 120, py - 200, px + 60, py - 90); c.fill(); c.restore();
      // a lupa entra (fala 3) e passa sobre a etiqueta
      const lu = ease(5.6, 6.6, t);
      if (lu > 0) { const lx = lerp(1500, 1060, lu) + Math.sin(t * 1.3) * 30, ly = lerp(560, 860, lu);
        c.save(); c.beginPath(); c.arc(lx, ly, 120, 0, TAU); c.clip(); c.translate(lx, ly); c.scale(1.5, 1.5); c.translate(-lx, -ly); c.drawImage(plate, 0, 0);
        c.translate(1040, 880); c.rotate(-0.08); c.fillStyle = '#2a1a10'; c.font = 'italic 700 74px Georgia, serif'; c.fillText(txt, -170, 18); c.restore();
        c.save(); c.strokeStyle = '#b08a3a'; c.lineWidth = 16; c.beginPath(); c.arc(lx, ly, 124, 0, TAU); c.stroke(); c.lineWidth = 26; c.strokeStyle = '#3a2410'; c.beginPath(); c.moveTo(lx + 88, ly + 88); c.lineTo(lx + 230, ly + 230); c.stroke(); c.restore(); }
      // a chama: tremula e apaga no fim
      c.save(); c.globalCompositeOperation = 'lighter';
      c.fillStyle = radg(c, VX, VY - 10, 4, 640 * fl * (1 - apaga * 0.85), [[0, 'rgba(255,200,110,.55)'], [0.35, 'rgba(200,120,50,.18)'], [1, 'rgba(0,0,0,0)']]); c.fillRect(0, 0, W, H); c.restore();
      if (apaga < 1) { c.save(); c.globalAlpha = 1 - apaga; c.fillStyle = radg(c, VX, VY - 26, 2, 46, [[0, '#fffbe8'], [0.4, '#ffd070'], [1, 'rgba(255,140,40,0)']]);
        c.beginPath(); c.ellipse(VX + Math.sin(t * 9) * 3, VY - 22, 16 * fl, 40 * fl, Math.sin(t * 7) * 0.06, 0, TAU); c.fill(); c.restore(); }
      else { c.save(); c.strokeStyle = 'rgba(200,190,170,.35)'; c.lineWidth = 4; c.beginPath(); for (let k = 0; k < 30; k++) { const yy = VY - k * 10; c.lineTo(VX + Math.sin(k * .4 + t * 3) * 14, yy); } c.stroke(); c.restore(); }
      c.restore();
      c.save(); c.fillStyle = `rgba(0,0,0,${apaga * 0.55})`; c.fillRect(0, 0, W, H); c.restore();
      tela(c, 'canvas_el2', '#d8c8a8', 0.14);
    }
    return { draw };
  })();

  // ---------------------------------------------------------------- caderno em aquarela: preço, média real, régua de −20%
  SCENES['el_grafico'] = (() => {
    let plate, built = false;
    const X0 = 520, X1 = 1420, YB = 820;
    // preço ilustrativo semana a semana (6 meses): oscila perto de 400 e cai no fim
    const N = 26, PR = Array.from({ length: N }, (_, i) => 400 + Math.sin(i * 0.9) * 18 + Math.sin(i * 2.3) * 9 - (i > 22 ? (i - 22) * 52 : 0));
    const yv = v => YB - (v - 150) * 1.35, xv = i => X0 + i * (X1 - X0) / (N - 1), MED = 400;
    function build() {
      const a = P.canvas(), g = a.getContext('2d'), r = rng(333);
      g.fillStyle = '#efe6d2'; g.fillRect(0, 0, W, H);
      for (let i = 0; i < 40; i++) { g.fillStyle = `rgba(${170 + r() * 40},${150 + r() * 30},${110 + r() * 30},.06)`; g.beginPath(); g.ellipse(r() * W, r() * H, 80 + r() * 260, 40 + r() * 140, r() * 3, 0, TAU); g.fill(); }
      g.strokeStyle = 'rgba(120,140,170,.25)'; g.lineWidth = 2; for (let y = 160; y < H; y += 46) { g.beginPath(); g.moveTo(380, y); g.lineTo(1540, y); g.stroke(); }
      g.strokeStyle = 'rgba(200,80,70,.35)'; g.beginPath(); g.moveTo(470, 120); g.lineTo(470, H); g.stroke();
      return M.broken(a, { cell: 9, len: 22, wid: 8, passes: 1, angle: () => 0.02, seed: 33, jit: 8, skip: 0.2, sat: 1.0, warm: [250, 240, 220], cool: [200, 200, 210] });
    }
    function lapis(c, x0, y0, x1, y1, cor, w, seed) { const r = rng(seed); c.strokeStyle = cor; c.lineWidth = w; c.lineCap = 'round';
      for (let p = 0; p < 2; p++) { c.beginPath(); c.moveTo(x0 + (r() - .5) * 3, y0 + (r() - .5) * 3); const n = 12; for (let k = 1; k <= n; k++) c.lineTo(lerp(x0, x1, k / n) + (r() - .5) * 3, lerp(y0, y1, k / n) + (r() - .5) * 3); c.stroke(); } }
    function draw(c, lt) {
      if (!built) { plate = build(); built = true; }
      const t = Math.max(0, lt);
      c.drawImage(plate, 0, 0);
      // eixos a lápis e meses
      lapis(c, X0 - 20, YB + 20, X1 + 40, YB + 20, '#4a4a58', 3, 1); lapis(c, X0 - 20, YB + 20, X0 - 20, 240, '#4a4a58', 3, 2);
      c.fillStyle = '#4a4a58'; c.font = '700 34px Caveat, cursive'; c.textAlign = 'center';
      ['jun', 'jul', 'ago', 'set', 'out', 'nov'].forEach((m, k) => c.fillText(m, X0 + k * (X1 - X0) / 5.2 + 40, YB + 66));
      // a linha do preço em aquarela, desenhada aos poucos
      const k = clamp((t - 0.3) / 3.6, 0, 1) * (N - 1);
      c.save(); c.lineJoin = 'round'; c.lineCap = 'round';
      for (const [w, a2] of [[22, .16], [11, .32], [4, .9]]) { c.strokeStyle = `rgba(40,70,120,${a2})`; c.lineWidth = w; c.beginPath();
        for (let i = 0; i <= Math.floor(k); i++) { const x = xv(i), y = yv(PR[i]); i ? c.lineTo(x, y) : c.moveTo(x, y); }
        const i0 = Math.floor(k); if (i0 < N - 1) c.lineTo(lerp(xv(i0), xv(i0 + 1), k - i0), lerp(yv(PR[i0]), yv(PR[i0 + 1]), k - i0)); c.stroke(); }
      c.restore();
      // a média real: faixa dourada tracejada (fala 4, "média")
      const m = ease(4.1, 5.0, t);
      if (m > 0) { c.save(); c.globalAlpha = m; c.fillStyle = 'rgba(214,170,60,.22)'; c.fillRect(X0 - 20, yv(MED) - 16, (X1 - X0 + 60) * m, 32);
        c.setLineDash([22, 14]); c.strokeStyle = '#b8862a'; c.lineWidth = 5; c.beginPath(); c.moveTo(X0 - 20, yv(MED)); c.lineTo(X0 - 20 + (X1 - X0 + 60) * m, yv(MED)); c.stroke(); c.restore(); }
      // a régua de −20% riscada em vermelho (fala 5, "20%")
      const rg = ease(9.0, 9.9, t);
      if (rg > 0) { lapis(c, X0 - 20, yv(MED * .8), X0 - 20 + (X1 - X0 + 60) * rg, yv(MED * .8), '#c0281a', 5, 7);
        c.save(); c.globalAlpha = rg * .18; c.fillStyle = '#3ddc84'; c.fillRect(X0 - 20, yv(MED * .8), X1 - X0 + 60, YB + 20 - yv(MED * .8)); c.restore(); }
      // os pontos que caem abaixo da régua acendem em verde
      for (let i = 0; i < N; i++) { if (i > k) break; const v = PR[i], x = xv(i), y = yv(v), abaixo = v < MED * .8, on = abaixo ? ease(10.2 + (i - 23) * .5, 10.6 + (i - 23) * .5, t) : 0;
        c.fillStyle = on > 0 ? `rgba(40,190,110,${.4 + .6 * on})` : 'rgba(40,70,120,.75)'; c.beginPath(); c.arc(x, y, 9 + on * 9 + (on > 0 ? Math.sin(t * 6) * 2 : 0), 0, TAU); c.fill(); }
      tela(c, 'canvas_el3', '#e8dcc8', 0.12);
    }
    return { draw };
  })();

  // ---------------------------------------------------------------- Cézanne: os jogadores, de costas, e os louros
  SCENES['el_cezanne'] = (() => {
    let plate, built = false;
    function build() {
      const a = P.canvas(), g = a.getContext('2d');
      g.fillStyle = grad(g, 0, 0, W, 0, [[0, '#8a7458'], [0.5, '#b49a70'], [1, '#6a5a48']]); g.fillRect(0, 0, W, H);
      g.fillStyle = '#7a8a9a'; g.fillRect(420, 120, 380, 300); g.fillStyle = '#c8a46a'; g.fillRect(1150, 90, 260, 380);
      g.fillStyle = grad(g, 0, 600, 0, H, [[0, '#a8603a'], [1, '#5a3020']]); poly(g, [[380, 610], [1540, 610], [1620, H], [300, H]]); g.fill();
      g.fillStyle = '#e8dcc0'; poly(g, [[520, 630], [1400, 630], [1450, 760], [470, 760]]); g.fill();          // toalha
      costas(g, 560, 470, 1.3, '#3a4a6a', '#5a4a3a', '#4a3a2e');                                               // chapéu-coco
      costas(g, 1360, 480, 1.25, '#b0a080', '#3a2a1e', '#6a5a4a');
      g.fillStyle = '#2a3a2a'; g.fillRect(940, 470, 40, 150); g.beginPath(); g.ellipse(960, 470, 20, 10, 0, 0, TAU); g.fill();   // garrafa
      [[860, 690, -.2], [1060, 700, .25]].forEach(([x, y, ro]) => carta(g, x, y, 70, 100, ro, '#b8241c'));
      // coroa de louros sobre a mesa (o prêmio)
      g.strokeStyle = '#4a6a2a'; g.lineWidth = 8; g.beginPath(); g.arc(960, 690, 70, Math.PI * 0.15, Math.PI * 0.85, true); g.stroke();
      for (let k = 0; k < 14; k++) { const an = Math.PI * 0.15 - k * (Math.PI * 1.7 / 14) * -1, sx = 960 + Math.cos(Math.PI + an) * 70, sy = 690 + Math.sin(Math.PI + an) * 70;
        g.fillStyle = k % 2 ? '#6a8a3a' : '#8aa04a'; g.beginPath(); g.ellipse(sx, sy, 20, 9, an, 0, TAU); g.fill(); }
      return M.broken(a, { cell: 10, len: 22, wid: 11, passes: 2, angle: (x, y) => 0.6 + Math.floor(x / 120) % 2 * 0.3, seed: 71, jit: 14, skip: 0.05, sat: 1.05, warm: [240, 210, 160], cool: [90, 110, 150] });
    }
    function draw(c, lt) { if (!built) { plate = build(); built = true; } const t = Math.max(0, lt); c.drawImage(plate, 0, 0);
      c.save(); c.globalCompositeOperation = 'lighter'; c.globalAlpha = 0.15 + 0.12 * Math.sin(t * 3); c.fillStyle = radg(c, 960, 690, 10, 200, [[0, '#ffe8a0'], [1, 'rgba(0,0,0,0)']]); c.fillRect(0, 0, W, H); c.restore();
      tela(c, 'canvas_el4', '#e8dcc8'); }
    return { draw };
  })();

  // ---------------------------------------------------------------- Pissarro: a vitrine da loja no bulevar
  SCENES['el_pissarro'] = (() => {
    let plate, built = false;
    function build() {
      const a = P.canvas(), g = a.getContext('2d'), r = rng(404);
      g.fillStyle = grad(g, 0, 0, 0, 300, [[0, '#a8b8c8'], [1, '#d8d4c8']]); g.fillRect(0, 0, W, 300);
      g.fillStyle = '#d8c8a8'; g.fillRect(380, 60, 1160, 640);                                       // fachada
      for (let j = 0; j < 3; j++) for (let i = 0; i < 7; i++) { g.fillStyle = '#5a6a7a'; g.fillRect(430 + i * 160, 100 + j * 120, 70, 90); }
      g.fillStyle = '#2a4a3a'; g.fillRect(380, 470, 1160, 240);                                       // frente da loja
      g.fillStyle = '#c84a2a'; for (let i = 0; i < 12; i++) { poly(g, [[380 + i * 97, 450], [477 + i * 97, 450], [470 + i * 97, 520], [387 + i * 97, 520]]); g.fill(); g.fillStyle = i % 2 ? '#c84a2a' : '#f0e0c0'; }   // toldo listrado
      g.fillStyle = '#f2dca0'; g.fillRect(480, 540, 900, 160);                                        // vitrine iluminada
      const cores = ['#b8241c', '#2a5a9a', '#e0a020', '#3a8a4a', '#6a3a8a', '#1a1a1a', '#e06a2a'];
      for (let i = 0; i < 9; i++) { g.fillStyle = cores[i % 7]; const x = 510 + i * 96, h = 70 + r() * 70; g.fillRect(x, 700 - h, 80, h); g.fillStyle = 'rgba(255,255,255,.4)'; g.fillRect(x + 8, 700 - h + 10, 64, 10); }
      g.fillStyle = grad(g, 0, 710, 0, H, [[0, '#8a8a90'], [1, '#5a5a66']]); g.fillRect(0, 710, W, H - 710);  // calçada molhada
      for (let i = 0; i < 14; i++) { const x = 420 + r() * 1080, y = 790 + r() * 200, s = 0.25 + (y - 760) / 900; g.fillStyle = ['#1e1e28', '#3a2a2a', '#2a3a5a'][i % 3]; g.fillRect(x - 12 * s * 3, y - 110 * s * 3, 24 * s * 3, 110 * s * 3); g.beginPath(); g.arc(x, y - 120 * s * 3, 10 * s * 3, 0, TAU); g.fill(); }
      return M.broken(a, { cell: 6, len: 12, wid: 6, passes: 2, angle: (x, y) => y > 710 ? 1.5 : 0.3, seed: 41, jit: 16, skip: 0.06, sat: 1.15, warm: [255, 230, 190], cool: [120, 130, 170] });
    }
    function draw(c, lt) { if (!built) { plate = build(); built = true; } const t = Math.max(0, lt); c.drawImage(plate, 0, 0);
      const r = rng(9 + Math.floor(t * 10)); c.fillStyle = 'rgba(255,236,190,.4)'; for (let i = 0; i < 90; i++) c.fillRect(480 + r() * 900, 720 + r() * 300, 4, 22 + r() * 30);   // reflexos na calçada
      tela(c, 'canvas_el5', '#e8dcc8'); }
    return { draw };
  })();

  // ---------------------------------------------------------------- Jan Steen: a roda de amigos
  SCENES['el_steen'] = (() => {
    let plate, built = false;
    function build() {
      const a = P.canvas(), g = a.getContext('2d');
      g.fillStyle = grad(g, 0, 0, 0, H, [[0, '#5a4a30'], [1, '#2a2014']]); g.fillRect(0, 0, W, H);
      g.fillStyle = 'rgba(255,220,150,.35)'; poly(g, [[420, 0], [700, 0], [1000, 700], [600, 700]]); g.fill();       // luz da janela alta
      g.fillStyle = '#8a6a3a'; g.beginPath(); g.ellipse(960, 640, 520, 150, 0, 0, TAU); g.fill();
      g.fillStyle = '#3a6a4a'; g.beginPath(); g.ellipse(960, 620, 300, 80, 0, 0, TAU); g.fill();        // tabuleiro verde
      const pc = ['#b8241c', '#2a5a9a', '#e0c040', '#f2ead6'];
      for (let i = 0; i < 16; i++) { g.fillStyle = pc[i % 4]; g.beginPath(); g.arc(760 + (i % 8) * 56, 600 + Math.floor(i / 8) * 40, 12, 0, TAU); g.fill(); }
      // figuras em volta, de costas e de perfil ao longe (sem rosto)
      [[520, 560, .9, '#8a2a22', '#c8a050'], [1400, 560, .9, '#2a4a6a', '#5a3a2a'], [760, 700, 1.15, '#d8b060', '#3a2a1a'], [1180, 710, 1.15, '#4a6a3a', '#2a1a10']].forEach(([x, y, s, cor, cab]) => costas(g, x, y, s, cor, cab, null, null));
      costas(g, 960, 300, .55, '#6a2a5a', '#3a2a1a', '#2a2a2a', '#e8d8b0');                                          // ao fundo, de pé
      g.fillStyle = '#c8a878'; g.beginPath(); g.ellipse(1500, 940, 90, 50, 0, 0, TAU); g.fill(); g.beginPath(); g.arc(1570, 900, 30, 0, TAU); g.fill();   // cachorro
      return M.broken(a, { cell: 7, len: 14, wid: 6, passes: 2, angle: (x, y) => -0.4 + Math.sin(x * .01) * .3, seed: 51, jit: 12, skip: 0.04, sat: 1.12, warm: [255, 215, 160], cool: [70, 60, 90] });
    }
    function draw(c, lt) { if (!built) { plate = build(); built = true; } const t = Math.max(0, lt); c.drawImage(plate, 0, 0);
      // um dado rola no tabuleiro
      const k = ease(0.1, 1.2, t), x = lerp(900, 1060, k), y = 620 - Math.abs(Math.sin(k * 9)) * 40 * (1 - k);
      c.save(); c.translate(x, y); c.rotate(k * 9); c.fillStyle = '#f6f0e0'; c.fillRect(-16, -16, 32, 32); c.fillStyle = '#1a1a1a'; [[-8, -8], [8, 8], [0, 0]].forEach(([a2, b]) => { c.beginPath(); c.arc(a2, b, 3.5, 0, TAU); c.fill(); }); c.restore();
      tela(c, 'canvas_el6', '#e8dcc8'); }
    return { draw };
  })();

  // ---------------------------------------------------------------- Vermeer: a janela e o celular que acende
  SCENES['el_vermeer'] = (() => {
    let plate, built = false;
    function build() {
      const a = P.canvas(), g = a.getContext('2d');
      g.fillStyle = grad(g, 420, 0, 1500, 0, [[0, '#d8d0b8'], [1, '#a89c80']]); g.fillRect(0, 0, W, H);
      g.fillStyle = '#e8f0f0'; poly(g, [[430, 120], [640, 150], [640, 620], [430, 660]]); g.fill();                     // janela à esquerda
      g.strokeStyle = '#5a4a30'; g.lineWidth = 6; for (let k = 1; k < 4; k++) { g.beginPath(); g.moveTo(430, 120 + k * 130); g.lineTo(640, 150 + k * 118); g.stroke(); } g.beginPath(); g.moveTo(535, 135); g.lineTo(535, 640); g.stroke();
      g.fillStyle = 'rgba(255,250,230,.35)'; poly(g, [[640, 150], [1500, 300], [1500, 900], [640, 620]]); g.fill();
      g.fillStyle = '#3a4a7a'; g.fillRect(1120, 200, 300, 220); g.strokeStyle = '#2a1a0a'; g.lineWidth = 14; g.strokeRect(1120, 200, 300, 220);   // mapa na parede
      // mesa com tapete oriental
      g.fillStyle = '#7a2a1e'; poly(g, [[560, 700], [1500, 690], [1540, H], [520, H]]); g.fill();
      for (let i = 0; i < 18; i++) { g.fillStyle = ['#c8962e', '#2a3a6a', '#e8dcc0'][i % 3]; g.fillRect(600 + i * 50, 730 + (i % 2) * 20, 30, 12); }
      g.fillStyle = '#f0ece0'; g.beginPath(); g.ellipse(760, 760, 90, 24, 0, 0, TAU); g.fill(); g.fillStyle = '#e8d8a0'; g.fillRect(740, 700, 40, 60);   // jarro
      g.fillStyle = '#1a1a1e'; g.save(); g.translate(1060, 820); g.rotate(-0.15); g.fillRect(-55, -100, 110, 200); g.restore();               // o celular
      return M.broken(a, { cell: 5, len: 9, wid: 5, passes: 2, angle: () => 1.3, seed: 61, jit: 8, skip: 0.02, sat: 1.08, warm: [255, 245, 220], cool: [120, 140, 170] });
    }
    function draw(c, lt) { if (!built) { plate = build(); built = true; } const t = Math.max(0, lt); c.drawImage(plate, 0, 0);
      const on = ease(0.3, 0.6, t), pul = on * (0.85 + 0.15 * Math.sin(t * 8));
      c.save(); c.translate(1060, 820); c.rotate(-0.15); c.fillStyle = `rgba(150,220,255,${pul})`; c.fillRect(-46, -90, 92, 180);
      c.fillStyle = `rgba(20,20,30,${on})`; c.fillRect(-36, -70, 72, 30); c.fillStyle = `rgba(61,220,132,${on})`; c.fillRect(-36, -30, 50, 10); c.restore();
      c.save(); c.globalCompositeOperation = 'lighter'; c.globalAlpha = pul * .5; c.fillStyle = radg(c, 1060, 820, 10, 260, [[0, '#a0e0ff'], [1, 'rgba(0,0,0,0)']]); c.fillRect(0, 0, W, H); c.restore();
      tela(c, 'canvas_el7', '#e8dcc8'); }
    return { draw };
  })();

  // ---------------------------------------------------------------- Chardin: o castelo de cartas sobe
  SCENES['el_chardin'] = (() => {
    let plate, built = false;
    const ANDAR = [0.2, 3.2, 4.9, 6.8, 7.7];               // tempos locais em que cada andar entra (sincronizados com a fala 7)
    function build() {
      const a = P.canvas(), g = a.getContext('2d');
      g.fillStyle = grad(g, 0, 0, W, H, [[0, '#4a4a32'], [0.6, '#2e2e20'], [1, '#1a1a12']]); g.fillRect(0, 0, W, H);
      g.fillStyle = radg(g, 700, 300, 20, 900, [[0, 'rgba(240,220,170,.35)'], [1, 'rgba(0,0,0,0)']]); g.fillRect(0, 0, W, H);
      g.fillStyle = grad(g, 0, 820, 0, H, [[0, '#7a5a34'], [1, '#3a2814']]); g.fillRect(0, 820, W, H - 820);              // mesa
      g.fillStyle = '#5a3a1e'; g.fillRect(0, 812, W, 14);
      g.fillStyle = '#c8a050'; g.beginPath(); g.ellipse(560, 900, 60, 16, 0, 0, TAU); g.fill();                               // moeda e gaveta entreaberta
      g.fillStyle = '#2a1a0a'; g.fillRect(1260, 880, 240, 90);
      return M.broken(a, { cell: 6, len: 10, wid: 6, passes: 2, angle: () => 0.8, seed: 71, jit: 8, skip: 0.02, sat: 1.0, warm: [250, 230, 190], cool: [80, 80, 70] });
    }
    function par(c, x, y, h, a2) {                           // duas cartas apoiadas em "V" invertido
      c.save(); c.globalAlpha = a2; for (const s of [-1, 1]) { c.save(); c.translate(x + s * h * 0.17, y - h / 2); c.rotate(s * 0.33);
        c.fillStyle = 'rgba(0,0,0,.3)'; c.fillRect(-h * .33 + 5, -h / 2 + 5, h * .66, h); c.fillStyle = s < 0 ? '#f2ead6' : '#e8dcc0'; c.fillRect(-h * .33, -h / 2, h * .66, h);
        c.strokeStyle = '#a03a2a'; c.lineWidth = 3; c.strokeRect(-h * .33 + 6, -h / 2 + 6, h * .66 - 12, h - 12); c.restore(); } c.restore(); }
    function draw(c, lt) { if (!built) { plate = build(); built = true; } const t = Math.max(0, lt); c.drawImage(plate, 0, 0);
      const h = 118, base = 800;
      ANDAR.forEach((t0, n) => { const k = ease(t0, t0 + 0.45, t); if (k <= 0) return; const cnt = 5 - n, y = base - n * (h + 8) - (1 - k) * 60;
        for (let i = 0; i < cnt; i++) { const x = 960 + (i - (cnt - 1) / 2) * 96; par(c, x, y, h, k); if (n > 0 || i < cnt - 1) { if (i < cnt - 1) { c.save(); c.globalAlpha = k; c.fillStyle = '#e0d4b8'; c.fillRect(x + 6, y - h - 4, 84, 8); c.restore(); } } } });
      c.save(); c.globalCompositeOperation = 'lighter'; c.globalAlpha = 0.1; c.fillStyle = radg(c, 760, 300, 20, 700, [[0, '#ffe8b0'], [1, 'rgba(0,0,0,0)']]); c.fillRect(0, 0, W, H); c.restore();
      tela(c, 'canvas_el8', '#e8dcc8'); }
    return { draw };
  })();

  // ---------------------------------------------------------------- Caillebotte: a rua molhada e as caixas
  SCENES['el_caillebotte'] = (() => {
    let plate, built = false;
    function build() {
      const a = P.canvas(), g = a.getContext('2d'), r = rng(707);
      g.fillStyle = grad(g, 0, 0, 0, 420, [[0, '#9aa4ac'], [1, '#c8ccc8']]); g.fillRect(0, 0, W, 420);
      g.fillStyle = '#c8bca4'; poly(g, [[700, 80], [1260, 80], [1260, 440], [700, 440]]); g.fill();                 // prédio em ponta (bico)
      for (let j = 0; j < 4; j++) for (let i = 0; i < 6; i++) { g.fillStyle = '#6a6a70'; g.fillRect(730 + i * 88, 110 + j * 78, 40, 54); }
      g.fillStyle = '#a89c88'; poly(g, [[380, 140], [700, 200], [700, 440], [380, 470]]); g.fill(); poly(g, [[1260, 200], [1540, 140], [1540, 470], [1260, 440]]); g.fill();
      g.fillStyle = grad(g, 0, 440, 0, H, [[0, '#8a8a88'], [1, '#6a6460']]); g.fillRect(0, 440, W, H - 440);
      g.strokeStyle = 'rgba(60,60,64,.35)'; g.lineWidth = 2; for (let y = 460; y < H; y += 18 + (y - 440) * 0.05) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }   // paralelepípedos
      for (let i = 0; i < 40; i++) { const x = r() * W, y = 460 + r() * 600; g.fillStyle = 'rgba(230,230,225,.25)'; g.fillRect(x, y, 30 + r() * 40, 3); }
      g.strokeStyle = '#2a2a2e'; g.lineWidth = 12; g.beginPath(); g.moveTo(1380, 1000); g.lineTo(1380, 380); g.stroke(); g.fillStyle = '#2a2a2e'; g.fillRect(1356, 350, 48, 40);   // poste
      return M.broken(a, { cell: 6, len: 12, wid: 5, passes: 2, angle: (x, y) => y > 440 ? 0.0 : 1.4, seed: 77, jit: 8, skip: 0.03, sat: 0.95, warm: [235, 230, 220], cool: [120, 130, 150] });
    }
    function draw(c, lt) { if (!built) { plate = build(); built = true; } const t = Math.max(0, lt); c.drawImage(plate, 0, 0);
      // figura de costas, com guarda-chuva, levando caixas de jogo; caminha para o fundo
      const k = ease(0, 4, t), s = lerp(1.0, 0.72, k), x = lerp(900, 980, k), y = lerp(1040, 900, k), pe = Math.sin(t * 6) * 6;
      c.save(); c.translate(x, y); c.scale(s, s);
      c.fillStyle = 'rgba(30,30,34,.3)'; c.beginPath(); c.ellipse(0, 10, 120, 18, 0, 0, TAU); c.fill();
      c.fillStyle = '#1e1e24'; c.fillRect(-46, -360, 92, 300); c.fillRect(-40, -60, 30, 64 + pe); c.fillRect(10, -60, 30, 64 - pe);   // casaco e pernas
      c.fillStyle = '#2a2420'; c.beginPath(); c.arc(0, -390, 30, 0, TAU); c.fill(); c.fillStyle = '#141418'; c.fillRect(-34, -440, 68, 40); c.fillRect(-48, -404, 96, 8);   // cartola
      const cx = ['#b8241c', '#2a5a9a', '#e0a020', '#3a8a4a'];
      cx.forEach((cor, i) => { c.fillStyle = cor; c.fillRect(30, -300 - i * 52, 140 - i * 10, 48); c.fillStyle = 'rgba(255,255,255,.35)'; c.fillRect(40, -292 - i * 52, 60, 8); });   // caixas empilhadas
      c.strokeStyle = '#1a1a1a'; c.lineWidth = 6; c.beginPath(); c.moveTo(-60, -260); c.lineTo(-70, -560); c.stroke();
      c.fillStyle = '#26262c'; c.beginPath(); c.moveTo(-300, -540); c.quadraticCurveTo(-70, -700, 160, -540); c.closePath(); c.fill();     // guarda-chuva
      c.restore();
      const r = rng(3 + Math.floor(t * 14)); c.strokeStyle = 'rgba(220,225,230,.35)'; c.lineWidth = 2;                                 // chuva
      for (let i = 0; i < 160; i++) { const xx = 380 + r() * 1180, yy = r() * H; c.beginPath(); c.moveTo(xx, yy); c.lineTo(xx - 6, yy + 26); c.stroke(); }
      tela(c, 'canvas_el9', '#e8dcc8'); }
    return { draw };
  })();

  // ---------------------------------------------------------------- de dia: o jogo montado e a cadeira vazia
  SCENES['el_mesa_dia'] = (() => {
    let plate, built = false;
    function build() {
      const a = P.canvas(), g = a.getContext('2d');
      g.fillStyle = grad(g, 0, 0, W, 0, [[0, '#f2e6c8'], [1, '#d8c8a0']]); g.fillRect(0, 0, W, H);
      g.fillStyle = '#fffaf0'; poly(g, [[440, 80], [760, 110], [760, 520], [440, 560]]); g.fill();                 // janela clara
      g.fillStyle = 'rgba(255,248,220,.5)'; poly(g, [[760, 110], [1500, 380], [1500, 1000], [760, 520]]); g.fill();
      g.fillStyle = '#8a5a30'; poly(g, [[420, 620], [1500, 620], [1580, H], [340, H]]); g.fill();                  // mesa
      g.fillStyle = '#3a6a5a'; poly(g, [[680, 660], [1240, 660], [1290, 900], [630, 900]]); g.fill();             // tabuleiro
      g.strokeStyle = 'rgba(240,230,200,.55)'; g.lineWidth = 3; for (let i = 1; i < 8; i++) { g.beginPath(); g.moveTo(680 + i * 70 - i * 6, 660); g.lineTo(630 + i * 82, 900); g.stroke(); } for (let j = 1; j < 4; j++) { g.beginPath(); g.moveTo(680 - j * 12, 660 + j * 60); g.lineTo(1240 + j * 12, 660 + j * 60); g.stroke(); }
      const pc = ['#b8241c', '#2a5a9a', '#e0c040', '#f2ead6'];
      for (let i = 0; i < 10; i++) { g.fillStyle = pc[i % 4]; const x = 720 + (i * 53) % 500, y = 700 + (i % 3) * 60; g.beginPath(); g.arc(x, y - 18, 11, 0, TAU); g.fill(); poly(g, [[x - 14, y + 10], [x + 14, y + 10], [x + 6, y - 10], [x - 6, y - 10]]); g.fill(); }   // peões
      [[1360, 760, .2, '#b8241c'], [1420, 800, -.1, 0]].forEach(([x, y, ro, f]) => carta(g, x, y, 80, 116, ro, f));
      // cadeira vazia do lado de cá, esperando
      g.fillStyle = '#5a3a1e'; g.fillRect(560, 820, 30, 260); g.fillRect(780, 820, 30, 260); g.fillRect(560, 800, 250, 40); g.fillRect(575, 840, 220, 18);
      g.fillStyle = '#a8301e'; g.fillRect(575, 860, 220, 120);
      return M.broken(a, { cell: 6, len: 12, wid: 6, passes: 2, angle: (x, y) => 0.9, seed: 87, jit: 10, skip: 0.03, sat: 1.1, warm: [255, 245, 215], cool: [140, 150, 170] });
    }
    function draw(c, lt) { if (!built) { plate = build(); built = true; } const t = Math.max(0, lt); c.drawImage(plate, 0, 0);
      const r = rng(5 + Math.floor(t * 8)); c.fillStyle = 'rgba(255,250,220,.6)'; for (let i = 0; i < 40; i++) c.fillRect(800 + r() * 600, 200 + r() * 500, 2, 2);
      // dois dados à espera, girando devagar no lugar
      for (const [x, y, ph] of [[1100, 950, 0], [1170, 940, 1.3]]) { c.save(); c.translate(x, y); c.rotate(Math.sin(t * 1.4 + ph) * 0.1); c.fillStyle = '#f6f0e0'; c.fillRect(-20, -20, 40, 40); c.fillStyle = '#1a1a1a'; [[-9, -9], [9, 9], [-9, 9], [9, -9]].forEach(([a2, b]) => { c.beginPath(); c.arc(a2, b, 4, 0, TAU); c.fill(); }); c.restore(); }
      tela(c, 'canvas_el10', '#e8dcc8'); }
    return { draw };
  })();
})();
