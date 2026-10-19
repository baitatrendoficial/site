"""Produtos de teste: 1 imagem 1080x1920 por produto (TikTok foto + story do Instagram) e a seção "Testando agora" da vitrine.

Uso: python3 automacao/gerar_testes.py testes/2026-s02.json

Fotos: testes/fotos/<semana>/<id>.jpg (o workflow "Baixar fotos da semana" baixa ao enviar o JSON).
Saída: saida/testes-<semana>/<id>.jpg e agenda.json (o que agendar); atualiza vitrine.js.
"""
import json, os, re, sys
from gerar_stories import story, PAP, TIN

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CAT = "Testando agora"


def main():
    arq = sys.argv[1]
    t = json.load(open(arq, encoding="utf-8"))
    nome = os.path.splitext(os.path.basename(arq))[0]
    fotos = os.path.join(RAIZ, "testes", "fotos", nome)
    saida = os.path.join(RAIZ, "saida", f"testes-{nome}")
    os.makedirs(saida, exist_ok=True)
    agenda = []
    for n, it in enumerate(t["itens"]):
        f = os.path.join(fotos, f"{it['id']}.jpg")
        im = story(f if os.path.exists(f) else None, "Achado do dia", it["gancho"], it["apoio"], it["preco"],
                   PAP if n % 2 == 0 else TIN)
        im.save(os.path.join(saida, f"{it['id']}.jpg"), quality=90)
        agenda.append({
            "data": it["data"], "id": it["id"], "arquivo": f"{it['id']}.jpg",
            "titulo": it["gancho"][:90],
            "texto": f"{it['gancho']} {it['nome']}, {it['preco']} na {it['loja']}. {it['apoio']}.\n\n"
                     f"Link no perfil: baitatrend.com.br (seção Testando agora)\n\n#publi Link de afiliado.\n#baitatrend #achadinhos #shopee",
        })
    json.dump(agenda, open(os.path.join(saida, "agenda.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # vitrine: troca os itens de teste antigos pelos desta semana, no topo
    vj = os.path.join(RAIZ, "vitrine.js")
    V = json.loads(re.sub(r"^window\.VITRINE = |;\s*$", "", open(vj, encoding="utf-8").read().strip()))
    V["itens"] = [i for i in V["itens"] if i.get("categoria") != CAT]
    novos = [{"id": it["id"], "categoria": CAT, "nome": it["nome"], "preco": it["preco"], "nota": it["nota"],
              "vendas": it["vendas"], "link": it["link"], "loja": it["loja"], "img": it["img"]} for it in t["itens"]]
    V["itens"] = novos + V["itens"]
    V["categorias"] = [CAT] + [c for c in V["categorias"] if c != CAT]
    open(vj, "w", encoding="utf-8").write("window.VITRINE = " + json.dumps(V, ensure_ascii=False) + ";\n")
    print(f"testes: {len(agenda)} imagens em {saida}, vitrine com {len(novos)} itens em '{CAT}'")


if __name__ == "__main__":
    main()
