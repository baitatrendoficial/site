"""Gera os vídeos curtos da semana (MP4 1080x1920, sem áudio) a partir das fotos e do roteiro.

Uso: python3 automacao/gerar_videos.py semanas/2026-s01.json saida/

Cada linha do roteiro com "texto: ..." vira uma cena; as fotos da semana se alternam com zoom lento.
A última cena é o card final com preço e #publi. Precisa do ffmpeg instalado.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "fontes")
W, H, FPS = 1080, 1920, 24
LAR, TIN, PAP = "#FF5A1F", "#15120E", "#F7F2E8"
HANDLE = "@baitatrendoficial"


def fonte(peso, tam):
    return ImageFont.truetype(os.path.join(FONTES, f"bricolage-grotesque-latin-{peso}-normal.woff"), tam)


def quebra(d, texto, f, largura):
    linhas, cur = [], ""
    for p in texto.split():
        t = (cur + " " + p).strip()
        if d.textlength(t, font=f) <= largura:
            cur = t
        else:
            if cur:
                linhas.append(cur)
            cur = p
    linhas.append(cur)
    return linhas


def fundo(foto):
    """Foto quadrada no centro sobre a própria foto desfocada, preenchendo 9:16."""
    im = Image.open(foto).convert("RGB")
    bg = im.resize((H, H)).crop(((H - W) // 2, 0, (H - W) // 2 + W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (W, H), TIN), 0.35)
    return bg, im


def cena_foto(foto, texto, n_frames, topo):
    bg, im = fundo(foto)
    f = fonte(800, 112)
    d0 = ImageDraw.Draw(bg)
    linhas = quebra(d0, texto, f, W - 160)
    quadros = []
    for k in range(n_frames):
        z = 1.0 + 0.08 * k / max(1, n_frames - 1)
        lado = int(W * z)
        fr = bg.copy()
        foto_z = im.resize((lado, lado))
        off = (lado - W) // 2
        fr.paste(foto_z.crop((off, off, off + W, off + W)), (0, 380))
        d = ImageDraw.Draw(fr)
        d.text((80, 140), topo, font=fonte(800, 44), fill=PAP)
        y = 1540
        caixa_h = 60 + len(linhas) * 118
        d.rounded_rectangle([56, y - 40, W - 56, y - 40 + caixa_h], radius=36, fill=LAR)
        for ln in linhas:
            d.text((96, y), ln, font=f, fill=TIN)
            y += 118
        fh = fonte(500, 40)
        d.text((W - 80 - d.textlength(HANDLE, font=fh), 146), HANDLE, font=fh, fill=PAP)
        quadros.append(fr)
    return quadros


def cena_final(s, n_frames):
    fr = Image.new("RGB", (W, H), LAR)
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle([80, 260, 260, 440], radius=44, fill=TIN)
    fb = fonte(800, 140)
    bb = d.textbbox((0, 0), "b", font=fb)
    d.text((170 - (bb[2] - bb[0]) / 2 - bb[0], 350 - (bb[3] - bb[1]) / 2 - bb[1] - 8), "b", font=fb, fill=PAP)
    y = 620
    for ln in quebra(d, s["produto"], fonte(800, 104), W - 160):
        d.text((80, y), ln, font=fonte(800, 104), fill=TIN)
        y += 110
    d.text((80, y + 50), s["preco"], font=fonte(800, 150), fill=PAP)
    d.text((80, y + 260), "Link na bio", font=fonte(800, 72), fill=TIN)
    d.text((80, H - 260), "#publi · link de afiliado", font=fonte(500, 44), fill=TIN)
    d.text((80, H - 190), HANDLE, font=fonte(500, 44), fill=TIN)
    return [fr] * n_frames


def main():
    arq, saida = sys.argv[1], sys.argv[2]
    s = json.load(open(arq, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(arq))
    fotos = [os.path.join(base, "fotos", os.path.splitext(os.path.basename(arq))[0], f"{n}.jpg") for n in range(1, 10)]
    fotos = [f for f in fotos if os.path.exists(f)]
    if not fotos:
        sys.exit("sem fotos baixadas para esta semana")
    os.makedirs(saida, exist_ok=True)
    nomes = {"Ter": "2-ter-video.mp4", "Qui": "4-qui-video.mp4", "Sáb": "6-sab-video.mp4"}
    for i, v in enumerate(s["videos"]):
        textos = [r.split("texto:")[-1].strip() for r in v["roteiro"] if "texto:" in r]
        textos = [t for t in textos if "Link na bio" not in t and "[" not in t]
        quadros = []
        for j, t in enumerate(textos):
            quadros += cena_foto(fotos[(i + j) % len(fotos)], t, int(FPS * 2.4), v["titulo"].upper())
        quadros += cena_final(s, int(FPS * 3))
        with tempfile.TemporaryDirectory() as tmp:
            for k, q in enumerate(quadros):
                q.save(os.path.join(tmp, f"{k:05d}.jpg"), quality=90)
            destino = os.path.join(saida, nomes.get(v["dia"], f"video-{i + 1}.mp4"))
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "%05d.jpg"),
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "21", "-movflags", "+faststart", destino], check=True)
        print("vídeo:", destino, f"{len(quadros) / FPS:.1f}s")


if __name__ == "__main__":
    main()
