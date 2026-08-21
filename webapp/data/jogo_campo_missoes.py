"""
Conteúdo das Ordens de Serviço do "Simulador de Campo" (jogo de treinamento
na tela Início). Cada missão é uma O.S. com 4 decisões (cenário + pergunta +
3 alternativas, uma correta). A lógica do jogo em si fica em
webapp/services/jogo_campo.py — aqui só o conteúdo.

Este é o lote inicial (3 O.S., adaptadas do protótipo de referência) — o
conteúdo cresce conforme situações reais de campo forem repassadas. Cada
O.S. nova é só mais um item nesta lista; não precisa mudar nada no motor
do jogo (webapp/services/jogo_campo.py) para adicionar mais.
"""

MISSOES = [
    {
        "id": "OS-48219",
        "bairro": "Bairro Liberdade",
        "titulo": "Instalação Nova — Fibra Óptica",
        "cliente": "Sr. Antônio Ferreira",
        "equipamento": "ONT Huawei EG8145",
        "briefing": "Cliente contratou o plano de 300 Mega. É a primeira instalação de fibra na casa dele — antes só usava internet do celular.",
        "instrumento": "optic",
        "decisoes": [
            {
                "cena": "Você chega com o cordão de fibra (pigtail) pronto para conectar na ONT Huawei EG8145. Na parte de trás do equipamento você vê uma entrada óptica com trava SC/APC (verde), quatro portas LAN (amarelas), entrada de energia e botão WPS.",
                "pergunta": "Em qual porta você conecta o conector de fibra?",
                "opcoes": [
                    {"texto": "Na porta óptica marcada como PON (conector verde SC/APC)", "correta": True,
                     "feedback": "Isso mesmo. A porta PON é a única entrada óptica da ONT — é por ela que chega o sinal da operadora. As portas LAN (amarelas) são para cabo de rede, nunca para fibra."},
                    {"texto": "Em qualquer porta LAN, já que todas fazem a mesma função", "correta": False,
                     "feedback": "As portas LAN são elétricas (RJ45), feitas para cabo de rede — o conector óptico simplesmente não encaixa nelas. Forçar pode danificar conector e porta."},
                    {"texto": "Na porta de energia, porque é a única com trava de segurança", "correta": False,
                     "feedback": "A porta de energia é exclusiva para a fonte da ONT. Conectar fibra ali não teria efeito nenhum, só atrasaria a instalação."},
                ],
            },
            {
                "cena": "Com a fibra conectada e a ONT ligada na tomada, você observa o painel de LEDs: PON (verde piscando), LOS (vermelho aceso), PWR (verde fixo).",
                "pergunta": "O LED LOS aceso em vermelho indica o quê?",
                "opcoes": [
                    {"texto": "Loss of Signal — perda de sinal óptico, algo está impedindo a luz de chegar corretamente", "correta": True,
                     "feedback": "Exato. LOS significa 'Loss of Signal'. Pode ser conector sujo, dobra excessiva no cabo ou rompimento na rede externa. Antes de mexer na configuração, vale limpar o conector e checar a rota da fibra."},
                    {"texto": "Que a ONT está em modo de espera (standby) e é só aguardar 10 minutos", "correta": False,
                     "feedback": "Esse 'standby' não existe nesse contexto — o LED vermelho de LOS é um alerta ativo de problema no sinal óptico, não um estado normal de espera."},
                    {"texto": "Que o cliente ultrapassou a franquia de dados do plano", "correta": False,
                     "feedback": "Franquia de dados é questão de plano/sistema, não aparece como alerta físico no equipamento. LOS é sempre sobre o sinal óptico em si."},
                ],
            },
            {
                "cena": "Você limpa o conector com o kit de limpeza e reconecta. O LOS apaga. Agora você usa o medidor óptico para conferir a potência do sinal antes de liberar o atendimento.",
                "pergunta": "O medidor mostra -19 dBm. O que você faz?",
                "opcoes": [
                    {"texto": "Segue com a instalação — está dentro da faixa considerada ideal para GPON (cerca de -8 a -27 dBm)", "correta": True,
                     "feedback": "Isso mesmo. -19 dBm está confortavelmente dentro da faixa ideal. Sinal perto demais de 0 dBm pode saturar o receptor, e abaixo de -27 dBm normalmente já não é suficiente. Ele está bem no meio — situação ótima."},
                    {"texto": "Cancela a instalação, porque qualquer número negativo indica problema", "correta": False,
                     "feedback": "Sinal óptico sempre é medido em números negativos (escala logarítmica) — isso é normal. O que importa é estar dentro da faixa aceitável, não o sinal ser negativo."},
                    {"texto": "Liga para o NOC pedindo para aumentar a potência do sinal na CTO", "correta": False,
                     "feedback": "Não é necessário — -19 dBm já está dentro do intervalo ideal. Pedir mais potência sem necessidade pode saturar o receptor de outros clientes na mesma rede."},
                ],
            },
            {
                "cena": "O cliente pede para você passar o cabo de fibra em uma quina bem apertada atrás do rack de TV, dobrando quase 90 graus, para 'esconder o fio'.",
                "pergunta": "Como você lida com esse pedido?",
                "opcoes": [
                    {"texto": "Explica que a fibra precisa de uma curva suave (raio mínimo de curvatura) e sugere uma rota alternativa, ainda discreta", "correta": True,
                     "feedback": "Correto. Fibra óptica não é como cabo elétrico — dobras muito fechadas causam microfraturas internas que degradam o sinal aos poucos, às vezes só semanas depois. Vale negociar uma rota com curva suave."},
                    {"texto": "Atende o pedido do cliente, já que o importante é deixar ele satisfeito hoje", "correta": False,
                     "feedback": "O cliente ficaria satisfeito na hora, mas o serviço provavelmente teria uma nova chamada em algumas semanas por perda de sinal — retrabalho e frustração maior depois."},
                    {"texto": "Recusa o pedido e diz que não é possível esconder o cabo de forma nenhuma", "correta": False,
                     "feedback": "É possível sim esconder o cabo — só não pode ser com dobra fechada. Canaletas e contornos suaves resolvem sem prejudicar o sinal."},
                ],
            },
        ],
    },
    {
        "id": "OS-51004",
        "bairro": "Bairro Panorama",
        "titulo": "Wi-Fi e Configuração do Roteador",
        "cliente": "Dona Marlene",
        "equipamento": "ONT Huawei EG8145 + roteador do cliente",
        "briefing": "Instalação já concluída no mês passado. Chamado aberto por 'internet caindo direto' — Dona Marlene usa um roteador próprio ligado depois da ONT.",
        "instrumento": "wifi",
        "decisoes": [
            {
                "cena": "Dona Marlene pede: 'Bota uma senha fácil, tipo o meu nome mesmo, pra eu não esquecer.'",
                "pergunta": "Como você orienta ela sobre a senha do Wi-Fi?",
                "opcoes": [
                    {"texto": "Sugere uma senha com pelo menos 8 caracteres, misturando letras e números, e anota num papel pra ela guardar perto do roteador", "correta": True,
                     "feedback": "Boa! Só o nome dela é fácil demais de adivinhar por vizinhos. O ideal é equilibrar segurança com praticidade — simples de lembrar, mas não óbvia."},
                    {"texto": "Usa o nome dela mesmo, já que é isso que ela pediu", "correta": False,
                     "feedback": "Atender ao pé da letra aqui cria risco real: rede fácil de adivinhar pode significar internet lenta pra ela e uso indevido pelo qual ela seria responsável."},
                    {"texto": "Gera uma senha aleatória de 20 caracteres com símbolos, sem anotar em lugar nenhum", "correta": False,
                     "feedback": "Segurança máxima não adianta se a cliente não consegue usar — ela vai esquecer e ligar de novo em uma semana pedindo pra resetar."},
                ],
            },
            {
                "cena": "Dona Marlene já tem um roteador próprio (um TP-Link mais antigo) que ela quer continuar usando, ligado depois da ONT.",
                "pergunta": "Nesse caso, o que você configura na ONT Huawei EG8145?",
                "opcoes": [
                    {"texto": "Modo bridge na ONT, deixando o roteamento (DHCP, NAT, Wi-Fi) só por conta do roteador dela", "correta": True,
                     "feedback": "Isso. Se os dois equipamentos roteiam ao mesmo tempo (dupla NAT), pode dar problema em jogos online, chamadas de vídeo e alguns apps. Com a ONT em bridge, só o roteador dela cuida da rede."},
                    {"texto": "Deixa a ONT em modo router e conecta o roteador dela numa porta LAN, criando duas redes separadas", "correta": False,
                     "feedback": "Isso cria dupla NAT — dois equipamentos roteando ao mesmo tempo. Funciona parcialmente, mas costuma dar problema em jogos, chamadas de vídeo e liberação de portas."},
                    {"texto": "Desliga o Wi-Fi da ONT e do roteador dela, e diz pra ela usar só cabo", "correta": False,
                     "feedback": "Isso resolveria o conflito, mas tira a mobilidade que ela contratou. Colocar a ONT em bridge resolve sem sacrificar o Wi-Fi."},
                ],
            },
            {
                "cena": "A casa da Dona Marlene fica num condomínio bem adensado. Pelo celular você percebe umas 8 redes Wi-Fi de vizinhos por perto, muitas no canal 6 (2.4GHz).",
                "pergunta": "O que você faz em relação ao canal Wi-Fi?",
                "opcoes": [
                    {"texto": "Configura um canal menos usado (como 1 ou 11), ou deixa em automático se o equipamento escolher bem sozinho", "correta": True,
                     "feedback": "Isso. Em área com muita rede próxima, canais sobrepostos geram interferência e lentidão. Os canais 1, 6 e 11 não se sobrepõem entre si em 2.4GHz — escolher um menos concorrido ajuda bastante."},
                    {"texto": "Deixa exatamente no canal 6 também, porque é o canal padrão de fábrica e não deve ser mudado", "correta": False,
                     "feedback": "O canal de fábrica não é sagrado — em local com muita gente no mesmo canal, mudar é justamente a solução mais simples pra reduzir interferência."},
                    {"texto": "Aumenta a potência de transmissão da ONT ao máximo pra 'furar' a interferência dos vizinhos", "correta": False,
                     "feedback": "Aumentar potência não resolve interferência de canal — só deixa a rede dela interferindo ainda mais nas dos vizinhos, piorando o ciclo pra todo mundo."},
                ],
            },
            {
                "cena": "Serviço configurado, tudo funcionando. Dona Marlene pergunta: 'Mas por que antes minha internet caía toda hora e agora não?'",
                "pergunta": "Como você responde pra ela?",
                "opcoes": [
                    {"texto": "Explica de forma simples: os dois aparelhos estavam tentando organizar a internet ao mesmo tempo, então um atrapalhava o outro — agora só um faz esse trabalho", "correta": True,
                     "feedback": "Ótima resposta. Traduzir 'dupla NAT' pra linguagem do dia a dia é exatamente o papel do técnico N1 — o cliente não precisa saber o termo técnico, mas merece entender o que mudou."},
                    {"texto": "Explica com detalhes técnicos completos sobre NAT, DHCP e camadas de rede", "correta": False,
                     "feedback": "Tecnicamente correto, mas ela provavelmente vai se perder no meio da explicação. Um bom atendimento N1 traduz o problema pra linguagem acessível."},
                    {"texto": "Diz que não sabe explicar, só sabe que 'mexeu numas coisas'", "correta": False,
                     "feedback": "Isso passa insegurança e não constrói confiança. Mesmo uma explicação simples e curta já melhora muito a percepção do cliente sobre o atendimento."},
                ],
            },
        ],
    },
    {
        "id": "OS-53871",
        "bairro": "Setor Industrial",
        "titulo": "Suporte — Sem Internet no Cômodo dos Fundos",
        "cliente": "Sr. Roberto",
        "equipamento": "Cabeamento Ethernet, testador de cabo",
        "briefing": "Cliente reclama: na sala funciona, mas no quarto dos fundos não pega nada — nem cabo, nem Wi-Fi.",
        "instrumento": "cable",
        "decisoes": [
            {
                "cena": "O Sr. Roberto reclama: 'Na sala funciona, mas no quarto dos fundos não pega nada, nem cabo nem Wi-Fi.'",
                "pergunta": "Qual é o primeiro passo pra diagnosticar?",
                "opcoes": [
                    {"texto": "Verificar se existe cabo de rede chegando até o cômodo e, se sim, testar a continuidade dele com um testador de cabo", "correta": True,
                     "feedback": "Isso. Antes de qualquer configuração, você confirma se o problema é físico (cabo rompido, mal conectado) ou de sinal Wi-Fi. Como nem o cabo funciona nesse cômodo, o caminho físico é o primeiro suspeito."},
                    {"texto": "Reiniciar a ONT e torcer pra resolver sozinho", "correta": False,
                     "feedback": "Reiniciar é um teste rápido válido, mas sozinho não te dá informação nenhuma sobre por que aquele cômodo específico não pega nada. Isso é 'chute', não diagnóstico."},
                    {"texto": "Trocar a ONT do cliente por uma nova, já que pode estar com defeito", "correta": False,
                     "feedback": "Trocar peça sem diagnóstico é caro e raramente resolve — o problema está isolado num único cômodo, o que aponta pra algo local, não pro equipamento principal."},
                ],
            },
            {
                "cena": "Você descobre que falta um cabo de rede daquele ponto até o rack — a distância entre o rack e o cômodo é de uns 40 metros, passando pelo forro da casa.",
                "pergunta": "Qual cabo você usa pra esse trecho?",
                "opcoes": [
                    {"texto": "Cabo de par trançado Cat5e ou Cat6, já que 40 metros está bem dentro do limite de 100 metros do padrão Ethernet", "correta": True,
                     "feedback": "Correto. O padrão Ethernet permite até 100 metros de par trançado sem perda significativa de sinal. Com 40 metros você tem folga de sobra."},
                    {"texto": "Cabo coaxial, porque suporta distâncias mais longas que o par trançado", "correta": False,
                     "feedback": "Coaxial não é o padrão pra rede Ethernet doméstica — os equipamentos do cliente têm portas RJ45, feitas pra par trançado, não pra coaxial."},
                    {"texto": "Fibra óptica, já que qualquer distância acima de 10 metros exige fibra", "correta": False,
                     "feedback": "Não existe esse limite. Fibra é típica pra longas distâncias ou muita interferência elétrica. Pra 40 metros dentro de casa, par trançado resolve com folga e custa bem menos."},
                ],
            },
            {
                "cena": "Você vai crimpar os dois conectores RJ45 do cabo novo.",
                "pergunta": "Qual cuidado é mais importante na hora de crimpar?",
                "opcoes": [
                    {"texto": "Usar o mesmo padrão de cores (T568A ou T568B) nas duas pontas do cabo", "correta": True,
                     "feedback": "Isso mesmo. O que importa não é qual padrão você escolhe, e sim usar o mesmo nos dois conectores — misturar padrões transforma o cabo num cabo cruzado, que não funciona como esperado entre a maioria dos equipamentos domésticos."},
                    {"texto": "Deixar uns 5 cm de cabo sem destrançar antes do conector, pra ficar mais resistente", "correta": False,
                     "feedback": "Pelo contrário — quanto mais fio destrançado exposto, mais chance de interferência entre os pares. O ideal é destrançar só o mínimo necessário pra encaixar no conector."},
                    {"texto": "Usar cores diferentes em cada ponta pra facilitar identificar qual fio é qual depois", "correta": False,
                     "feedback": "Isso cria um cabo cruzado sem querer. Pra identificar as pontas depois, o certo é usar etiquetas, não misturar os padrões de crimpagem."},
                ],
            },
            {
                "cena": "Cabo testado, luz do testador toda verde, internet funcionando no quarto dos fundos. O Sr. Roberto pergunta se pode ligar mais aparelhos naquele mesmo ponto.",
                "pergunta": "Como você orienta ele?",
                "opcoes": [
                    {"texto": "Explica que aquele ponto sozinho atende 1 aparelho por cabo, mas ele pode usar um switch simples ali pra dividir entre vários aparelhos com fio", "correta": True,
                     "feedback": "Perfeito. Um ponto de rede = um cabo = uma conexão. Pra vários aparelhos cabeados no mesmo cômodo, um switch (não confundir com roteador) resolve sem passar mais cabo pela casa."},
                    {"texto": "Diz que não é possível ligar mais nenhum aparelho naquele ponto de jeito nenhum", "correta": False,
                     "feedback": "É possível sim, só precisa de um switch pra dividir o ponto entre vários aparelhos com fio — informação que evita uma ligação de reclamação depois."},
                    {"texto": "Sugere que ele compre outro plano de internet separado só pra aquele cômodo", "correta": False,
                     "feedback": "Isso não tem relação com o problema — o plano é da casa toda. O que resolve aqui é a distribuição física do cabeamento (um switch), não um novo plano."},
                ],
            },
        ],
    },
]
