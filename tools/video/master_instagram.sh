set -e
export DO_NOT_TRACK=1 PRODUCER_HEADLESS_SHELL_PATH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
HF=/home/user/hf-tools/node_modules/.bin/hyperframes
for v in "video-ttr como-se-joga-ticket-to-ride" "video-everdell como-se-joga-everdell"; do
  set -- $v; D=/home/user/$1; N=$2
  cd $D/hf && $HF render --fps 60 --crf 8 -o $D/bruto60.mp4 2>&1 | grep -E "rendered|rror" || true
  cd $D && ffmpeg -v error -y -i bruto60.mp4 \
    -c:v libx264 -preset slow -tune animation -crf 14 -maxrate 25M -bufsize 50M -profile:v high -level:v 4.2 -pix_fmt yuv420p \
    -g 120 -keyint_min 60 -sc_threshold 0 -r 60 -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
    -af "loudnorm=I=-14.5:TP=-2:LRA=11,alimiter=limit=0.83:level=disabled,aresample=48000" -ar 48000 -c:a aac -b:a 320k -movflags +faststart ${N}-IG.mp4
  echo "OK $N"
done
