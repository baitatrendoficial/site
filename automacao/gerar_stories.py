"""Gera os stories da semana (PNG 1080x1920) e o roteiro de reforço: 3 stories por dia + 1 TikTok extra por dia.

Uso: python3 automacao/gerar_stories.py semanas/2026-s01.json saida/2026-s01/

Saída: stories/<dia>-<n>.png e reforco.json (o que agendar, em que dia e hora, e com qual texto).
Os textos saem só do JSON da semana (produto, preço, nota, vendidos, benefícios, sinais).
"""
import json, os, sys
from datetime import date, timedelta
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, "fontes")
W, H = 1080, 1920
LAR, TIN, PAP, SUA = "#FF5A1F", "#15120E", "#F7F2E8", "#4A4037"
HANDLE = "@baitatrendoficial"
DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
NOMES = {"Seg": "seg", "Ter": "ter", "Qua": "qua", "Qui": "qui", "Sex": "sex", "Sáb": "sab", "Dom": "dom"}
HORAS = ["09:00", "15:00", "21:00"]
HORA_TIKTOK = "17:00"


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


def curto(txt, n=70):
    """Primeira parte de um benefício, para caber grande no story."""
    txt = txt.split(";")[0]
    for sep in [",", " para ", " que "]:
        if len(txt) > n and sep in txt:
            txt = txt.split(sep)[0]
    return txt.strip().rstrip(".")


def maiuscula(txt):
    return txt[:1].upper() + txt[1:]


