"""Monta vitrine.json com os produtos da Vitrine (dados do painel de afiliados da Shopee, 08/10/2026).

Uso: python3 automacao/vitrine_s01.py
"""
import json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = "https://down-tx-br.img.susercontent.com/"
CONSULTA = "2026-10-08"

# id, categoria, nome curto, preço, vendas, link de afiliado, arquivo da imagem
P = [
    ("20699758504", "Dias de chuva", "Guarda-chuva automático abre e fecha, cabe na bolsa", "27,00", "20 mil+", "https://s.shopee.com.br/9fLW5xRxSL", None),
    ("58262746825", "Dias de chuva", "Guarda-chuva compacto anti-vento com lanterna", "32,00", "1 mil+", "https://s.shopee.com.br/50ZgZ8SEG5", "br-11134207-820mb-mqo88pve6q6bd7.webp"),
    ("23199568947", "Dias de chuva", "Kit 2 capas de chuva transparentes", "25,89", "2 mil+", "https://s.shopee.com.br/4B0ZZbVOws", "br-11134207-820lu-mtdzzccvfw8y07.webp"),
    ("58251353658", "Dias de chuva", "Varal de chão dobrável para apartamento (12 kg)", "59,90", "30 mil+", "https://s.shopee.com.br/1gJEb0ev17", "br-11134207-81z1k-mhqf3kve4phd06.webp"),
    ("58266942513", "Dias de chuva", "Varal torre 3 andares com rodinhas", "72,95", "1 mil+", "https://s.shopee.com.br/1VzoOhfYM6", "sg-11134201-8259n-msmk8aozxp1id9.webp"),

    ("23993134058", "Casa e cozinha", "Kit 5 utensílios de silicone para cozinha", "21,50", "40 mil+", "https://s.shopee.com.br/905pKUD08C", "br-11134201-820lq-mqycsqf1ph528c.webp"),
    ("22894944958", "Casa e cozinha", "Utensílios de silicone antiaderente", "18,61", "3 mil+", "https://s.shopee.com.br/BUQoFkd3i", "br-11134207-820me-mneaqb9op8n481.webp"),
    ("23497309877", "Casa e cozinha", "Espremedor de frutas elétrico recarregável", "61,99", "80 mil+", "https://s.shopee.com.br/Lnr0Yjzij", "sg-11134201-8259f-msgkvfvn2sju02.webp"),
    ("58251614409", "Casa e cozinha", "Copo térmico 1200 ml com tampa e canudo", "34,68", "80 mil+", "https://s.shopee.com.br/8AWiKxGAp1", "br-11134207-820l7-msdnnzmmtpfp25.webp"),
    ("23293962531", "Casa e cozinha", "Copo térmico 1200 ml com alça e canudo de metal", "52,99", "1 mil+", "https://s.shopee.com.br/9pewK19pRR", "br-11134207-7r98o-m9fx32anh92x9e.webp"),
    ("23698786124", "Casa e cozinha", "Garrafa térmica inox com capa de silicone", "31,99", "9 mil+", "https://s.shopee.com.br/AAHmid8Ylb", "br-11134207-820m5-mt00jk3e0eme7b.webp"),
    ("22694069772", "Casa e cozinha", "Amolador de facas e tesouras elétrico", "27,89", "5 mil+", "https://s.shopee.com.br/qk7bTi5hu", "sg-11134201-7rdx6-mdl9t8sxuafp32.webp"),
    ("20999602504", "Casa e cozinha", "Mini seladora portátil de embalagens", "15,99", "20 mil+", "https://s.shopee.com.br/1LgOCOgBh5", "sg-11134201-8227w-mhpvjye8mozkc6.webp"),
    ("23594149969", "Casa e cozinha", "Kit 5 caixas organizadoras com tampa", "79,90", "20 mil+", "https://s.shopee.com.br/2VsLaXbkKK", "br-11134207-820lj-mqvxcnrv84joe4.webp"),
    ("58260237454", "Casa e cozinha", "Percarbonato de sódio Calisul, tira-manchas sem cloro", "39,90", "8 mil+", "https://s.shopee.com.br/2LYvOEcNfJ", "br-11134207-820mf-ms6z4y7egao720.webp"),

    ("22892833180", "Ferramentas", "Jogo de chaves catraca 46 peças com maleta", "28,99", "400 mil+", "https://s.shopee.com.br/8fSyvsEGoA", "br-11134207-820l9-mqt86n8incape7.webp"),
    ("8716065733", "Ferramentas", "Kit de ferramentas 200 peças com maleta", "29,90", "20 mil+", "https://s.shopee.com.br/9V25vPB67P", "br-11134207-820l6-mpmp8kzjbrpf13.webp"),
    ("58217601055", "Ferramentas", "Parafusadeira e furadeira 25V sem fio com maleta", "89,99", "2 mil+", "https://s.shopee.com.br/AUud7F7I5d", "br-11134207-820lt-msq8pkzchmh355.webp"),

    ("22499247158", "Tecnologia", "Mini power bank 10.000 mAh", "31,99", "10 mil+", "https://s.shopee.com.br/1B0bwlGOh", "sg-11134201-81zvk-mik9ovwbhszk62.webp"),
    ("19899586753", "Tecnologia", "Fone sem fio Bluetooth com estojo", "42,89", "100 mil+", "https://s.shopee.com.br/1qcenJeHg8", "sg-11134201-7rffm-m4f5wo6pi7mjaa.webp"),
    ("20997608223", "Tecnologia", "Caixa de som Bluetooth 30W com LED", "106,97", "100 mil+", "https://s.shopee.com.br/9Kifj6BjSM", "br-11134207-7r98o-lqo1mmf95gcjc2.webp"),
    ("58207657402", "Tecnologia", "Caixa de som Bluetooth resistente à água (IPX6)", "64,90", "3 mil+", "https://s.shopee.com.br/gQhPAij2t", "br-11134207-820m9-mm9qmldg6rcw4b.webp"),
    ("58267259992", "Tecnologia", "Lâmpada LED recarregável para camping", "30,90", "2 mil+", "https://s.shopee.com.br/40h9NIW2Hr", "br-11134207-820l4-msw6d8dl81s70b.webp"),

    ("42655559896", "Beleza", "Kit 15 pincéis de maquiagem com esponjas", "60,00", "100 mil+", "https://s.shopee.com.br/9APFWnCMnF", "sg-11134201-823p7-mp4n4y19ucjyf9.webp"),
    ("18699185302", "Beleza", "Espelho de maquiagem com luz LED dobrável", "25,00", "10 mil+", "https://s.shopee.com.br/AKbCuw7vQa", "br-11134207-820lo-msy0r6ajzv9j75.webp"),
    ("42809403599", "Beleza", "Escova de silicone para lavar o cabelo", "16,95", "90 mil+", "https://s.shopee.com.br/9zyMWK9C6Y", "sg-11134201-8259f-mq36i3vp58nha7.webp"),
    ("20103606180", "Beleza", "Máquina de barbear e aparador 3 em 1", "48,47", "100 mil+", "https://s.shopee.com.br/W7HCrjMNk", "04527aa2d9d6a2e8d2b68d715f079947.webp"),
    ("45504824205", "Beleza", "Cílios postiços volume reutilizáveis", "9,72", "60 mil+", "https://s.shopee.com.br/113XnmhSMv", "sg-11134201-82599-mrjvqd3a22o214.webp"),
    ("47663635933", "Beleza", "Cera capilar em bastão anti-frizz", "19,99", "6 mil+", "https://s.shopee.com.br/20w4zcdeLH", "cn-11134207-820l4-mqeiyd5s893655.webp"),
    ("22094238842", "Beleza", "Body splash Ayra 100 ml", "25,00", "8 mil+", "https://s.shopee.com.br/30ocBSZqJV", "br-11134207-820m8-mm0ga7dwj4zo9f.webp"),
    ("51008479378", "Beleza", "Sombra em bastão à prova d'água", "11,00", "4 mil+", "https://s.shopee.com.br/3B82NlZCyW", "sg-11134301-82606-mmbmhybciayw16.webp"),
    ("22993854099", "Beleza", "Cabine UV de unhas com presilha de mesa", "19,99", "4 mil+", "https://s.shopee.com.br/2qVBz9aTeU", "br-11134207-820m2-mp33hdqvrta840.webp"),
    ("55713085679", "Beleza", "Touca de cetim para dormir", "11,99", "2 mil+", "https://s.shopee.com.br/2gBlmqb6zT", "cn-11134207-820l4-ms1avpb2677p5b.webp"),
    ("12682371475", "Beleza", "Kit Belkit banho de verniz (4 itens)", "12,84", "3 mil+", "https://s.shopee.com.br/2BFVBvd10I", "0b71142df0dd7b510644a4003a2c524a.webp"),

    ("19497692224", "Moda", "Kit 2 camisetas masculinas caneladas", "49,90", "50 mil+", "https://s.shopee.com.br/9fLW7iASmO", "br-11134207-81z1k-me1r8fnxc2dc92.webp"),
    ("58261247758", "Moda", "Moletom canguru unissex forrado", "66,94", "2 mil+", "https://s.shopee.com.br/8pmP8BDdTD", "sg-11134201-823py-mokpxs5ucl4y67.webp"),
    ("22898300477", "Moda", "Kit 3 cropped canelados de algodão", "39,90", "2 mil+", "https://s.shopee.com.br/4fwqAWTUw3", "br-11134207-7r98o-m991mmyo36rm1f.webp"),
    ("42470077703", "Moda", "Vestido midi canelado com costas trançadas", "47,90", "3 mil+", "https://s.shopee.com.br/5q8nYfP3ZI", "br-11134207-81z1k-mf8j74vixhc624.webp"),
    ("58207994286", "Moda", "Conjunto cropped e short-saia com fivela", "59,00", "3 mil+", "https://s.shopee.com.br/5fpNMMPguH", "br-11134207-820m2-mmhi7z0vj2tj02.webp"),
    ("22693482981", "Moda", "Macaquinho tubinho com zíper", "29,00", "1 mil+", "https://s.shopee.com.br/5VVxA3QKFG", "br-11134207-820m9-moy63ohpbg9128.webp"),
    ("23293531456", "Moda", "Conjunto alfaiataria regata e short", "79,99", "5 mil+", "https://s.shopee.com.br/5LCWxkQxaF", "br-11134207-81z1k-mfnscfwycwzr8b.webp"),
    ("23398057558", "Moda", "Saída de praia de tricô rendada", "28,00", "2 mil+", "https://s.shopee.com.br/5At6lRRav6", "br-11134207-820li-mses6ow5r7k75e.webp"),

    ("23694205612", "Fitness", "Conjunto fitness legging e top", "65,90", "10 mil+", "https://s.shopee.com.br/1BMy05gp1w", "br-11134201-820lr-mu2phi62akg2c0.webp"),
    ("23899192132", "Fitness", "Camisetão oversized de algodão para treino", "37,79", "5 mil+", "https://s.shopee.com.br/4LJzluUlbt", "br-11134207-81z1k-mi0i2ig6u0hu04.webp"),
    ("58215914612", "Fitness", "Macaquinho fitness costas abertas", "39,90", "2 mil+", "https://s.shopee.com.br/4qGGMpSrb4", "br-11134207-820m4-mrq7zqfsk9ae36.webp"),
    ("26095396567", "Fitness", "Mini trampolim jump para exercícios", "159,99", "1 mil+", "https://s.shopee.com.br/4VdPyDU8Gu", "sg-11134201-825av-mqz5ojv4n4sk03.webp"),

    ("58268341942", "Infantil", "Squishy dumpling antiestresse", "27,90", "5 mil+", "https://s.shopee.com.br/3VksmNXwIg", "br-11134207-820mg-mtlipl366olc4d.webp"),
    ("50410432912", "Infantil", "Escova de dentes infantil retrátil de bichinho", "13,88", "5 mil+", "https://s.shopee.com.br/3LRSa4YZdf", "sg-11134201-822y3-mo6szyskaqdca1.webp"),
    ("58201188371", "Infantil", "Andador empurrador musical educativo", "122,99", "9 mil+", "https://s.shopee.com.br/3g4IygXIxh", "br-11134207-81z1k-mhlw12dngn46c0.webp"),
    ("20297976747", "Infantil", "Bomba tira-leite automática", "39,89", "10 mil+", "https://s.shopee.com.br/3qNjAzWfci", "br-11134207-7r98o-m1zrew60x93z0f.webp"),
]

ORDEM = ["Dias de chuva", "Casa e cozinha", "Ferramentas", "Tecnologia", "Beleza", "Moda", "Fitness", "Infantil"]

itens = [{
    "id": i, "categoria": c, "nome": n, "preco": "R$ " + p, "vendas": v,
    "link": l, "loja": "Shopee", "img": (IMG + f) if f else None,
} for i, c, n, p, v, l, f in P]

out = {"consultado_em": CONSULTA, "categorias": ORDEM, "itens": itens}
with open(os.path.join(RAIZ, "vitrine.json"), "w", encoding="utf-8") as fp:
    json.dump(out, fp, ensure_ascii=False, indent=2)
with open(os.path.join(RAIZ, "vitrine.js"), "w", encoding="utf-8") as fp:
    fp.write("window.VITRINE = " + json.dumps(out, ensure_ascii=False) + ";\n")
print(len(itens), "itens")
