"""Prepara tudo de uma semana a partir do JSON: confere o conteúdo, gera posts, vídeos e atualiza o site.

Uso: python3 automacao/preparar_semana.py semanas/2026-s02.json

Precisa das fotos já baixadas em semanas/fotos/<semana>/ (o workflow "Baixar fotos da semana"
faz isso sozinho quando o JSON é enviado ao GitHub). Sai com erro e explica o que falta.
"""
import json, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
OBRIGATORIOS = ["numero", "inicio", "fim", "periodo_curto", "periodo_longo", "produto", "beneficios", "preco",
                "link", "loja", "foto", "porque_site", "sinais", "porque", "checklist", "videos", "legendas",
                "fotos_site", "beneficios_site"]


def conferir(s, nome):
    erros = []
    for k in OBRIGATORIOS:
        if not s.get(k):
            erros.append(f"campo vazio ou ausente: {k}")
    if not re.fullmatch(r"\d{4}-s\d{2}", nome):
        erros.append(f"nome do arquivo deve ser AAAA-sNN.json (veio {nome})")
    if s.get("preco") and not re.fullmatch(r"R\$ \d{1,3}(\.\d{3})*,\d{2}", s["preco"]):
        erros.append(f"preço fora do formato 'R$ 27,00': {s['preco']}")
    if s.get("link") and not s["link"].startswith("https://"):
        erros.append("link de afiliado precisa começar com https://")
    leg = s.get("legendas") or {}
    for d in DIAS:
        if d not in leg:
            erros.append(f"falta legenda de {d}")
        elif d != "Qua" and "#publi" not in leg[d]:
            erros.append(f"legenda de {d} sem #publi (obrigatório em post de produto)")
    if len(s.get("videos") or []) != 3:
        erros.append("precisa de exatamente 3 vídeos (Ter, Qui, Sáb)")
    if len(s.get("fotos_site") or []) < 3:
        erros.append("precisa de pelo menos 3 fotos em fotos_site")
    return erros


def main():
    arq = sys.argv[1]
    nome = os.path.splitext(os.path.basename(arq))[0]
    s = json.load(open(arq, encoding="utf-8"))
    erros = conferir(s, nome)
    pasta_fotos = os.path.join(RAIZ, "semanas", "fotos", nome)
    if not os.path.isdir(pasta_fotos) or not os.listdir(pasta_fotos):
        erros.append(f"fotos ainda não baixadas em semanas/fotos/{nome}/ (espere o workflow e dê git pull)")
    if erros:
        print("Não dá para preparar a semana:")
        for e in erros:
            print(" -", e)
        sys.exit(1)
    saida = os.path.join(RAIZ, "saida", nome)
    py = sys.executable
    subprocess.run([py, os.path.join(AQUI, "gerar_posts.py"), arq, saida], check=True)
    subprocess.run([py, os.path.join(AQUI, "gerar_videos.py"), arq, saida], check=True)
    subprocess.run([py, os.path.join(AQUI, "atualizar_site.py"), arq], check=True)
    print(f"Pronto: posts e vídeos em saida/{nome}/, site atualizado (dados.js).")


if __name__ == "__main__":
    main()