def story(foto, etiqueta, titulo, apoio, preco, cor_fundo=PAP, destaque=None):
    im = Image.new("RGB", (W, H), cor_fundo)
    escuro = cor_fundo == TIN
    texto = PAP if escuro else TIN
    d = ImageDraw.Draw(im)
    # faixa de cima (fica abaixo da barra do Instagram)
    d.text((72, 230), etiqueta.upper(), font=fonte(800, 40), fill=LAR if not escuro else LAR)
    fh = fonte(500, 34)
    d.text((W - 72 - d.textlength(HANDLE, font=fh), 236), HANDLE, font=fh, fill=SUA if not escuro else "#B4A898")
    # foto quadrada com cantos arredondados
    y = 320
    alt_foto = 560 if destaque else 760
    if foto:
        f = Image.open(foto).convert("RGB")
        # recorta no formato da caixa (936 x alt_foto) sem esticar a foto
        prop = 936 / alt_foto
        w, h = (f.width, round(f.width / prop)) if f.width / f.height < prop else (round(f.height * prop), f.height)
        f = f.crop(((f.width - w) // 2, (f.height - h) // 2, (f.width + w) // 2, (f.height + h) // 2)).resize((936, alt_foto))
        m = Image.new("L", f.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, f.width, f.height], radius=48, fill=255)
        im.paste(f, (72, y), m)
        y += alt_foto + 56
    if destaque:
        fd = fonte(800, 220)
        d.text((72, y - 30), destaque, font=fd, fill=LAR)
        y += 220
    limite = H - 400 - 40
    for tam in (84, 76, 68, 60, 54):
        ft, fa = fonte(800, tam), fonte(500, 44)
        lt = quebra(d, titulo, ft, W - 144)
        la = quebra(d, apoio, fa, W - 144) if apoio else []
        alt = len(lt) * (tam + 8) + (18 + len(la) * 56 if la else 0)
        if y + alt <= limite:
            break
    for ln in lt:
        d.text((72, y), ln, font=ft, fill=texto)
        y += tam + 8
    if la:
        y += 18
        for ln in la:
            d.text((72, y), ln, font=fa, fill=SUA if not escuro else "#E9DFD0")
            y += 56
    # rodapé: preço + link na bio (acima da área de resposta do story)
    yb = H - 400
    d.rounded_rectangle([72, yb, W - 72, yb + 150], radius=40, fill=LAR)
    fp = fonte(800, 64)
    d.text((112, yb + 38), preco, font=fp, fill=TIN)
    fl = fonte(800, 50)
    t = "baitatrend.com.br"
    d.text((W - 112 - d.textlength(t, font=fl), yb + 48), t, font=fl, fill=TIN)
    fpub = fonte(500, 32)
    d.text((72, yb + 175), "#publi · link de afiliado", font=fpub, fill=SUA if not escuro else "#B4A898")
    return im


def main():
    arq, saida = sys.argv[1], sys.argv[2]
    s = json.load(open(arq, encoding="utf-8"))
    nome = os.path.splitext(os.path.basename(arq))[0]
    base = os.path.dirname(os.path.abspath(arq))
    fotos = [os.path.join(base, "fotos", nome, f"{n}.jpg") for n in range(1, 10)]
    fotos = [f for f in fotos if os.path.exists(f)] or [None]
    foto = lambda i: fotos[i % len(fotos)]
    pasta = os.path.join(saida, "stories")
    os.makedirs(pasta, exist_ok=True)

    prod, preco, loja = s["produto"], s["preco"], s["loja"]
    ben = [curto(b) for b in s.get("beneficios_site") or s["beneficios"]]
    prova = f"Nota {s['nota']} de 5 e {s['vendidos']} vendidos na {loja}" if s.get("nota") and s.get("vendidos") else f"Avaliações com foto na {loja}"
    sinal = s["sinais"][0]
    inicio = date.fromisoformat(s["inicio"])

    # (etiqueta, título, apoio, fundo, destaque) para manhã / tarde / noite de cada dia
    plano = {
        "Seg": [("Destaque da semana", prod, "O produto que está em alta agora.", PAP, None),
                ("Por que está em alta", maiuscula(sinal["fonte"]), None, TIN, sinal["valor"]),
                ("Fica até domingo", "7 dias como destaque do Baita Trend", "Link no perfil: baitatrend.com.br", PAP, None)],
        "Ter": [("Bom dia", prod, ben[0], PAP, None),
                ("Quem comprou aprovou", prova, None, TIN, None),
                ("Ainda dá tempo", "6 dias como destaque", "Link no perfil: baitatrend.com.br", PAP, None)],
        "Qua": [("Bom dia", prod, ben[1 % len(ben)], PAP, None),
                ("Por que está em alta", maiuscula(s["sinais"][1]["fonte"]), None, TIN, s["sinais"][1]["valor"] if len(s["sinais"][1]["valor"]) <= 6 else None),
                ("Ainda dá tempo", "5 dias como destaque", "Link no perfil: baitatrend.com.br", PAP, None)],
        "Qui": [("Bom dia", prod, ben[2 % len(ben)], PAP, None),
                ("Detalhe que faz diferença", ben[3 % len(ben)], None, TIN, None),
                ("Ainda dá tempo", "4 dias como destaque", "Link no perfil: baitatrend.com.br", PAP, None)],
        "Sex": [("Sextou", prod, ben[4 % len(ben)], PAP, None),
                ("Quem comprou aprovou", prova, None, TIN, None),
                ("Fim de semana chegando", "3 dias como destaque", "Link no perfil: baitatrend.com.br", PAP, None)],
        "Sáb": [("Bom dia", prod, ben[0], PAP, None),
                ("Antes de comprar", "Confira as avaliações com foto no anúncio", None, TIN, None),
                ("Amanhã é o último dia", prod, "Depois ele sai do destaque.", PAP, None)],
        "Dom": [("Último dia", prod, "Hoje é o último dia como destaque.", PAP, None),
                ("Quem comprou aprovou", prova, None, TIN, None),
                ("Segunda tem produto novo", "Qual produto você quer ver aqui?", "Responde este story.", PAP, None)],
    }

    reforco = {"stories": [], "tiktok_extra": []}
    k = 0
    for i, dia in enumerate(DIAS):
        dt = inicio + timedelta(days=i)
        for j, (etq, tit, apoio, fundo, dest) in enumerate(plano[dia]):
            arqp = f"{NOMES[dia]}-{j + 1}.png"
            im = story(foto(k), etq, tit, apoio, preco, fundo, dest)
            im.save(os.path.join(pasta, arqp), optimize=True)
            if j == 1:  # o TikTok só aceita foto em JPEG ou WebP
                im.save(os.path.join(pasta, arqp[:-4] + ".jpg"), quality=90)
            k += 1
            reforco["stories"].append({"data": f"{dt.isoformat()}T{HORAS[j]}:00", "arquivo": f"stories/{arqp}"})
        # TikTok extra do dia: o story da tarde como foto, com música e legenda curta
        etq, tit = plano[dia][1][0], plano[dia][1][1]
        reforco["tiktok_extra"].append({
            "data": f"{dt.isoformat()}T{HORA_TIKTOK}:00",
            "arquivo": f"stories/{NOMES[dia]}-2.jpg",
            "titulo": f"{prod}: {etq.lower()}"[:90],
            "texto": f"{tit}. {prod} por {preco}, link no perfil: baitatrend.com.br\n\n#publi Link de afiliado.\n#baitatrend #achadinhos #emalta",
        })
    with open(os.path.join(saida, "reforco.json"), "w", encoding="utf-8") as fp:
        json.dump(reforco, fp, ensure_ascii=False, indent=2)
    print(f"stories: {len(reforco['stories'])} · tiktok extra: {len(reforco['tiktok_extra'])} → {saida}")


if __name__ == "__main__":
    main()
