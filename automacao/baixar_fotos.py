"""Baixa as fotos listadas em "fotos_site" de cada semanas/*.json para semanas/fotos/<semana>/.

Roda no GitHub Actions (que tem acesso livre à internet). Só baixa o que ainda não existe.
"""
import glob, json, os, urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for arq in sorted(glob.glob(os.path.join(RAIZ, "semanas", "*.json"))):
    s = json.load(open(arq, encoding="utf-8"))
    nome = os.path.splitext(os.path.basename(arq))[0]
    pasta = os.path.join(RAIZ, "semanas", "fotos", nome)
    for n, url in enumerate(s.get("fotos_site") or [], 1):
        destino = os.path.join(pasta, f"{n}.jpg")
        if os.path.exists(destino):
            continue
        os.makedirs(pasta, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r, open(destino, "wb") as fp:
            fp.write(r.read())
        print("baixou", destino)
