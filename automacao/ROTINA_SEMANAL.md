# Rotina semanal do Baita Trend

A tarefa agendada roda **toda sexta às 8h57** (Brasília) e prepara a semana que começa na segunda seguinte.
Ela segue este roteiro. Nada vai ao ar sem o "aprovado" do Cassiano.

Contas: tudo em `baitatrendoficial` (Gmail, Instagram, TikTok, Shopee Afiliados, Amazon Associados `baitatrendofi-20`,
Mercado Livre Afiliados, Metricool). O Chrome do Cassiano já está logado nelas.

## 1. Pesquisar o produto (sem perguntar nada)

Objetivo: 1 produto com **três sinais** ao mesmo tempo.

1. **Busca subindo:** Google Trends Brasil (últimos 90 dias), notícias e sazonalidade (clima, datas como Dia das Crianças,
   Black Friday, Natal, volta às aulas, calor/frio).
2. **Vídeo viralizando:** TikTok Creative Center (produtos e hashtags em alta no Brasil), Reels, "achadinhos".
3. **Vendendo nas lojas:** mais vendidos da Shopee, do Mercado Livre (API do hub de afiliados, filtro `best_seller`)
   e da Amazon Brasil.

Filtros obrigatórios:
- Preço entre R$ 20 e R$ 200, nota ≥ 4,5, pelo menos 1 mil vendidos no anúncio escolhido.
- Não repetir produto ou categoria das últimas 4 semanas (ver `dados.json` → `historico`).
- Fora: remédios, suplementos, cosméticos com promessa de saúde, armas, itens adultos, apostas, réplicas de marca.
- Preferir anúncio de loja oficial ou com muitas avaliações com foto.

Anote os números de cada sinal com a fonte. Eles vão para `sinais` e para o card de quarta.

## 2. Gerar os links de afiliado (Chrome)

- Shopee: painel de afiliados → "Obter Link em Massa", subId `semana`. Não usar a API GQL (bloqueio anti-robô).
- Mercado Livre: linkbuilder do programa de afiliados → link `meli.la`.
- Amazon: `https://www.amazon.com.br/dp/ASIN?tag=baitatrendofi-20` (sem preço nem foto da Amazon, regra deles).
- Nunca clicar no próprio link para comprar.

## 3. Escrever a semana

Crie `semanas/AAAA-sNN.json` copiando o formato de `semanas/2026-s01.json` (número = semana anterior + 1,
`inicio` = segunda, `fim` = domingo). Regras de texto:
- Português do Brasil, tom direto e amigável, sem exagero ("melhor do mundo", "imperdível").
- Só afirmar o que está no anúncio ou nas fontes. Nada de "testamos" se não testamos.
- Toda legenda de produto termina com `#publi Link de afiliado.` (exigência do CONAR). Quarta é o card de contexto.
- Nunca escreva "link na bio": o TikTok ainda não tem link clicável. Use "Link no perfil: baitatrend.com.br".
- Não copiar avaliações de compradores nem vídeos do vendedor. Fotos do anúncio vão em `fotos_site` (URLs diretas).
- Os vídeos usam as fotos do produto com legendas; o roteiro só pode descrever o que a foto mostra.
- Atualize também a vitrine se algum produto dela saiu do ar.

## 4. Gerar e conferir

```
git checkout -b semana-NN
git add semanas/AAAA-sNN.json && git commit -m "Semana NN: <produto>" && git push -u origin semana-NN
# espere o workflow "Baixar fotos da semana" terminar (1–2 min) e então:
git pull
python3 automacao/preparar_semana.py semanas/AAAA-sNN.json
git add -A && git commit -m "Semana NN: posts, vídeos e site" && git push
```

Abra cada PNG e um frame de cada vídeo antes de seguir. Confira preço e link abrindo o anúncio.

## 5. Pedir aprovação

Mande para o Cassiano (notificação no celular) um resumo curto:
produto, preço, loja, os 3 sinais com números, link do anúncio, e os arquivos gerados
(prévia via `https://raw.githubusercontent.com/baitatrendoficial/site/semana-NN/saida/AAAA-sNN/<arquivo>`).
Pare aqui e espere. Se ele pedir ajuste, ajuste e mande de novo.

## 6. Depois do "aprovado"

1. `git push origin semana-NN:aprovada/semana-NN` e apague a `semana-NN`. O workflow "Publicar semana aprovada"
   põe o site no ar na segunda 00h05. Não junte na `main` antes disso (o produto atual ainda está em destaque).
2. Agende tudo no Metricool pelo conector "Metricool Social Media Management" (brand 7328590, fuso America/Sao_Paulo),
   com `createScheduledPost`. Mídia por URL pública da branch:
   `https://raw.githubusercontent.com/baitatrendoficial/site/aprovada/semana-NN/saida/AAAA-sNN/<arquivo>`.
   Se o conector não estiver disponível, use o Metricool pelo Chrome (aba visível, recarregar se travar).

   a) Os 7 posts (Instagram + TikTok), legendas de `saida/AAAA-sNN/legendas.md`:

| Dia | Hora | Arquivo | Instagram |
|---|---|---|---|
| Seg | 12h | 1-seg-destaque.png | POST |
| Ter | 19h | 2-ter-video.mp4 | REEL |
| Qua | 12h | 3-qua-por-que-esta-em-alta.png | POST |
| Qui | 19h | 4-qui-video.mp4 | REEL |
| Sex | 12h | 5-sex-antes-de-comprar.png | POST |
| Sáb | 11h | 6-sab-video.mp4 | REEL |
| Dom | 19h | 7-dom-ultima-chamada.png | POST |

   Cards: `tiktokData` com `autoAddMusic: true` e `title`. Vídeos: Instagram `type: REEL`.
   `commercialContentThirdParty` e `commercialContentOwnBrand` sempre false.

   b) Reforço, a partir de `saida/AAAA-sNN/reforco.json`:
   - `stories`: 21 stories (9h, 15h, 21h), só Instagram, `instagramData.type: STORY`, sem texto.
   - `tiktok_extra`: 1 TikTok por dia às 17h (foto do story da tarde, em .jpg: o TikTok recusa PNG), com `title`, `text` e `autoAddMusic: true`.

   Confira depois com `getScheduledPosts` que entraram 35 itens (7 + 21 + 7).
3. Se o Metricool recusar por limite do plano, pare e avise o Cassiano com as opções (plano pago, só uma rede, manual).
4. Mostre a agenda da semana preenchida e encerre.

## Decisões

- Selo "Parceria paga" (Conteúdo comercial) no TikTok: **sempre desligado** (decisão do Cassiano em 12/10/2026).
  A divulgação fica pelo #publi na legenda e no card.
