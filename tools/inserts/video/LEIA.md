# Vídeo de montagem e desmontagem

1. `python3 exportar.py`: gera `cena.json` com todas as peças já na posição da caixa. Usa o projeto, as bandejas do
   js500 do pacote e as pilhas de carta.
2. `npm install three@0.160.0`, depois copie `node_modules/three/build/three.module.min.js` para `three.js`.
3. `node gravar.js 30`: renderiza `cena.html` no Chromium headless, quadro a quadro, em `frames/`.
4. `ffmpeg -framerate 30 -i frames/%05d.png -c:v libx264 -pix_fmt yuv420p -crf 20 insert.mp4`

Os caminhos em `exportar.py` apontam para a pasta de rascunho da sessão; ajuste a variável `S`.

## Vídeo do setup na mesa

1. `python3 setup_layout.py`: calcula onde cada peça fica na mesa em volta do tabuleiro (720 x 520 mm) e grava
   `setup.json`.
2. `node gravar2.js 30 "" setup.html frames_s 8769`: renderiza os quadros.
3. `ffmpeg -framerate 30 -i frames_s/%05d.png -c:v libx264 -pix_fmt yuv420p -crf 20 setup.mp4`
