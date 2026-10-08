"""Coloca uma semana no destaque do site e manda a anterior para o histórico.

Uso: python3 automacao/atualizar_site.py semanas/2026-s01.json

Lê e grava dados.json e gera dados.js, que o index.html carrega.
"""
import json, os, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(RAIZ, "dados.json")


def para_site(s):
    v = s["videos"]
    return {
        "exemplo": False,
        "numero": s["numero"],
        "inicio": s["inicio"],
        "fim": s["fim"],
        "produto": s["produto"],
        "porque": s["porque_site"],
        "sinais": s["sinais"],
        "preco": s["preco"],
        "link": s.get("link") or "#",
        "loja": s.get("loja", "Shopee"),
        "foto": s.get("foto_site"),
        "posts": [
            {"dia": "Seg", "formato": "card", "tema": "Apresentação do produto"},
            {"dia": "Ter", "formato": "video", "tema": v[0]["titulo"]},
            {"dia": "Qua", "formato": "card", "tema": "Por que está em alta"},
            {"dia": "Qui", "formato": "video", "tema": v[1]["titulo"]},
            {"dia": "Sex", "formato": "card", "tema": "Antes de comprar, confira"},
            {"dia": "Sáb", "formato": "video", "tema": v[2]["titulo"]},
            {"dia": "Dom", "formato": "card", "tema": "Última chamada"},
        ],
    }


def main():
    s = json.load(open(sys.argv[1], encoding="utf-8"))
    dados = json.load(open(DADOS, encoding="utf-8")) if os.path.exists(DADOS) else {"semana_atual": None, "historico": []}
    atual = dados.get("semana_atual")
    nova = para_site(s)
    if atual and not atual.get("exemplo") and atual["numero"] != nova["numero"]:
        if not any(h["numero"] == atual["numero"] for h in dados["historico"]):
            dados["historico"].insert(0, {k: atual[k] for k in ("numero", "inicio", "fim", "produto", "preco", "link", "loja")})
    dados["semana_atual"] = nova
    with open(DADOS, "w", encoding="utf-8") as fp:
        json.dump(dados, fp, ensure_ascii=False, indent=2)
    with open(os.path.join(RAIZ, "dados.js"), "w", encoding="utf-8") as fp:
        fp.write("window.BAITA = " + json.dumps(dados, ensure_ascii=False, indent=2) + ";\n")
    print(f"Site: semana {nova['numero']} no destaque, {len(dados['historico'])} semana(s) no histórico.")


if __name__ == "__main__":
    main()
