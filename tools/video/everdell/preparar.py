"""Narração montada e palavras com tempo absoluto -> hf/assets."""
import json, subprocess
LEAD = 0.15
GAP = {1: .25, 2: .25, 3: .25, 4: .25, 5: .25, 6: .3, 7: .25, 8: .3, 9: .3}
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout)
t, falas, ent, filt, words = LEAD, [], [], [], []
for i in range(1, 11):
    p = f"voz/proc/fala{i}.wav"; d = dur(p)
    ent += ["-i", p]; filt.append(f"[{i-1}]adelay={int(t*1000)}|{int(t*1000)}[a{i-1}]")
    falas.append({"fala": i, "inicio": round(t, 3), "fim": round(t + d, 3)})
    for w in json.load(open(f"voz/stt/fala{i}.json"))["words"]:
        if w["type"] == "word": words.append({"fala": i, "w": w["text"], "s": round(t + w["start"], 3), "e": round(t + w["end"], 3)})
    t += d + GAP.get(i, 0)
TOTAL = round(t + 1.6, 2)
fc = ";".join(filt) + ";" + "".join(f"[a{k}]" for k in range(10)) + f"amix=inputs=10:normalize=0,apad,atrim=0:{TOTAL}[out]"
subprocess.run(["ffmpeg","-v","error","-y",*ent,"-filter_complex",fc,"-map","[out]","-ar","48000","hf/assets/audio/narracao.wav"],check=True)
json.dump({"total": TOTAL, "falas": falas, "palavras": words}, open("hf/assets/data/tempos.json","w"), ensure_ascii=False, indent=1)
print("total", TOTAL); [print(f) for f in falas]
