"""Gera os 7 posts da semana (PNG 1080x1350) e o arquivo de legendas.

Uso: python3 automacao/gerar_posts.py semanas/2026-s01.json saida/

O JSON de entrada segue o formato de semanas/2026-s01.json.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "fontes")
S = 2
W, H = 1080 * S, 1350 * S
LAR, TIN, PAP, CAR, SUA, CIN, LINHA_ESC, CLARO = "#FF5A1F", "#15120E", "#F7F2E8", "#FFFFFF", "#4A4037", "#B4A898", "#3A3229", "#E9DFD0"
LAR_TXT = "#C2410C"
HANDLE = "@baitatrendoficial"


def fonte(peso, tam):
    return ImageFont.truetype(os.path.join(FONTES, f"bricolage-grotesque-latin-{peso}-normal.woff"), int(tam * S))


def linhas(d, texto, f, largura):
    out, cur = [], ""
    for p in texto.split():
        t = (cur + " " + p).strip()
        if d.textlength(t, font=f) <= largura * S:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = p
    out.append(cur)
    return out


def bloco(d, x, y, texto, f, cor, largura, entrelinha):
    for ln in linhas(d, texto, f, largura):
        d.text((x * S, y * S), ln, font=f, fill=cor)
        y += entrelinha
    return y


def ajusta(d, texto, peso, tam, largura, max_linhas):
    """Diminui o corpo até o texto caber em max_linhas."""
    while tam > 40:
        f = fonte(peso, tam)
        if len(linhas(d, texto, f, largura)) <= max_linhas:
            return f, tam
        tam -= 4
    return fonte(peso, tam), tam


def direita(d, x_dir, y, texto, f, cor):
    d.text((x_dir * S - d.textlength(texto, font=f), y * S), texto, font=f, fill=cor)


def rodape(d, esq, cor_esq, cor_dir, cor_linha, y=1214):
    d.line([88 * S, (y - 24) * S, 992 * S, (y - 24) * S], fill=cor_linha, width=3 * S)
    f = fonte(500, 28)
    d.text((88 * S, y * S), esq, font=f, fill=cor_esq)
    direita(d, 992, y, HANDLE, f, cor_dir)


def foto_ou_vaga(img, d, caixa, foto, legenda, fundo, borda, cor_txt, raio=36):
    x0, y0, x1, y1 = [v * S for v in caixa]
    if foto and os.path.exists(foto):
        im = Image.open(foto).convert("RGB")
        bw, bh = x1 - x0, y1 - y0
        r = max(bw / im.width, bh / im.height)
        im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
        cx, cy = (im.width - bw) // 2, (im.height - bh) // 2
        im = im.crop((cx, cy, cx + bw, cy + bh))
        mask = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw, bh], radius=raio * S, fill=255)
        img.paste(im, (x0, y0), mask)
    else:
        d.rounded_rectangle([x0, y0, x1, y1], radius=raio * S, fill=fundo, outline=borda, width=4 * S)
        f = fonte(500, 30)
        tw = d.textlength(legenda, font=f)
        d.text(((x0 + x1) / 2 - tw / 2, (y0 + y1) / 2 - 18 * S), legenda, font=f, fill=cor_txt)


def play(d, x, y, cor_fundo, cor_icone):
    d.ellipse([x * S, y * S, (x + 60) * S, (y + 60) * S], fill=cor_fundo)
    d.polygon([((x + 24) * S, (y + 18) * S), ((x + 44) * S, (y + 30) * S), ((x + 24) * S, (y + 42) * S)], fill=cor_icone)


def salvar(img, caminho):
    img.resize((1080, 1350), Image.LANCZOS).save(caminho)


def card_destaque(s, saida):
    img = Image.new("RGB", (W, H), LAR); d = ImageDraw.Draw(img)
    d.text((72 * S, 76 * S), f"DESTAQUE DA SEMANA {s['numero']}", font=fonte(800, 30), fill=TIN)
    pil = s["periodo_curto"]; f = fonte(800, 28); tw = d.textlength(pil, font=f)
    d.rounded_rectangle([1008 * S - tw - 40 * S, 66 * S, 1008 * S, 116 * S], radius=25 * S, fill=TIN)
    d.text((1008 * S - tw - 20 * S, 74 * S), pil, font=f, fill=PAP)
    foto_ou_vaga(img, d, (72, 150, 1008, 690), s.get("foto"), "[ Foto do produto ]", PAP, TIN, SUA)
    f, tam = ajusta(d, s["produto"], 800, 96, 936, 2)
    y = bloco(d, 72, 724, s["produto"], f, TIN, 936, int(tam * 0.94))
    x, y = 72, y + 24
    fp = fonte(800, 32)
    for b in s["beneficios"][:2]:
        tw = d.textlength(b, font=fp)
        if x * S + tw + 48 * S > 1008 * S:
            x, y = 72, y + 76
        d.rounded_rectangle([x * S, y * S, x * S + tw + 48 * S, (y + 62) * S], radius=31 * S, fill=PAP)
        d.text((x * S + 24 * S, (y + 12) * S), b, font=fp, fill=TIN)
        x += tw / S + 64
    d.line([72 * S, 1164 * S, 1008 * S, 1164 * S], fill=TIN, width=3 * S)
    d.text((72 * S, 1184 * S), s["preco"], font=fonte(800, 56), fill=TIN)
    d.text((72 * S, 1254 * S), "#publi · link de afiliado na bio", font=fonte(500, 26), fill=TIN)
    direita(d, 1008, 1220, HANDLE, fonte(500, 30), TIN)
    salvar(img, os.path.join(saida, "1-seg-destaque.png"))


def capa_video(v, nome, saida, estilo):
    escuro = estilo == "escuro"
    claro = estilo == "claro"
    fundo = TIN if escuro else (PAP if claro else LAR)
    img = Image.new("RGB", (W, H), fundo); d = ImageDraw.Draw(img)
    txt = PAP if escuro else TIN
    vaga = CLARO if claro else "#2A241D"
    foto_ou_vaga(img, d, (0, 0, 1080, 720), v.get("frame_foto"), f"[ {v['frame']} ]", vaga, vaga, SUA if claro else CIN, raio=0)
    play(d, 56, 48, LAR, TIN)
    d.text((132 * S, 62 * S), f"VÍDEO · {v['duracao'].upper()}", font=fonte(800, 30), fill=LAR_TXT if claro else LAR)
    f, tam = ajusta(d, v["titulo"], 800, 120, 936, 2)
    y = bloco(d, 72, 776, v["titulo"], f, txt, 936, int(tam * 0.9))
    bloco(d, 72, y + 24, v["subtitulo"], fonte(500, 38), CLARO if escuro else TIN, 936, 48)
    rodape(d, "#publi · link na bio", CIN if escuro else TIN, txt, LINHA_ESC if escuro else TIN)
    salvar(img, os.path.join(saida, nome))


def card_porque(s, saida):
    p = s["porque"]
    img = Image.new("RGB", (W, H), PAP); d = ImageDraw.Draw(img)
    d.text((80 * S, 88 * S), "POR QUE ESTÁ EM ALTA", font=fonte(800, 30), fill=LAR_TXT)
    f, tam = ajusta(d, p["titulo"], 800, 92, 920, 2)
    y = bloco(d, 80, 140, p["titulo"], f, TIN, 920, int(tam * 0.95)) + 36
    d.rounded_rectangle([80 * S, y * S, 1000 * S, (y + 230) * S], radius=32 * S, fill=LAR)
    fn = fonte(800, 150); d.text((120 * S, (y + 30) * S), p["numero"], font=fn, fill=TIN)
    nx = 120 + d.textlength(p["numero"], font=fn) / S + 36
    bloco(d, nx, y + 50, p["numero_texto"], fonte(800, 38), TIN, 1000 - nx - 40, 46)
    y += 252
    for it in p["itens"][:2]:
        d.rounded_rectangle([80 * S, y * S, 1000 * S, (y + 170) * S], radius=32 * S, fill=CAR)
        yy = bloco(d, 124, y + 30, it["titulo"], fonte(800, 44), TIN, 840, 50)
        bloco(d, 124, yy + 8, it["texto"], fonte(500, 30), SUA, 840, 38)
        y += 190
    bloco(d, 80, 1220, "Fontes: " + p["fontes"], fonte(500, 22), SUA, 640, 28)
    direita(d, 1000, 1236, HANDLE, fonte(500, 30), TIN)
    salvar(img, os.path.join(saida, "3-qua-por-que-esta-em-alta.png"))


def card_checklist(s, saida):
    c = s["checklist"]
    img = Image.new("RGB", (W, H), TIN); d = ImageDraw.Draw(img)
    d.text((80 * S, 88 * S), "SALVA ESSE POST", font=fonte(800, 30), fill=LAR)
    f, tam = ajusta(d, c["titulo"], 800, 100, 920, 3)
    y = bloco(d, 80, 140, c["titulo"], f, PAP, 920, int(tam * 0.93)) + 44
    fb, fr = fonte(800, 40), fonte(500, 40)
    for it in c["itens"][:4]:
        d.rounded_rectangle([80 * S, (y + 6) * S, 132 * S, (y + 58) * S], radius=14 * S, outline=LAR, width=5 * S)
        d.line([(92 * S, (y + 32) * S), (104 * S, (y + 44) * S), (122 * S, (y + 20) * S)], fill=LAR, width=5 * S, joint="curve")
        texto = it["forte"] + " " + it["texto"]
        ls = linhas(d, texto, fr, 820)
        yy = y
        for i, ln in enumerate(ls):
            if i == 0 and ln.startswith(it["forte"]):
                d.text((164 * S, yy * S), it["forte"], font=fb, fill=PAP)
                resto = ln[len(it["forte"]):]
                d.text((164 * S + d.textlength(it["forte"], font=fb), yy * S), resto, font=fr, fill=PAP)
            else:
                d.text((164 * S, yy * S), ln, font=fr, fill=PAP)
            yy += 50
        y = yy + 30
    rodape(d, "O destaque da semana tem link na bio · #publi", CIN, PAP, LINHA_ESC)
    salvar(img, os.path.join(saida, "5-sex-antes-de-comprar.png"))


def card_ultima(s, saida):
    img = Image.new("RGB", (W, H), LAR); d = ImageDraw.Draw(img)
    d.text((80 * S, 88 * S), f"DOMINGO · FIM DA SEMANA {s['numero']}", font=fonte(800, 30), fill=TIN)
    fu, _ = ajusta(d, "Última chamada.", 800, 128, 920, 1)
    d.text((80 * S, 140 * S), "Última chamada.", font=fu, fill=TIN)
    y = 330
    d.rounded_rectangle([80 * S, y * S, 1000 * S, (y + 324) * S], radius=32 * S, fill=PAP)
    foto_ou_vaga(img, d, (112, y + 32, 372, y + 292), s.get("foto"), "[ foto ]", PAP, TIN, SUA)
    f, tam = ajusta(d, s["produto"], 800, 50, 580, 3)
    yy = bloco(d, 404, y + 50, s["produto"], f, TIN, 580, int(tam * 1.0))
    d.text((404 * S, (yy + 16) * S), s["preco"], font=fonte(800, 44), fill=LAR_TXT)
    bloco(d, 80, 720, "O link continua na bio. Segunda que vem tem destaque novo.", fonte(500, 44), TIN, 920, 54)
    rodape(d, "#publi · link de afiliado", TIN, TIN, TIN)
    salvar(img, os.path.join(saida, "7-dom-ultima-chamada.png"))


def legendas(s, saida):
    dias = [("Seg", "Destaque da semana", "Card", "12h"), ("Ter", s["videos"][0]["titulo"], "Vídeo", "19h"),
            ("Qua", "Por que está em alta", "Card", "12h"), ("Qui", s["videos"][1]["titulo"], "Vídeo", "19h"),
            ("Sex", "Antes de comprar, confira", "Card", "12h"), ("Sáb", s["videos"][2]["titulo"], "Vídeo", "11h"),
            ("Dom", "Última chamada", "Card", "19h")]
    out = [f"# Semana {s['numero']} · {s['produto']}", "", f"{s['periodo_longo']} · link: {s.get('link') or '[link de afiliado]'}", ""]
    for dia, tit, fmt, hora in dias:
        out += [f"## {dia} · {tit} ({fmt}, {hora})", "", s["legendas"][dia].strip(), ""]
    out += ["## Roteiros dos vídeos", ""]
    for v in s["videos"]:
        out += [f"### {v['dia']} · {v['titulo']} ({v['duracao']})", ""]
        out += [f"- {cena}" for cena in v["roteiro"]] + [""]
    with open(os.path.join(saida, "legendas.md"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(out))


def main():
    entrada, saida = sys.argv[1], sys.argv[2]
    os.makedirs(saida, exist_ok=True)
    s = json.load(open(entrada, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(entrada))
    for k in ("foto",):
        if s.get(k):
            s[k] = os.path.join(base, s[k])
    for v in s["videos"]:
        if v.get("frame_foto"):
            v["frame_foto"] = os.path.join(base, v["frame_foto"])
    card_destaque(s, saida)
    capa_video(s["videos"][0], "2-ter-video-capa.png", saida, "escuro")
    card_porque(s, saida)
    capa_video(s["videos"][1], "4-qui-video-capa.png", saida, "laranja")
    card_checklist(s, saida)
    capa_video(s["videos"][2], "6-sab-video-capa.png", saida, "claro")
    card_ultima(s, saida)
    legendas(s, saida)
    print("ok:", saida)


if __name__ == "__main__":
    main()
