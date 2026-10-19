"""Monta um vídeo da semana a partir de uma cena gerada por IA (ex.: Gemini/Veo, 9:16).

Uso: python3 automacao/video_ia.py semanas/2026-s02.json saida/2026-s02/ia-ventilador-sala.mp4 Ter

Sobre a cena entram: título no topo, as frases do roteiro do dia ("texto: ...") divididas
igualmente no tempo, e o aviso fixo "Cena ilustrativa gerada por IA". No fim, o mesmo card final
dos outros vídeos (preço, baitatrend.com.br, #publi). Mantém o som da cena. Precisa do ffmpeg.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gerar_videos import W, H, FPS, LAR, TIN, PAP, HANDLE, fonte, quebra, cena_final

NOMES = {"Ter": "2-ter-video.mp4", "Qui": "4-qui-video.mp4", "Sáb": "6-sab-video.mp4"}
AVISO = "Cena ilustrativa gerada por IA"


def overlay(titulo, texto):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 230], fill=(21, 18, 14, 150))
    d.text((80, 140), titulo.upper(), font=fonte(800, 44), fill=PAP)
    fh = fonte(500, 40)
    d.text((W - 80 - d.textlength(HANDLE, font=fh), 146), HANDLE, font=fh, fill=PAP)
    f = fonte(800, 104)
    linhas = quebra(d, texto, f, W - 160)
    y = 1370
    d.rounded_rectangle([56, y - 40, W - 56, y - 40 + 60 + len(linhas) * 112], radius=36, fill=LAR)
    for ln in linhas:
        d.text((96, y), ln, font=f, fill=TIN)
        y += 112
    fa = fonte(500, 34)
    tw = d.textlength(AVISO, font=fa)
    d.rounded_rectangle([W - 80 - tw - 28, H - 150, W - 80 + 4, H - 92], radius=20, fill=(21, 18, 14, 170))
    d.text((W - 80 - tw - 12, H - 143), AVISO, font=fa, fill=PAP)
    return im


def main():
    arq, cena, dia = sys.argv[1], sys.argv[2], sys.argv[3]
    s = json.load(open(arq, encoding="utf-8"))
    v = next(x for x in s["videos"] if x["dia"] == dia)
    textos = [r.split("texto:")[-1].strip() for r in v["roteiro"] if "texto:" in r]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", cena],
                               capture_output=True, text=True, check=True).stdout)
    saida = os.path.join(os.path.dirname(cena), NOMES[dia])
    with tempfile.TemporaryDirectory() as tmp:
        entradas, filtros, ant = ["-i", cena], [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}[b0]"], "b0"
        passo = dur / len(textos)
        for i, t in enumerate(textos):
            p = os.path.join(tmp, f"o{i}.png")
            overlay(v["titulo"], t).save(p)
            entradas += ["-i", p]
            filtros.append(f"[{ant}][{i + 1}:v]overlay=0:0:enable='between(t,{i * passo:.2f},{(i + 1) * passo:.2f})'[b{i + 1}]")
            ant = f"b{i + 1}"
        fim = os.path.join(tmp, "fim.png")
        cena_final(s, 1)[0].save(fim)
        entradas += ["-loop", "1", "-t", "3", "-i", fim, "-f", "lavfi", "-t", "3", "-i", "anullsrc=r=48000:cl=stereo"]
        k = len(textos) + 1
        filtros.append(f"[{k}:v]fps={FPS},format=yuv420p[fim]")
        filtros.append(f"[{ant}]format=yuv420p[cena]")
        filtros.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo[a0]")
        filtros.append(f"[cena][a0][fim][{k + 1}:a]concat=n=2:v=1:a=1[v][a]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entradas, "-filter_complex", ";".join(filtros),
                        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", saida], check=True)
    print("vídeo IA:", saida)


if __name__ == "__main__":
    main()
