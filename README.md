# Baita Trend — site

Site estático publicado em https://baitatrend.com.br pelo GitHub Pages.

O conteúdo do site fica em `dados.json` e `dados.js`, gerados por `automacao/atualizar_site.py`.

## Automação semanal

- `semanas/AAAA-sNN.json`: conteúdo de cada semana (produto, sinais, textos dos 7 posts, legendas e roteiros).
- `python3 automacao/gerar_posts.py semanas/2026-s01.json saida/`: gera os 7 posts em PNG (1080×1350) e `legendas.md`.
- `python3 automacao/atualizar_site.py semanas/2026-s01.json`: põe a semana no destaque do site e manda a anterior para o histórico (grava `dados.json` e `dados.js`).
- Fotos do produto, quando houver, ficam em `semanas/fotos/` e são referenciadas no JSON (`foto` para os cards, `foto_site` para o site).

Fluxo: a tarefa semanal cria uma branch `semana-NN` com o JSON e os posts gerados. Depois da aprovação, a branch entra na `main` e o site atualiza sozinho.
