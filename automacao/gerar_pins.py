"""Pins do Pinterest (1000x1500, sem preço, que muda) a partir de testes/pinterest-AAAA-sNN.json.

Uso: python3 automacao/gerar_pins.py testes/pinterest-2026-s03.json
Fotos: testes/fotos/<semana dos testes>/<id>.jpg. Saída: saida/pinterest-AAAA-sNN/<id>.jpg
"""
import glob, json, os, sys
from PIL import Image, ImageDraw
from gerar_stories import fonte, quebra, LAR, TIN, PAP, SUA

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
W, H = 1000, 1500

def foto(pid):
    for f in glob.glob(os.path.join(RAIZ, "testes", "fotos", "*", f"{pid}.jpg")):
        return f

def pin(p):
    im = Image.new("RGB", (W, H), PAP); d = ImageDraw.Draw(im)
    f = foto(p["id"]); alt = 930
    if f:
        ph = Image.open(f).convert("RGB"); prop = W / alt
        w, h = (ph.width, round(ph.width / prop)) if ph.width / ph.height < prop else (round(ph.height * prop), ph.height)
        ph = ph.crop(((ph.width - w) // 2, (ph.height - h) // 2, (ph.width + w) // 2, (ph.height + h) // 2)).resize((W, alt))
        im.paste(ph, (0, 0))
    y = alt + 50
    for tam in (78, 70, 62, 56):
        ft = fonte(800, tam); lt = quebra(d, p["gancho"], ft, W - 120)
        if len(lt) <= 3: break
    for ln in lt:
        d.text((60, y), ln, font=ft, fill=TIN); y += tam + 8
    y += 14
    fa = fonte(500, 40)
    for ln in quebra(d, p["apoio"], fa, W - 120)[:2]:
        d.text((60, y), ln, font=fa, fill=SUA); y += 50
    yb = H - 150
    d.rounded_rectangle([60, yb, W - 60, yb + 100], radius=50, fill=LAR)
    fb = fonte(800, 44); t = "Ver na Shopee"
    d.text(((W - d.textlength(t, font=fb)) / 2, yb + 24), t, font=fb, fill=TIN)
    d.text((60, H - 40), "baitatrend.com.br · #publi link de afiliado", font=fonte(500, 26), fill=SUA)
    return im

def main():
    arq = sys.argv[1]; s = json.load(open(arq, encoding="utf-8"))
    out = os.path.join(RAIZ, "saida", "pinterest-" + s["semana"]); os.makedirs(out, exist_ok=True)
    for p in s["pins"]:
        pin(p).save(os.path.join(out, f"{p['id']}.jpg"), quality=90)
    print(len(s["pins"]), "pins em", out)

if __name__ == "__main__":
    main()
