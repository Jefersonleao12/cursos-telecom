"""
Conteúdo das Ordens de Serviço do "Simulador de Campo" (jogo de treinamento
na tela Início). Cada missão é uma O.S. com 4 decisões (cenário + pergunta +
3 alternativas, uma correta). A lógica do jogo em si fica em
webapp/services/jogo_campo.py — aqui só o conteúdo.

50 O.S. cobrindo fibra/óptica, Wi-Fi/roteador, cabeamento, atendimento ao
cliente, segurança do trabalho e ética profissional — o conteúdo pode
continuar crescendo conforme situações reais de campo forem repassadas.
Cada O.S. nova é só mais um item nesta lista; não precisa mudar nada no
motor do jogo (webapp/services/jogo_campo.py) para adicionar mais.
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
        "os_info": {
            "id_cliente": "55455",
            "horario": "09h30",
            "assunto": "Instalação Fibra Optica",
            "endereco": "TRAVESSA DAS PALMEIRAS, 431",
            "cidade": "Cacoal",
            "referencia": "Em frente ao posto de saúde",
            "caixa_atendimento": "CWL 01",
            "porta_ftth": "5",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Instalação Fibra Optica\n"
                "Descrição O.S. anterior: - Solicitante: atendente Bruna\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99187-8144\n"
                "Ocorrência: Cliente contratou o plano de 300 Mega e solicita instalação de fibra óptica. Primeira instalação no imóvel — atualmente utiliza apenas internet móvel."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Instalação, manutenção ou retirada de rede Fibra Optica",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {
                "cena": "Você chega com o cordão de fibra (pigtail) pronto para conectar na ONT Huawei EG8145. Na parte de trás do equipamento você vê uma entrada óptica com trava SC/APC (verde), quatro portas LAN (amarelas), entrada de energia e botão WPS.",
                "pergunta": "Em qual porta você conecta o conector de fibra?",
                "opcoes": [
                {
                    "texto": "Na porta óptica marcada como PON (conector verde SC/APC)",
                    "correta": True,
                    "feedback": "Isso mesmo. A porta PON é a única entrada óptica da ONT — é por ela que chega o sinal da operadora. As portas LAN (amarelas) são para cabo de rede, nunca para fibra.",
                },
                {
                    "texto": "Na porta óptica auxiliar marcada como CATV, deixando a PON livre pra uma eventual segunda operadora no futuro",
                    "correta": False,
                    "feedback": "A porta CATV é entrada de TV a cabo por RF, não de dados. O sinal da operadora chega pela PON — é ela que registra a ONT na OLT, e não existe 'reservar' a PON pra depois.",
                },
                {
                    "texto": "Na porta PON, usando o conector azul SC/UPC que veio no kit, já que o encaixe é do mesmo formato",
                    "correta": False,
                    "feedback": "Encaixa, e é aí que mora o problema: o polimento UPC é reto e o APC é angulado. A junta dos dois gera reflexão, o sinal volta e a instalação fica instável de um jeito difícil de diagnosticar depois.",
                },
            ],
            },
            {
                "cena": "Com a fibra conectada e a ONT ligada na tomada, você observa o painel de LEDs: PON (verde piscando), LOS (vermelho aceso), PWR (verde fixo).",
                "pergunta": "O LED LOS aceso em vermelho indica o quê?",
                "opcoes": [
                {
                    "texto": "Loss of Signal — perda de sinal óptico, algo está impedindo a luz de chegar corretamente",
                    "correta": True,
                    "feedback": "Exato. LOS significa 'Loss of Signal'. Pode ser conector sujo, dobra excessiva no cabo ou rompimento na rede externa. Antes de mexer na configuração, vale limpar o conector e checar a rota da fibra.",
                },
                {
                    "texto": "Que a ONT ainda está sincronizando com a OLT e esse LED apaga sozinho assim que o registro terminar",
                    "correta": False,
                    "feedback": "Durante o registro os LEDs piscam, e o LOS fica apagado. LOS ACESO e fixo é o oposto disso: significa que a luz não está chegando, então não há sincronismo nenhum pra concluir.",
                },
                {
                    "texto": "Que o sinal óptico está chegando forte demais e a ONT ligou a proteção do receptor pra não saturar",
                    "correta": False,
                    "feedback": "Sinal alto demais é problema real (ver a O.S. de sinal saturado), mas aparece como instabilidade e queda, não como LOS. O LOS é falta de luz, não excesso — são causas opostas.",
                },
            ],
            },
            {
                "cena": "Você limpa o conector com o kit de limpeza e reconecta. O LOS apaga. Agora você usa o medidor óptico para conferir a potência do sinal antes de liberar o atendimento.",
                "pergunta": "O medidor mostra -19 dBm. O que você faz?",
                "opcoes": [
                {
                    "texto": "Segue com a instalação — está dentro da faixa considerada ideal para GPON (cerca de -8 a -27 dBm)",
                    "correta": True,
                    "feedback": "Isso mesmo. -19 dBm está confortavelmente dentro da faixa ideal. Sinal perto demais de 0 dBm pode saturar o receptor, e abaixo de -27 dBm normalmente já não é suficiente. Ele está bem no meio — situação ótima.",
                },
                {
                    "texto": "Refaz a limpeza do conector e mede de novo, buscando chegar mais perto de -15 dBm, que é o meio da faixa, antes de liberar o atendimento pro cliente",
                    "correta": False,
                    "feedback": "-19 dBm já está confortavelmente dentro da faixa de trabalho. Perseguir um número 'mais bonito' consome tempo do seu dia sem ganho real de qualidade pro cliente.",
                },
                {
                    "texto": "Registra o valor no sistema e abre chamado pro NOC conferir a atenuação, deixando a instalação ativa",
                    "correta": False,
                    "feedback": "Abrir chamado pra um valor normal gera ruído pro NOC e pode fazer um alerta de verdade se perder no meio. Escalone quando o número sair da faixa, não quando ele estiver dentro dela.",
                },
            ],
            },
            {
                "cena": "O cliente pede para você passar o cabo de fibra em uma quina bem apertada atrás do rack de TV, dobrando quase 90 graus, para 'esconder o fio'.",
                "pergunta": "Como você lida com esse pedido?",
                "opcoes": [
                {
                    "texto": "Explica que a fibra precisa de uma curva suave (raio mínimo de curvatura) e sugere uma rota alternativa, ainda discreta",
                    "correta": True,
                    "feedback": "Correto. Fibra óptica não é como cabo elétrico — dobras muito fechadas causam microfraturas internas que degradam o sinal aos poucos, às vezes só semanas depois. Vale negociar uma rota com curva suave.",
                },
                {
                    "texto": "Faz a curva apertada como o cliente pediu e mede a potência depois pra confirmar que a perda ficou aceitável",
                    "correta": False,
                    "feedback": "A medição de hoje pode até passar, mas macrocurvatura é um problema que piora com o tempo e com a variação de temperatura. O cliente ficaria com uma falha marcada pra acontecer semanas depois.",
                },
                {
                    "texto": "Instala um protetor de curvatura naquela quina, mantém a dobra de 90 graus que o cliente pediu e anota no atendimento que o cabo passa por um ponto crítico",
                    "correta": False,
                    "feedback": "O acessório organiza o cabo, mas não muda o raio mínimo de curvatura da fibra — ele não autoriza uma dobra que a fibra não suporta. A rota é que precisa mudar.",
                },
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
        "os_info": {
            "id_cliente": "56083",
            "horario": "15h30",
            "assunto": "Realizar serviços - configurações",
            "endereco": "TRAVESSA DAS PALMEIRAS, 441",
            "cidade": "São Miguel",
            "referencia": "Esquina com a rua principal",
            "caixa_atendimento": "SMGE 01",
            "porta_ftth": "8",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Juliana\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99113-7876\n"
                "Ocorrência: Cliente relata que a internet cai com frequência. Possui roteador próprio conectado após a ONT. Solicita verificação técnica no local."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {
                "cena": "Dona Marlene pede: 'Bota uma senha fácil, tipo o meu nome mesmo, pra eu não esquecer.'",
                "pergunta": "Como você orienta ela sobre a senha do Wi-Fi?",
                "opcoes": [
                {
                    "texto": "Sugere uma senha com pelo menos 8 caracteres, misturando letras e números, e anota num papel pra ela guardar perto do roteador",
                    "correta": True,
                    "feedback": "Boa! Só o nome dela é fácil demais de adivinhar por vizinhos. O ideal é equilibrar segurança com praticidade — simples de lembrar, mas não óbvia.",
                },
                {
                    "texto": "Usa o nome dela seguido do ano de nascimento, que fica fácil de lembrar e já mistura letra com número",
                    "correta": False,
                    "feedback": "Mistura letra e número, mas é dado público: qualquer pessoa que conheça a Dona Marlene acerta em duas tentativas. Senha fácil de lembrar não pode ser fácil de adivinhar.",
                },
                {
                    "texto": "Deixa a senha de fábrica da etiqueta, que já é forte e fica sempre disponível impressa no aparelho",
                    "correta": False,
                    "feedback": "A senha da etiqueta costuma seguir um padrão derivado do número de série, e fica visível pra qualquer visitante que chegue perto do roteador. Serve pra ligar o serviço, não pra ficar pra sempre.",
                },
            ],
            },
            {
                "cena": "Dona Marlene já tem um roteador próprio (um TP-Link mais antigo) que ela quer continuar usando, ligado depois da ONT.",
                "pergunta": "Nesse caso, o que você configura na ONT Huawei EG8145?",
                "opcoes": [
                {
                    "texto": "Modo bridge na ONT, deixando o roteamento (DHCP, NAT, Wi-Fi) só por conta do roteador dela",
                    "correta": True,
                    "feedback": "Isso. Se os dois equipamentos roteiam ao mesmo tempo (dupla NAT), pode dar problema em jogos online, chamadas de vídeo e alguns apps. Com a ONT em bridge, só o roteador dela cuida da rede.",
                },
                {
                    "texto": "Mantém a ONT em modo router e configura o roteador dela também em modo router, com faixas de IP diferentes",
                    "correta": False,
                    "feedback": "Não conflita, mas cria duas camadas de NAT: a internet 'funciona' e ao mesmo tempo quebra chamada de vídeo, jogo online e acesso remoto. É o cenário que costuma gerar chamado umas semanas depois.",
                },
                {
                    "texto": "Coloca a ONT em bridge e o roteador dela também em bridge, deixando a operadora entregar IP direto nos aparelhos",
                    "correta": False,
                    "feedback": "Com os dois em bridge ninguém faz o roteamento: não há quem autentique a conexão nem distribua os IPs da casa. A rede simplesmente não sobe — alguém precisa assumir esse papel.",
                },
            ],
            },
            {
                "cena": "A casa da Dona Marlene fica num condomínio bem adensado. Pelo celular você percebe umas 8 redes Wi-Fi de vizinhos por perto, muitas no canal 6 (2.4GHz).",
                "pergunta": "O que você faz em relação ao canal Wi-Fi?",
                "opcoes": [
                {
                    "texto": "Configura um canal menos usado (como 1 ou 11), ou deixa em automático se o equipamento escolher bem sozinho",
                    "correta": True,
                    "feedback": "Isso. Em área com muita rede próxima, canais sobrepostos geram interferência e lentidão. Os canais 1, 6 e 11 não se sobrepõem entre si em 2.4GHz — escolher um menos concorrido ajuda bastante.",
                },
                {
                    "texto": "Fixa no canal 3 ou 9, que ficam entre os canais mais usados e por isso sofrem menos disputa direta",
                    "correta": False,
                    "feedback": "Parece esperto, mas é o pior dos mundos: em 2,4 GHz só 1, 6 e 11 não se sobrepõem. Um canal intermediário pega pedaço dos dois vizinhos e some ruído em vez de dividir espaço organizado.",
                },
                {
                    "texto": "Passa a rede toda pra 5 GHz, que sofre bem menos interferência, e desliga o 2,4 GHz pra não confundir",
                    "correta": False,
                    "feedback": "O 5 GHz é mais limpo mesmo, mas atravessa menos parede e nem todo aparelho da casa enxerga essa faixa. Desligar o 2,4 GHz resolve a interferência e cria um problema de cobertura no lugar.",
                },
            ],
            },
            {
                "cena": "Serviço configurado, tudo funcionando. Dona Marlene pergunta: 'Mas por que antes minha internet caía toda hora e agora não?'",
                "pergunta": "Como você responde pra ela?",
                "opcoes": [
                {
                    "texto": "Explica de forma simples: os dois aparelhos estavam tentando organizar a internet ao mesmo tempo, então um atrapalhava o outro — agora só um faz esse trabalho",
                    "correta": True,
                    "feedback": "Ótima resposta. Traduzir 'dupla NAT' pra linguagem do dia a dia é exatamente o papel do técnico N1 — o cliente não precisa saber o termo técnico, mas merece entender o que mudou.",
                },
                {
                    "texto": "Explica que o roteador antigo dela estava com defeito e agora funciona porque a ONT assumiu o serviço",
                    "correta": False,
                    "feedback": "O roteador dela não tinha defeito nenhum — ele estava fazendo o trabalho dele, só que em duplicidade com a ONT. Dizer que estava quebrado leva a cliente a comprar um aparelho novo à toa.",
                },
                {
                    "texto": "Diz que provavelmente era instabilidade da rede na região e que agora o sinal está mais estável por lá",
                    "correta": False,
                    "feedback": "É uma resposta confortável, e por isso mesmo perigosa: joga a causa pra fora quando o problema estava na configuração da casa. Se ela mexer no roteador de novo, a queda volta e ninguém entende por quê.",
                },
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
        "os_info": {
            "id_cliente": "52227",
            "horario": "14h30",
            "assunto": "Realizar serviços - configurações",
            "endereco": "AVENIDA MARECHAL RONDON, 700",
            "cidade": "Conselvan",
            "referencia": "Portão de madeira, casa de esquina",
            "caixa_atendimento": "AYPO 01",
            "porta_ftth": "3",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Aline\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99813-3490\n"
                "Ocorrência: Cliente informa que a internet funciona normalmente na sala, mas não há sinal (cabo ou Wi-Fi) no quarto dos fundos. Solicita verificação no local."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {
                "cena": "O Sr. Roberto reclama: 'Na sala funciona, mas no quarto dos fundos não pega nada, nem cabo nem Wi-Fi.'",
                "pergunta": "Qual é o primeiro passo pra diagnosticar?",
                "opcoes": [
                {
                    "texto": "Verificar se existe cabo de rede chegando até o cômodo e, se sim, testar a continuidade dele com um testador de cabo",
                    "correta": True,
                    "feedback": "Isso. Antes de qualquer configuração, você confirma se o problema é físico (cabo rompido, mal conectado) ou de sinal Wi-Fi. Como nem o cabo funciona nesse cômodo, o caminho físico é o primeiro suspeito.",
                },
                {
                    "texto": "Instalar um repetidor Wi-Fi no corredor, já que o cômodo é o mais distante da sala e o sinal chega fraco",
                    "correta": False,
                    "feedback": "Pode até melhorar o Wi-Fi, mas o Sr. Roberto disse que o cabo também não funciona — e repetidor nenhum resolve cabo. Partir pra solução antes de diagnosticar costuma custar uma segunda visita.",
                },
                {
                    "texto": "Trocar o cabo de rede daquele ponto por um novo já crimpado, pra descartar problema de cabeamento de uma vez",
                    "correta": False,
                    "feedback": "Boa intenção, mas você ainda não sabe se existe cabo naquele trecho. Trocar pressupõe que há o que trocar — e é justamente essa a pergunta que o teste de continuidade responde primeiro.",
                },
            ],
            },
            {
                "cena": "Você descobre que falta um cabo de rede daquele ponto até o rack — a distância entre o rack e o cômodo é de uns 40 metros, passando pelo forro da casa.",
                "pergunta": "Qual cabo você usa pra esse trecho?",
                "opcoes": [
                {
                    "texto": "Cabo de par trançado Cat5e ou Cat6, já que 40 metros está bem dentro do limite de 100 metros do padrão Ethernet",
                    "correta": True,
                    "feedback": "Correto. O padrão Ethernet permite até 100 metros de par trançado sem perda significativa de sinal. Com 40 metros você tem folga de sobra.",
                },
                {
                    "texto": "Cabo Cat6A blindado, que passa a ser obrigatório acima de 30 metros pra compensar a perda no percurso",
                    "correta": False,
                    "feedback": "Essa regra não existe. O limite do Ethernet é de 100 metros pra qualquer categoria a partir da Cat5e; blindagem serve pra ambiente com muito ruído elétrico, não pra distância.",
                },
                {
                    "texto": "Dois trechos de Cat5e de 20 metros emendados com um acoplador RJ45 no meio do percurso",
                    "correta": False,
                    "feedback": "Funciona no teste e depois dá dor de cabeça: cada acoplador é um ponto de perda e de mau contato, ainda por cima no meio do forro, onde ninguém vai procurar defeito daqui a seis meses.",
                },
            ],
            },
            {
                "cena": "Você vai crimpar os dois conectores RJ45 do cabo novo.",
                "pergunta": "Qual cuidado é mais importante na hora de crimpar?",
                "opcoes": [
                {
                    "texto": "Usar o mesmo padrão de cores (T568A ou T568B) nas duas pontas do cabo",
                    "correta": True,
                    "feedback": "Isso mesmo. O que importa não é qual padrão você escolhe, e sim usar o mesmo nos dois conectores — misturar padrões transforma o cabo num cabo cruzado, que não funciona como esperado entre a maioria dos equipamentos domésticos.",
                },
                {
                    "texto": "Destrançar os pares o mínimo possível antes do conector, no máximo uns 13 mm, pra manter o desempenho",
                    "correta": False,
                    "feedback": "Isso é boa prática de verdade e vale seguir. Só que é um cuidado de desempenho: com os pares muito destrançados o cabo ainda funciona. Com padrões diferentes nas duas pontas, ele simplesmente não passa dado.",
                },
                {
                    "texto": "Testar a continuidade do cabo antes de crimpar a segunda ponta, pra não perder conector se estiver rompido",
                    "correta": False,
                    "feedback": "O testador precisa das duas pontas terminadas pra fechar o circuito — antes disso não há o que medir. O conector custa centavos; o teste vem depois, com o cabo pronto.",
                },
            ],
            },
            {
                "cena": "Cabo testado, luz do testador toda verde, internet funcionando no quarto dos fundos. O Sr. Roberto pergunta se pode ligar mais aparelhos naquele mesmo ponto.",
                "pergunta": "Como você orienta ele?",
                "opcoes": [
                {
                    "texto": "Explica que aquele ponto sozinho atende 1 aparelho por cabo, mas ele pode usar um switch simples ali pra dividir entre vários aparelhos com fio",
                    "correta": True,
                    "feedback": "Perfeito. Um ponto de rede = um cabo = uma conexão. Pra vários aparelhos cabeados no mesmo cômodo, um switch (não confundir com roteador) resolve sem passar mais cabo pela casa.",
                },
                {
                    "texto": "Explica que ele pode usar um hub simples ali, que divide o sinal entre os aparelhos sem configurar nada",
                    "correta": False,
                    "feedback": "Hub e switch parecem a mesma coisa mas não são: o hub repete tudo pra todo mundo, então os aparelhos disputam a mesma faixa e a velocidade cai conforme ele liga mais coisa. O switch entrega a porta cheia pra cada um.",
                },
                {
                    "texto": "Sugere instalar um segundo roteador naquele ponto, criando uma rede própria pro cômodo dos fundos",
                    "correta": False,
                    "feedback": "Resolve, mas cria uma segunda rede dentro da casa: os aparelhos do fundo deixam de enxergar a impressora e a TV da sala. Pra só dividir o ponto, o switch faz o serviço sem separar nada.",
                },
            ],
            },
        ],
    },
    {
        "id": "OS-54102",
        "bairro": "Nova Porto Velho",
        "titulo": "Suporte — ONT com Sinal Óptico Zerado",
        "cliente": "Sra. Cleusa",
        "equipamento": "ONT Huawei EG8145, medidor óptico",
        "briefing": "Cliente sem internet desde ontem. Você já confirmou que a fibra chega até a ONT dela, mas o LED PON nem acende.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "56506",
            "horario": "10h00",
            "assunto": "Sem Internet",
            "endereco": "TRAVESSA DAS PALMEIRAS, 672",
            "cidade": "Aripuanã",
            "referencia": "Perto da praça central",
            "caixa_atendimento": "AYP 01",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Sem Internet\n"
                "Descrição O.S. anterior: - Solicitante: atendente Mayara\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99679-7477\n"
                "Ocorrência: Cliente sem internet desde o dia anterior. Solicita atendimento técnico com urgência para verificação do sinal."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "A ONT está ligada na tomada (LED PWR aceso), mas o LED PON está completamente apagado — nem vermelho, nem verde.",
             "pergunta": "O que isso costuma indicar?",
             "opcoes": [
                {
                    "texto": "Não está chegando NENHUM sinal óptico na ONT — o problema é anterior a ela, provavelmente no splitter da CTO ou na rede externa",
                    "correta": True,
                    "feedback": "Isso. PON apagado (não vermelho) geralmente significa ausência total de luz, não só sinal fraco — o caminho mais provável é conferir a CTO/splitter na rua antes de mexer mais na casa.",
                },
                {
                    "texto": "A ONT perdeu o provisionamento e precisa ser recadastrada no sistema com o número de série antes de qualquer teste físico na fibra ou na CTO",
                    "correta": False,
                    "feedback": "Provisionamento é problema de software, e aparece como PON piscando ou LOS aceso, não como LED apagado. Apagado é ausência de luz — sinal físico que nem chegou.",
                },
                {
                    "texto": "O cordão está conectado com a polaridade invertida (TX e RX trocados) na entrada da própria ONT",
                    "correta": False,
                    "feedback": "Em GPON a fibra é única: o mesmo filamento leva e traz o sinal, em comprimentos de onda diferentes. Não existe par TX/RX pra inverter — isso é de enlaces ópticos ponto a ponto, não do padrão que usamos.",
                },
            ]},
            {"cena": "Você vai até a CTO (caixa de emenda na rua) mais próxima e abre com a chave adequada.",
             "pergunta": "O que você confere primeiro dentro da CTO?",
             "opcoes": [
                {
                    "texto": "Se a porta do splitter que atende essa casa está com o cordão bem conectado e sem sinais de rompimento",
                    "correta": True,
                    "feedback": "Exato — CTO é um ponto clássico de problema: conector solto, mal encaixado por outro serviço, ou cordão rompido por bicho/obra.",
                },
                {
                    "texto": "Mede a potência na entrada e na saída geral do splitter pra descobrir se a CTO inteira está recebendo bem, antes de identificar qual porta atende essa casa",
                    "correta": False,
                    "feedback": "A medição na saída geral não diz nada sobre a porta desse cliente: o splitter pode estar entregando bem em quinze portas e mal justamente na dele. Identifique a porta primeiro.",
                },
                {
                    "texto": "Reaperta todos os conectores da CTO, pra garantir contato firme em todas as portas de uma vez",
                    "correta": False,
                    "feedback": "Mexer em portas de clientes que estão funcionando é a receita pra sair da CTO com mais chamados do que entrou. Trabalhe só na porta do atendimento.",
                },
            ]},
            {"cena": "Você encontra o cordão da porta da Sra. Cleusa desconectado — provavelmente outro técnico mexeu ali por engano num serviço vizinho.",
             "pergunta": "O que você faz?",
             "opcoes": [
                {
                    "texto": "Reconecta na porta certa, limpa o conector antes de encaixar, e confere o sinal com o medidor óptico depois",
                    "correta": True,
                    "feedback": "Correto — sempre limpar antes de reconectar, e confirmar com o medidor que o sinal voltou dentro da faixa ideal, não só 'parece que conectou'.",
                },
                {
                    "texto": "Reconecta na porta certa e confere o sinal no medidor, sem limpar o conector já que ele estava dentro da caixa",
                    "correta": False,
                    "feedback": "A caixa protege da chuva, não de poeira e do óleo do dedo de quem manuseou. Como a sujeira só aparece como perda depois, você entrega um atendimento que degrada sozinho nas próximas semanas.",
                },
                {
                    "texto": "Reconecta o cordão e registra a ocorrência pra central antes de medir, pra avisar o outro técnico o quanto antes",
                    "correta": False,
                    "feedback": "Registrar é importante e vai acontecer no fim. Mas sair da CTO sem medir é apostar que reconectar bastou — se o conector estiver danificado, você descobre pelo chamado do cliente, não pelo medidor.",
                },
            ]},
            {"cena": "Sinal restabelecido, ONT com todos os LEDs certos. Você liga pra Sra. Cleusa confirmando que já pode testar a internet.",
             "pergunta": "Antes de encerrar a O.S., o que mais vale registrar no relatório do serviço?",
             "opcoes": [
                {
                    "texto": "Que a causa foi um cordão desconectado na CTO por outro serviço — ajuda a central a identificar se foi um erro recorrente de algum técnico ou equipe",
                    "correta": True,
                    "feedback": "Isso é importante: registrar a causa raiz (não só 'resolvido') ajuda a Norte Tel a evitar que o mesmo erro se repita com outros clientes na mesma CTO.",
                },
                {
                    "texto": "Que o sinal foi restabelecido na CTO e o valor medido no cliente, sem citar como o cordão ficou desconectado",
                    "correta": False,
                    "feedback": "O registro fica tecnicamente correto e inútil pra central: sem a causa, ninguém percebe que houve desconexão indevida. É justamente esse padrão que revela um problema recorrente de procedimento.",
                },
                {
                    "texto": "Que houve desconexão indevida e o nome do técnico que atendeu aquela CTO na data, pra apuração",
                    "correta": False,
                    "feedback": "Você não tem como saber quem foi só pelo que encontrou na caixa. Registre o fato (cordão desconectado, provavelmente em outro serviço) e deixe a central cruzar os dados — apontar nome sem prova cria conflito à toa.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54187",
        "bairro": "São Cristóvão",
        "titulo": "Instalação — Sinal Óptico Saturado",
        "cliente": "Sr. Edmilson",
        "equipamento": "ONT Huawei EG8145, medidor óptico",
        "briefing": "Instalação nova, casa bem próxima da CTO. Após ligar tudo, o LED PON pisca estranho e a internet cai a cada poucos minutos.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "58613",
            "horario": "10h30",
            "assunto": "Instalação Fibra Optica",
            "endereco": "RUA DAS FLORES, 368",
            "cidade": "Juína",
            "referencia": "Perto do campo de futebol",
            "caixa_atendimento": "JNA 01",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Instalação Fibra Optica\n"
                "Descrição O.S. anterior: - Solicitante: atendente Bruna\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99442-9157\n"
                "Ocorrência: Cliente contratou instalação nova de fibra óptica. Imóvel localizado próximo à CTO."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Instalação, manutenção ou retirada de rede Fibra Optica",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você mede a potência óptica na ONT: o medidor mostra -3 dBm.",
             "pergunta": "O que esse valor indica?",
             "opcoes": [
                {
                    "texto": "Sinal forte demais (perto de 0 dBm) — pode estar saturando o receptor da ONT, causando instabilidade",
                    "correta": True,
                    "feedback": "Isso mesmo. Assim como sinal fraco demais é problema, sinal forte demais também satura o receptor óptico — casas muito próximas da CTO às vezes precisam de um atenuador.",
                },
                {
                    "texto": "Sinal no limite superior da faixa — dá pra liberar e acompanhar se o cliente reclamar de instabilidade",
                    "correta": False,
                    "feedback": "-3 dBm não é limite, é fora da faixa de trabalho. Liberar assim transfere pro cliente a tarefa de descobrir o problema, e a instabilidade por saturação é das mais difíceis de ele relacionar com a instalação.",
                },
                {
                    "texto": "Provável erro de leitura por conector sujo — vale limpar bem e medir de novo antes de concluir qualquer coisa",
                    "correta": False,
                    "feedback": "Limpar nunca é perda de tempo, mas repare na direção: sujeira ATRAPALHA a luz, então derrubaria a leitura. Um valor alto demais não vem de sujeira — vem de sinal chegando forte mesmo.",
                },
            ]},
            {"cena": "Você confirma que a distância até a CTO é muito curta, o que explica o sinal alto.",
             "pergunta": "Qual é a solução mais adequada?",
             "opcoes": [
                {
                    "texto": "Instalar um atenuador óptico no cordão pra reduzir a potência até a faixa ideal",
                    "correta": True,
                    "feedback": "Correto — o atenuador existe exatamente pra esses casos, reduzindo a potência sem precisar 'esticar' cabo desnecessariamente.",
                },
                {
                    "texto": "Trocar o cordão por um bem mais longo, enrolado com folga no rack, pra gastar sinal na distância extra",
                    "correta": False,
                    "feedback": "A fibra perde cerca de 0,3 dB por quilômetro. Pra derrubar os dBm que sobram você precisaria de quilômetros de cordão — alguns metros a mais não mudam praticamente nada na medição.",
                },
                {
                    "texto": "Pedir pro NOC reduzir a potência da porta da OLT que atende essa CTO até o valor ficar na faixa",
                    "correta": False,
                    "feedback": "Essa porta alimenta o splitter inteiro. Baixar a potência pra ajustar um cliente que está perto demais derruba justamente os que estão mais longe. O ajuste tem que ser no ponto, não na origem.",
                },
            ]},
            {"cena": "Com o atenuador instalado, o medidor agora mostra -16 dBm.",
             "pergunta": "Isso está adequado pra liberar a instalação?",
             "opcoes": [
                {
                    "texto": "Sim — está bem dentro da faixa ideal pra GPON, pode liberar o atendimento",
                    "correta": True,
                    "feedback": "Isso mesmo, -16 dBm é uma leitura ótima, confortavelmente dentro da faixa recomendada.",
                },
                {
                    "texto": "Sim, mas vale trocar por um atenuador de valor menor pra deixar uma margem mais folgada pro futuro",
                    "correta": False,
                    "feedback": "-16 dBm está no meio da faixa, que já é a margem folgada. Trocar por trocar significa medir tudo de novo e correr o risco de sair da faixa pro outro lado.",
                },
                {
                    "texto": "Não — com atenuador instalado a referência muda, e o ideal passa a ser entre -8 e -12 dBm",
                    "correta": False,
                    "feedback": "A faixa aceitável é da ONT e não muda por causa do atenuador: ela mede a luz que chega, não como a luz foi ajustada. -16 dBm é -16 dBm, com ou sem atenuador no caminho.",
                },
            ]},
            {"cena": "Serviço concluído. O Sr. Edmilson pergunta se vai precisar trocar esse 'aparelhinho' (o atenuador) algum dia.",
             "pergunta": "Como você responde?",
             "opcoes": [
                {
                    "texto": "Explica que o atenuador é passivo, não tem eletrônica nem desgasta com o uso — só precisaria mexer se a distância até a CTO mudasse",
                    "correta": True,
                    "feedback": "Resposta correta e tranquiliza o cliente: é um componente simples e duradouro, sem necessidade de manutenção regular.",
                },
                {
                    "texto": "Explica que o atenuador tem validade e é trocado na manutenção preventiva anual, junto com o cordão óptico",
                    "correta": False,
                    "feedback": "Essa manutenção anual não existe, e criar essa expectativa gera chamado desnecessário depois. O atenuador é uma peça passiva: enquanto a instalação não mudar, ele fica onde está.",
                },
                {
                    "texto": "Explica que ele mesmo pode tirar o atenuador se um dia achar a internet lenta, porque o sinal fica mais forte",
                    "correta": False,
                    "feedback": "Mais sinal parece melhor, mas aqui é o contrário: sem o atenuador a ONT volta a saturar e a internet fica instável de novo — e ninguém vai ligar a lentidão com a peça que ele tirou meses antes.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54233",
        "bairro": "Centro (Vilhena)",
        "titulo": "Instalação — Prédio Comercial de 3 Andares",
        "cliente": "Escritório Contábil Vale Verde",
        "equipamento": "ONT Huawei EG8145, canaleta, protetor de fibra",
        "briefing": "A fibra entra no térreo, mas a sala do cliente fica no 2º andar. É preciso levar o sinal com segurança pela rota vertical do prédio.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "52489",
            "horario": "17h00",
            "assunto": "Instalação de Novo Ponto",
            "endereco": "RUA DOM PEDRO II, 702",
            "cidade": "Colniza",
            "referencia": "Esquina com a rua principal",
            "caixa_atendimento": "CNIZ 01",
            "porta_ftth": "8",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Instalação de Novo Ponto\n"
                "Descrição O.S. anterior: - Solicitante: atendente Rafael\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99120-9760\n"
                "Ocorrência: Cliente contratou instalação de ponto de internet em prédio comercial de 3 andares. Escritório localizado no 2º andar."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Instalação, manutenção ou retirada de rede Fibra Optica",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você precisa passar a fibra por um shaft (duto vertical) compartilhado com outras instalações do prédio.",
             "pergunta": "Qual cuidado é essencial nessa rota?",
             "opcoes": [
                {
                    "texto": "Usar protetor/canaleta pra fibra e evitar que ela fique solta encostando em cabos elétricos ou bordas cortantes",
                    "correta": True,
                    "feedback": "Isso — fibra desprotegida num shaft compartilhado corre risco de ser pisada, cortada ou dobrada por outros serviços que passarem ali depois.",
                },
                {
                    "texto": "Prender a fibra junto aos cabos de força com abraçadeira, que é o jeito de deixar tudo firme e organizado no shaft",
                    "correta": False,
                    "feedback": "Fibra não sofre interferência elétrica, então o risco não é esse: é mecânico. Abraçadeira apertada amassa o cabo, e cabo de força esquenta e tem peso — a fibra fica sob esforço contínuo até romper.",
                },
                {
                    "texto": "Deixar a fibra com bastante folga solta pelo shaft, já que sobra é melhor que falta em manutenção futura",
                    "correta": False,
                    "feedback": "Folga demais vira laçada que encosta em borda cortante e prende em qualquer serviço de outro prestador. Reserva técnica se faz enrolada em raio adequado e fixada, não sobrando solta pelo duto.",
                },
            ]},
            {"cena": "No 2º andar, a sala do cliente fica a uns 60 metros da entrada de fibra do prédio, exigindo uma emenda no meio do caminho.",
             "pergunta": "Qual método de emenda oferece melhor qualidade de sinal pra esse trecho?",
             "opcoes": [
                {
                    "texto": "Emenda por fusão (solda térmica), que tem perda de sinal muito menor que um conector mecânico",
                    "correta": True,
                    "feedback": "Correto. Fusão é o padrão pra emendas permanentes de qualidade — perda mínima de sinal, importante em rotas mais longas dentro do prédio.",
                },
                {
                    "texto": "Emenda mecânica, que dispensa a máquina de fusão e por isso é o método indicado quando há prazo apertado",
                    "correta": False,
                    "feedback": "Ela existe justamente pra emergência, e é aceitável nesse papel. Pra uma instalação definitiva, porém, ela insere bem mais perda que a fusão e envelhece pior — o cliente paga isso em margem de sinal.",
                },
                {
                    "texto": "Conector de campo montado nas duas pontas, ligados por um adaptador, que permite desconectar depois se precisar",
                    "correta": False,
                    "feedback": "É prático pra manutenção, mas você troca uma emenda por duas interfaces ópticas no meio do trecho. Cada uma soma perda e vira ponto de sujeira — num percurso que já tem distância, a conta não fecha.",
                },
            ]},
            {"cena": "Instalação concluída. O medidor óptico mostra -21 dBm na ONT do cliente, já considerando a distância e a emenda.",
             "pergunta": "Isso é aceitável?",
             "opcoes": [
                {
                    "texto": "Sim, ainda está dentro da faixa ideal pra GPON, mesmo com a distância extra e a emenda",
                    "correta": True,
                    "feedback": "Correto — mesmo com perdas adicionais de distância e emenda, -21 dBm segue dentro da faixa recomendada.",
                },
                {
                    "texto": "Não — com emenda no percurso o limite aceitável fica mais apertado, e -21 dBm já não dá margem de segurança",
                    "correta": False,
                    "feedback": "A faixa da ONT não muda por causa da emenda: ela mede a luz que chega, não o caminho que a luz fez. -21 dBm está dentro da faixa, com emenda ou sem.",
                },
                {
                    "texto": "Sim, mas vale refazer a fusão pra tentar ganhar 1 ou 2 dBm e deixar o cliente com mais folga no futuro",
                    "correta": False,
                    "feedback": "Refazer uma fusão que já está boa é abrir de novo um ponto que estava resolvido, com chance real de sair pior. Dentro da faixa, o ganho marginal não paga o risco.",
                },
            ]},
            {"cena": "O escritório pede um documento simples confirmando a instalação, pra anexar no controle interno deles.",
             "pergunta": "O que você inclui nesse registro?",
             "opcoes": [
                {
                    "texto": "Data, equipamento instalado, leitura do sinal óptico e um resumo da rota (com emenda no shaft do prédio)",
                    "correta": True,
                    "feedback": "Isso é um bom registro técnico — dá rastreabilidade caso precise de manutenção futura, especialmente sabendo que existe uma emenda no meio do caminho.",
                },
                {
                    "texto": "Data, equipamento instalado e a leitura do sinal, sem detalhar a rota — o percurso é informação interna da operação",
                    "correta": False,
                    "feedback": "A rota é justamente o que o controle interno deles precisa: quando alguém for mexer no shaft, é esse registro que evita cortarem a fibra sem saber que ela passa ali.",
                },
                {
                    "texto": "Data, rota completa e a leitura, além do número de série da ONT e a senha do Wi-Fi configurada no local",
                    "correta": False,
                    "feedback": "Registro técnico não leva senha. Esse documento circula no controle interno do escritório e pode ser lido por qualquer pessoa — a senha vai pro cliente, não pro papel.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54301",
        "bairro": "Costa e Silva",
        "titulo": "Suporte — Corte de Fibra por Obra na Rua",
        "cliente": "Família Andrade",
        "equipamento": "Fibra drop, kit de fusão",
        "briefing": "Uma empresa de saneamento fez uma escavação na rua e cortou o cabo de fibra que atende vários clientes, incluindo essa casa.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "53776",
            "horario": "17h00",
            "assunto": "Sem Internet",
            "endereco": "TRAVESSA DAS PALMEIRAS, 193",
            "cidade": "Pimenta Bueno",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "PBW 01",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Sem Internet\n"
                "Descrição O.S. anterior: - Solicitante: atendente Lucas\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99441-1193\n"
                "Ocorrência: Cliente sem internet. Região reporta interrupção coletiva, possivelmente relacionada a obra na via pública."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Infraestrutura de Fibra",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você chega no local e confirma visualmente que o cabo de fibra está rompido, com a escavação ainda aberta.",
             "pergunta": "Qual é o primeiro passo correto?",
             "opcoes": [
                {
                    "texto": "Isolar a área, avaliar se dá pra fazer o reparo com segurança, e comunicar a central sobre um corte que afeta múltiplos clientes",
                    "correta": True,
                    "feedback": "Correto — corte de rede externa costuma afetar mais gente além dessa casa, então avisar a central ajuda a coordenar o reparo e informar outros clientes afetados.",
                },
                {
                    "texto": "Fazer a emenda logo, aproveitando que a vala está aberta, e comunicar a central assim que o serviço estiver concluído",
                    "correta": False,
                    "feedback": "Aproveitar a vala aberta faz sentido. O que não pode esperar é o aviso: se o corte afeta vários clientes, a central precisa saber agora pra responder aos chamados que já estão entrando.",
                },
                {
                    "texto": "Fotografar o rompimento, registrar a ocorrência contra a empresa da obra e aguardar autorização pra reparar",
                    "correta": False,
                    "feedback": "A documentação é importante e você vai fazer. Mas parar o reparo esperando autorização deixa a rua sem internet por causa de um trâmite — registre e conserte, nessa ordem, sem inverter.",
                },
            ]},
            {"cena": "Você faz a emenda por fusão no trecho rompido, restabelecendo a continuidade do cabo.",
             "pergunta": "Depois da fusão, qual o próximo passo antes de considerar o reparo concluído?",
             "opcoes": [
                {
                    "texto": "Medir o sinal óptico em pelo menos um ponto pra confirmar que a fusão ficou de boa qualidade",
                    "correta": True,
                    "feedback": "Isso — uma fusão malfeita pode parecer OK visualmente mas ter perda alta de sinal; medir confirma que o reparo realmente funcionou.",
                },
                {
                    "texto": "Conferir visualmente a fusão na tela da máquina, que já mostra a estimativa de perda da emenda feita",
                    "correta": False,
                    "feedback": "A estimativa da máquina é um bom indício, mas é cálculo de imagem, não medição do enlace. Só o medidor mostra o que realmente chega na ponta depois de todo o percurso.",
                },
                {
                    "texto": "Ligar pra central confirmar se os clientes daquele trecho voltaram a ficar online no sistema de monitoramento",
                    "correta": False,
                    "feedback": "Se voltaram online, ótimo — mas online não quer dizer com boa margem. Uma fusão ruim entrega sinal suficiente pra registrar e fraco demais pra aguentar chuva na semana seguinte.",
                },
            ]},
            {"cena": "Sinal confirmado bom em todos os pontos testados. A escavação da empresa de saneamento ainda está aberta na rua.",
             "pergunta": "O que fazer com a fibra reparada antes de sair do local?",
             "opcoes": [
                {
                    "texto": "Proteger fisicamente a emenda (com um protetor adequado) antes de a vala ser fechada, pra evitar novo dano",
                    "correta": True,
                    "feedback": "Correto — sem proteção, a emenda fica vulnerável quando a vala for fechada ou se houver mais movimentação na obra.",
                },
                {
                    "texto": "Sinalizar o ponto com fita de identificação e informar a empresa de saneamento sobre a posição exata do cabo",
                    "correta": False,
                    "feedback": "Sinalizar ajuda, e vale fazer. Mas fita não protege de retroescavadeira nem de pedra sendo jogada na vala — a emenda precisa de proteção física antes de o buraco ser fechado.",
                },
                {
                    "texto": "Deixar uma reserva de cabo enrolada na vala, pra que uma futura emenda no mesmo ponto não exija nova escavação",
                    "correta": False,
                    "feedback": "Reserva técnica é boa prática e cabe aqui. Só que ela também precisa ser acomodada e protegida: cabo sobrando solto na vala é o próximo rompimento esperando a próxima obra.",
                },
            ]},
            {"cena": "De volta à central, você precisa registrar o ocorrido.",
             "pergunta": "O que é importante constar no registro desse atendimento?",
             "opcoes": [
                {
                    "texto": "Que o corte foi causado por obra de terceiros (empresa de saneamento), com local e horário — útil caso a Norte Tel precise cobrar o reparo da responsável",
                    "correta": True,
                    "feedback": "Exato — registrar a causa externa (terceiro) é importante tanto pro histórico técnico quanto pra questões administrativas/financeiras da empresa.",
                },
                {
                    "texto": "Que houve rompimento de cabo com reparo por fusão, o horário do restabelecimento e o sinal medido nos pontos",
                    "correta": False,
                    "feedback": "Está completo do lado técnico e vazio do lado que importa aqui: sem registrar que a causa foi obra de terceiros, a Norte Tel perde o respaldo pra cobrar o prejuízo de quem cortou.",
                },
                {
                    "texto": "Que o corte foi causado por obra de terceiros, sem identificar a empresa, pra não gerar atrito com o município",
                    "correta": False,
                    "feedback": "Justamente o nome da empresa é o que torna o registro útil. Sem identificar quem executava a obra, o relato não serve pra reembolso nem pra prevenir o próximo corte no mesmo trecho.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54355",
        "bairro": "Aponiã",
        "titulo": "Suporte — ONT Sem Energia",
        "cliente": "Sr. Waldir",
        "equipamento": "ONT Huawei EG8145",
        "briefing": "Cliente relata 'sumiu a internet do nada'. Ele já tentou desligar e ligar o roteador, sem sucesso.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "55366",
            "horario": "09h00",
            "assunto": "Sem Internet",
            "endereco": "TRAVESSA DAS PALMEIRAS, 781",
            "cidade": "Alta Floresta",
            "referencia": "Casa de dois andares, grade preta",
            "caixa_atendimento": "AFT 01",
            "porta_ftth": "2",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Sem Internet\n"
                "Descrição O.S. anterior: - Solicitante: atendente Bruna\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99643-8029\n"
                "Ocorrência: Cliente relata perda total do sinal de internet. Informa já ter reiniciado o roteador, sem sucesso."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Ao chegar, você percebe que a ONT está completamente apagada — nenhum LED aceso, nem o de energia.",
             "pergunta": "Qual é o primeiro ponto a verificar?",
             "opcoes": [
                {
                    "texto": "Se a tomada e a fonte de energia da ONT estão funcionando (pode ser só falta de energia no equipamento, não um problema de sinal)",
                    "correta": True,
                    "feedback": "Isso mesmo — sem nenhum LED aceso, o suspeito número um é a alimentação elétrica, não a fibra. É o teste mais simples e deve vir primeiro.",
                },
                {
                    "texto": "Conferir o cordão óptico e o LED de sinal, que é o sintoma mais comum quando o cliente fica sem internet",
                    "correta": False,
                    "feedback": "Seria o caminho certo em quase todo chamado — só que aqui NENHUM led acende, nem o de energia. Sem energia o equipamento não processa luz nenhuma, então não há o que o cordão explique.",
                },
                {
                    "texto": "Substituir a fonte da ONT por uma reserva da van, já que fonte queimada é a falha mais comum nesses equipamentos",
                    "correta": False,
                    "feedback": "A fonte é mesmo suspeita, e talvez seja ela. Mas testar a tomada leva dez segundos e não gasta peça: se o problema for a rede elétrica da casa, a fonte nova morre igual.",
                },
            ]},
            {"cena": "Você descobre que a tomada está sem energia — o problema é da instalação elétrica da casa, não da Norte Tel.",
             "pergunta": "Como você conduz essa situação com o Sr. Waldir?",
             "opcoes": [
                {
                    "texto": "Explica com clareza que o problema é elétrico (fora do escopo da Norte Tel) e sugere testar em outra tomada ou chamar um eletricista",
                    "correta": True,
                    "feedback": "Boa conduta — explicar com transparência o que está fora do seu escopo, sem deixar o cliente sem direção nenhuma.",
                },
                {
                    "texto": "Explica que a tomada está sem energia e deixa a ONT ligada numa extensão até o cliente resolver o elétrico",
                    "correta": False,
                    "feedback": "Resolve o dia de hoje e cria um risco pra depois: extensão improvisada em uso permanente esquenta e é causa comum de incêndio. Se for usar, tem que ficar claro que é provisório e por pouco tempo.",
                },
                {
                    "texto": "Explica que é problema elétrico e orienta o cliente a abrir um novo chamado depois que o eletricista resolver",
                    "correta": False,
                    "feedback": "Está correto no diagnóstico, mas devolve o cliente pra fila sem necessidade: se a ONT liga numa tomada boa, dá pra confirmar que a rede está normal agora e encerrar o assunto de vez.",
                },
            ]},
            {"cena": "O Sr. Waldir testa numa tomada de outro cômodo, com um cabo extensão temporário, e a ONT liga normalmente.",
             "pergunta": "Qual orientação final você dá sobre a solução temporária?",
             "opcoes": [
                {
                    "texto": "Reforça que é uma solução provisória e que ele deve providenciar o reparo elétrico definitivo da tomada original o quanto antes",
                    "correta": True,
                    "feedback": "Correto — deixar claro que é temporário evita que o cliente esqueça do problema elétrico de fundo, que pode causar outros riscos na casa.",
                },
                {
                    "texto": "Orienta que ele pode manter a extensão, desde que use uma de bitola maior e com proteção contra surto",
                    "correta": False,
                    "feedback": "Uma extensão melhor reduz o risco, não elimina: continua sendo ligação provisória em uso contínuo. O reparo da tomada é o que resolve, e adiar isso costuma virar permanente.",
                },
                {
                    "texto": "Orienta que ele mesmo troque a tomada, que é um serviço simples e barato de fazer em casa",
                    "correta": False,
                    "feedback": "Pode até ser simples pra quem sabe, mas orientar cliente a mexer na parte elétrica é assumir um risco que não é nosso. A recomendação é chamar eletricista — e o motivo disso é seguro dele, não burocracia.",
                },
            ]},
            {"cena": "Antes de fechar a O.S., você confirma o sinal óptico normalmente com a ONT já ligada.",
             "pergunta": "O que registrar como causa desse chamado?",
             "opcoes": [
                {
                    "texto": "Falta de energia na tomada da ONT — causa elétrica da residência, sem relação com a rede da Norte Tel",
                    "correta": True,
                    "feedback": "Registro correto e preciso — importante pra não gerar confusão numa eventual reincidência do mesmo chamado.",
                },
                {
                    "texto": "Problema na fonte de alimentação da ONT, resolvido com a troca da tomada utilizada pelo cliente",
                    "correta": False,
                    "feedback": "A fonte estava boa o tempo todo. Registrar defeito de fonte suja o histórico do equipamento e pode gerar troca preventiva desnecessária num aparelho que nunca teve problema.",
                },
                {
                    "texto": "Atendimento improcedente — sem falha identificada na rede da Norte Tel durante a visita técnica",
                    "correta": False,
                    "feedback": "Falha havia, e você identificou qual: a tomada. 'Improcedente' faz parecer que o cliente chamou à toa, e apaga a informação que explicaria um novo chamado igual daqui a um mês.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54410",
        "bairro": "Tiradentes",
        "titulo": "Upgrade de Plano — Verificação de Equipamento",
        "cliente": "Sr. Jonas",
        "equipamento": "ONT antiga (modelo com portas 100 Mbps), medidor óptico",
        "briefing": "Cliente contratou upgrade pra 500 Mega, mas o teste de velocidade não passa de 95 Mbps mesmo com o sinal óptico ótimo.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "59243",
            "horario": "16h30",
            "assunto": "Internet Lenta",
            "endereco": "RUA SETE DE SETEMBRO, 756",
            "cidade": "Cujubim",
            "referencia": "Próximo à igreja",
            "caixa_atendimento": "CUJU 01",
            "porta_ftth": "5",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Lucas\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99341-4689\n"
                "Ocorrência: Cliente contratou upgrade de plano para 500 Mega e relata velocidade abaixo do contratado nos testes realizados."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O sinal óptico está excelente (-17 dBm), mas a velocidade continua travada perto de 95 Mbps.",
             "pergunta": "Qual é a causa mais provável, já que o sinal óptico está ótimo?",
             "opcoes": [
                {
                    "texto": "A porta LAN da ONT (ou do roteador) é limitada a 100 Mbps — um gargalo físico que nada tem a ver com o sinal óptico",
                    "correta": True,
                    "feedback": "Exato. Modelos mais antigos de ONT/roteador têm portas Fast Ethernet (100 Mbps), que travam a velocidade independente da qualidade do sinal óptico ou do plano contratado.",
                },
                {
                    "texto": "O plano do cliente pode ter sido provisionado errado na OLT, entregando bem menos banda do que o contratado",
                    "correta": False,
                    "feedback": "É uma hipótese válida e vale conferir. Mas repare no número: 95 Mbps é exatamente onde uma porta de 100 Mbps satura. Provisionamento errado costuma dar valores quebrados, não esse teto tão redondo.",
                },
                {
                    "texto": "O servidor do teste de velocidade está congestionado — vale repetir a medição em outro horário e outro site",
                    "correta": False,
                    "feedback": "Trocar de servidor é bom hábito quando o número parece estranho. Só que congestionamento oscila, e aqui a velocidade trava sempre no mesmo teto — travar sempre no mesmo ponto aponta gargalo físico.",
                },
            ]},
            {"cena": "Você confirma: a ONT desse cliente é um modelo antigo, só com portas 10/100 Mbps.",
             "pergunta": "O que você faz?",
             "opcoes": [
                {
                    "texto": "Orienta a troca da ONT por um modelo com portas Gigabit, compatível com o plano contratado",
                    "correta": True,
                    "feedback": "Correto — pra entregar de fato os 500 Mega contratados, o equipamento precisa ter portas Gigabit; sem isso, o plano fica limitado artificialmente.",
                },
                {
                    "texto": "Conecta o notebook direto na ONT e usa o Wi-Fi só pros celulares, contornando a limitação da porta LAN",
                    "correta": False,
                    "feedback": "Não contorna nada: a limitação está na própria porta da ONT, então conectar direto nela esbarra no mesmo teto. O gargalo é o equipamento, não o meio.",
                },
                {
                    "texto": "Registra a limitação no atendimento e explica ao cliente que o ganho só virá quando ele trocar de plano",
                    "correta": False,
                    "feedback": "Inverte a causa: o plano já está certo, quem não acompanha é o equipamento. Orientar troca de plano faria o cliente pagar mais e continuar nos mesmos 95 Mbps.",
                },
            ]},
            {"cena": "Com a ONT nova (portas Gigabit) instalada, você refaz o teste de velocidade num notebook conectado por cabo.",
             "pergunta": "O teste mostra 480 Mbps. Isso está adequado?",
             "opcoes": [
                {
                    "texto": "Sim — é normal ficar um pouco abaixo do valor nominal do plano por conta de overhead de rede; está dentro do esperado",
                    "correta": True,
                    "feedback": "Correto. É normal e esperado que a velocidade medida fique levemente abaixo do valor 'redondo' do plano — 480 de 500 Mega é uma entrega saudável.",
                },
                {
                    "texto": "Sim, mas vale testar de novo com o Wi-Fi desligado pra descartar qualquer interferência no resultado",
                    "correta": False,
                    "feedback": "O teste já foi feito por cabo, então o Wi-Fi não entra na conta. Repetir medição que não tem como mudar só alonga a visita.",
                },
                {
                    "texto": "Não — 480 de 500 indica perda no percurso, e vale conferir a crimpagem do cabo antes de encerrar",
                    "correta": False,
                    "feedback": "20 Mbps abaixo do nominal é o overhead normal dos protocolos, presente em qualquer link. Perda por crimpagem ruim aparece como queda bem maior e erro no teste, não como 4% a menos.",
                },
            ]},
            {"cena": "Cliente satisfeito com a velocidade nova. Ele pergunta se o Wi-Fi da ONT nova também vai ficar mais rápido.",
             "pergunta": "Como você responde?",
             "opcoes": [
                {
                    "texto": "Explica que o Wi-Fi também melhora, mas pode variar conforme a distância e obstáculos — o teste mais confiável continua sendo por cabo",
                    "correta": True,
                    "feedback": "Resposta completa e honesta — cria uma expectativa realista sobre a diferença entre velocidade cabeada e sem fio.",
                },
                {
                    "texto": "Garante que o Wi-Fi agora entrega a velocidade do plano em qualquer cômodo, já que o equipamento é novo",
                    "correta": False,
                    "feedback": "A troca melhora o Wi-Fi, mas prometer o número do plano em qualquer cômodo é criar um chamado futuro: parede, distância e aparelho do cliente sempre vão tirar uma parte.",
                },
                {
                    "texto": "Explica que o Wi-Fi da ONT nova é bem melhor e que ele pode desativar o roteador antigo que estava em uso",
                    "correta": False,
                    "feedback": "Pode até ser verdade sobre o Wi-Fi, mas a pergunta era outra e a orientação mexe na rede da casa sem necessidade. Responda o que ele perguntou; mudança de topologia se avalia à parte.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54468",
        "bairro": "Caiari",
        "titulo": "Suporte — Instabilidade Intermitente",
        "cliente": "Dona Iracema",
        "equipamento": "ONT Huawei EG8145, medidor óptico",
        "briefing": "Cliente relata que a internet cai por alguns segundos, várias vezes ao dia, sem padrão aparente.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "55216",
            "horario": "14h00",
            "assunto": "Internet Lenta",
            "endereco": "RUA RIO BRANCO, 243",
            "cidade": "Alto Alegre",
            "referencia": "Perto do campo de futebol",
            "caixa_atendimento": "AAPC 01",
            "porta_ftth": "7",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Aline\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99323-9381\n"
                "Ocorrência: Cliente relata quedas de internet por alguns segundos, diversas vezes ao dia, sem horário definido."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "No momento da visita, tudo parece normal: sinal bom, LEDs certos. Você não consegue reproduzir o problema na hora.",
             "pergunta": "O que fazer diante de um problema intermitente que não se repete na sua frente?",
             "opcoes": [
                {
                    "texto": "Checar o histórico de quedas registrado no sistema (se existir) e inspecionar fisicamente conectores e rota da fibra em busca de pontos de estresse",
                    "correta": True,
                    "feedback": "Boa abordagem — problemas intermitentes muitas vezes têm causa física (conector meio solto, dobra, calor) que só aparece em certas condições, então vale investigar mesmo sem reproduzir na hora.",
                },
                {
                    "texto": "Deixar a ONT em monitoramento e voltar em outro dia, quando houver mais chance de o problema estar acontecendo",
                    "correta": False,
                    "feedback": "Marcar retorno pra 'talvez pegar o problema' custa uma visita e não garante nada. Intermitência quase sempre deixa rastro físico — dá pra procurar agora, sem depender da sorte.",
                },
                {
                    "texto": "Refazer o teste de velocidade várias vezes ao longo da visita, pra tentar flagrar a queda enquanto está no local",
                    "correta": False,
                    "feedback": "Vale como pano de fundo, mas queda intermitente pode ter janela de dias. O que aparece na inspeção do conector e da rota leva minutos e costuma explicar o caso.",
                },
            ]},
            {"cena": "Ao inspecionar o conector óptico da ONT, você percebe que ele está mal encaixado, quase saindo — um leve toque no cabo faz o LED PON piscar.",
             "pergunta": "Isso é compatível com o problema relatado?",
             "opcoes": [
                {
                    "texto": "Sim — um conector mal encaixado pode cair momentaneamente com vibração da casa (alguém passando perto, porta batendo), causando quedas intermitentes",
                    "correta": True,
                    "feedback": "Exatamente esse tipo de causa física explica quedas que 'vêm e vão' sem padrão claro — pequenas vibrações no dia a dia bastam pra interromper um encaixe frouxo.",
                },
                {
                    "texto": "Sim, mas o mais provável é que o encaixe frouxo tenha surgido agora, ao você manusear o equipamento na visita",
                    "correta": False,
                    "feedback": "Pode acontecer, e por isso vale checar antes de mexer. Só que o sintoma relatado bate exatamente com esse achado — atribuir ao próprio manuseio joga fora a pista mais forte que você tem.",
                },
                {
                    "texto": "Sim, e por isso o certo é trocar a ONT: um conector que afrouxa sozinho indica desgaste do encaixe do equipamento",
                    "correta": False,
                    "feedback": "O encaixe frouxo quase sempre é do cordão ou de como ele foi acomodado, não da ONT. Trocar o equipamento sem confirmar isso é gastar peça e ainda deixar a causa real no lugar.",
                },
            ]},
            {"cena": "Você limpa o conector, reencaixa até sentir o 'clique' de segurança, e confirma que balançar o cabo não afeta mais o LED.",
             "pergunta": "O que fazer em seguida?",
             "opcoes": [
                {
                    "texto": "Medir o sinal óptico pra confirmar que ficou dentro da faixa ideal, e orientar a cliente a avisar se as quedas voltarem a acontecer",
                    "correta": True,
                    "feedback": "Correto — confirmar com o medidor fecha o diagnóstico, e deixar a porta aberta pra um retorno garante que, se o problema persistir por outra causa, ele seja investigado.",
                },
                {
                    "texto": "Registrar a causa encontrada e orientar a cliente sobre as quedas, já que o encaixe firme resolve o problema",
                    "correta": False,
                    "feedback": "Falta o passo que confirma: sem medir, você não sabe se o conector está apenas encaixado ou realmente entregando sinal na faixa. É a medição que fecha o diagnóstico.",
                },
                {
                    "texto": "Medir o sinal e, estando bom, garantir à cliente que o problema está definitivamente resolvido",
                    "correta": False,
                    "feedback": "A medição está certa; a promessa é que não. Num caso intermitente, o correto é dizer que a causa provável foi corrigida e pedir que ela avise se voltar — isso mantém o histórico vivo.",
                },
            ]},
            {"cena": "Uma semana depois, Dona Iracema liga dizendo que não caiu mais nenhuma vez.",
             "pergunta": "O que isso confirma sobre o diagnóstico original?",
             "opcoes": [
                {
                    "texto": "Que a causa realmente era o conector mal encaixado — o registro dessa causa no histórico ajuda em atendimentos parecidos no futuro",
                    "correta": True,
                    "feedback": "Isso — o retorno positivo do cliente confirma o diagnóstico, e manter esse tipo de causa registrada ajuda outros técnicos a reconhecerem o padrão mais rápido.",
                },
                {
                    "texto": "Que o diagnóstico estava certo, e que agora o chamado pode ser encerrado como resolvido no sistema",
                    "correta": False,
                    "feedback": "Encerrar está certo. O que se perde é registrar a causa confirmada: sem isso, um chamado parecido no futuro começa do zero em vez de partir do que já se aprendeu nesta casa.",
                },
                {
                    "texto": "Que o problema provavelmente era da rede externa e se resolveu sozinho junto com a manutenção do trecho",
                    "correta": False,
                    "feedback": "Não houve manutenção externa nesse período, e havia uma causa física identificada no local. Atribuir à rede apaga um diagnóstico bom e ainda sugere instabilidade que não existiu.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54520",
        "bairro": "Embratel",
        "titulo": "Instalação — Cliente com Plano de Alta Demanda",
        "cliente": "Estúdio de Design Criativo Prisma",
        "equipamento": "ONT Huawei EG8145, roteador profissional",
        "briefing": "Estúdio com 6 pessoas que trabalham com upload constante de arquivos grandes (vídeo/design). Contrataram um plano simétrico.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "53230",
            "horario": "13h30",
            "assunto": "Instalação Fibra Optica",
            "endereco": "AVENIDA BRASIL, 429",
            "cidade": "Cacoal",
            "referencia": "Ponto branco com azul, casa nos fundos",
            "caixa_atendimento": "CWL 02",
            "porta_ftth": "4",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Instalação Fibra Optica\n"
                "Descrição O.S. anterior: - Solicitante: atendente Patrícia\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99166-8141\n"
                "Ocorrência: Cliente (estúdio, 6 usuários) contratou plano simétrico de alta demanda para upload constante de arquivos grandes."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Instalação, manutenção ou retirada de rede Fibra Optica",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O cliente pergunta por que contratou 'plano simétrico' e o que isso quer dizer na prática pro trabalho dele.",
             "pergunta": "Como você explica de forma simples?",
             "opcoes": [
                {
                    "texto": "Explica que simétrico significa velocidade de upload igual à de download — importante pra quem envia arquivos grandes o tempo todo, não só baixa coisas",
                    "correta": True,
                    "feedback": "Boa explicação, direto ao ponto que importa pro dia a dia do cliente: planos comuns têm upload bem mais lento que download, o que atrapalharia o trabalho deles.",
                },
                {
                    "texto": "Explica que simétrico garante a velocidade contratada o tempo todo, sem a variação dos planos comuns",
                    "correta": False,
                    "feedback": "Simetria é sobre a relação entre subida e descida, não sobre garantia de banda. Prometer velocidade constante é criar expectativa que nenhum plano de acesso cumpre.",
                },
                {
                    "texto": "Explica que simétrico significa que a internet dele tem prioridade na rede sobre os clientes residenciais",
                    "correta": False,
                    "feedback": "Prioridade é outra coisa, e não vem embutida na simetria. Se o estúdio precisar de tratamento diferenciado, isso é um serviço à parte — vender isso como incluso gera frustração depois.",
                },
            ]},
            {"cena": "Ao medir, o sinal óptico está ótimo, e o teste de velocidade confirma valores altos e simétricos.",
             "pergunta": "O que mais vale verificar antes de considerar a instalação pronta pra esse tipo de uso profissional?",
             "opcoes": [
                {
                    "texto": "Se o roteador aguenta bem 6 pessoas conectadas simultaneamente com tráfego pesado, sem gargalo — um roteador doméstico simples pode não bastar",
                    "correta": True,
                    "feedback": "Correto — sinal ótimo até a ONT não garante boa experiência se o roteador não aguentar a carga de vários usuários fazendo upload pesado ao mesmo tempo.",
                },
                {
                    "texto": "Se o Wi-Fi cobre bem toda a área do estúdio, medindo o sinal nos pontos mais distantes de trabalho",
                    "correta": False,
                    "feedback": "Cobertura importa, mas não é o gargalo aqui: com seis pessoas subindo arquivo pesado ao mesmo tempo, o roteador satura antes de a cobertura ser problema. É a capacidade que precisa ser checada.",
                },
                {
                    "texto": "Se o cabeamento interno do estúdio é Cat5e ou superior, pra não limitar a velocidade nas estações de trabalho",
                    "correta": False,
                    "feedback": "Vale conferir, e é uma boa pergunta. Mas o cabo só entra na conta se ele existir — antes disso, é o roteador entregue que define quantas sessões pesadas simultâneas a rede aguenta.",
                },
            ]},
            {"cena": "Você percebe que o roteador entregue é um modelo doméstico básico, provavelmente insuficiente pro uso pesado com 6 pessoas.",
             "pergunta": "Qual é a orientação correta?",
             "opcoes": [
                {
                    "texto": "Sugerir ao cliente (ou à central) o upgrade pra um roteador de perfil profissional, mais adequado ao uso intenso simultâneo",
                    "correta": True,
                    "feedback": "Isso — um plano de alta performance merece um equipamento à altura, senão o cliente não sente o benefício completo do que contratou.",
                },
                {
                    "texto": "Instalar o roteador entregue e registrar no atendimento a limitação, deixando a avaliação pro cliente depois",
                    "correta": False,
                    "feedback": "Registrar é melhor que calar, mas o cliente não tem como avaliar sozinho algo técnico que ele nem sabe que existe. Sem a orientação clara agora, o chamado por lentidão volta em poucas semanas.",
                },
                {
                    "texto": "Instalar o roteador entregue e configurar limite de banda por aparelho, pra nenhum usuário derrubar os outros",
                    "correta": False,
                    "feedback": "Divide melhor um recurso que continua insuficiente: todo mundo passa a ser lento de forma organizada. Serve como paliativo, não como resposta ao uso profissional que ele contratou.",
                },
            ]},
            {"cena": "O responsável pelo estúdio agradece a orientação e pede uma recomendação rápida de como configurar a rede.",
             "pergunta": "Qual sugestão prática faz mais sentido pra esse ambiente de trabalho?",
             "opcoes": [
                {
                    "texto": "Sugerir cabo de rede pra estações que fazem upload pesado com frequência, deixando o Wi-Fi pra dispositivos móveis e uso ocasional",
                    "correta": True,
                    "feedback": "Boa recomendação prática — cabo dá estabilidade máxima pra quem depende de upload constante, e Wi-Fi cobre bem o resto sem sobrecarregar a rede sem fio.",
                },
                {
                    "texto": "Sugerir dividir a rede em duas faixas, com os computadores no 5 GHz e os celulares no 2,4 GHz",
                    "correta": False,
                    "feedback": "Organiza e ajuda um pouco, mas o upload pesado continua disputando o mesmo ar. Pra estação que sobe arquivo o dia inteiro, o cabo entrega estabilidade que nenhuma separação de faixa alcança.",
                },
                {
                    "texto": "Sugerir um repetidor em cada sala do estúdio, pra garantir sinal forte em qualquer ponto do ambiente",
                    "correta": False,
                    "feedback": "Repetidor multiplica cobertura e divide banda: num ambiente de upload pesado é exatamente o oposto do necessário. Se faltar cobertura, o caminho são pontos de acesso ligados por cabo.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54577",
        "bairro": "Flodoaldo Pontes Pinto",
        "titulo": "Suporte — Reflexão Óptica Alta",
        "cliente": "Sr. Deusdete",
        "equipamento": "ONT Huawei EG8145, medidor óptico",
        "briefing": "Cliente com quedas frequentes de sinal, mesmo com potência óptica dentro da faixa. Instalação já tem 2 anos.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "51137",
            "horario": "15h00",
            "assunto": "Internet Lenta",
            "endereco": "RUA SETE DE SETEMBRO, 369",
            "cidade": "São Miguel",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "SMGE 02",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Mayara\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99901-6142\n"
                "Ocorrência: Cliente relata quedas frequentes de sinal. Instalação com 2 anos de uso, sem alteração recente reportada."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "A potência óptica medida está em -18 dBm (dentro da faixa ideal), mas mesmo assim há quedas frequentes de conexão.",
             "pergunta": "Já que a potência está boa, o que mais pode causar instabilidade num sinal óptico?",
             "opcoes": [
                {
                    "texto": "Reflexão óptica alta — um conector não assentado corretamente pode refletir parte da luz de volta, mesmo com a potência medida parecendo boa",
                    "correta": True,
                    "feedback": "Exato. Potência (dBm) e reflexão (ORL) são medidas diferentes — um conector mal assentado ou desgastado pode ter potência OK mas reflexão ruim, causando instabilidade.",
                },
                {
                    "texto": "Variação de temperatura ao longo do dia, que altera levemente a potência entregue pelo laser da OLT e derruba a conexão nos horários mais quentes",
                    "correta": False,
                    "feedback": "Temperatura afeta mesmo os componentes ópticos, mas na casa de décimos de dB — longe de derrubar um enlace com margem boa. Procure a causa no que muda de repente, não no que muda devagar.",
                },
                {
                    "texto": "Sobrecarga do splitter da CTO, que perde capacidade quando muitos clientes do mesmo ramal usam a rede ao mesmo tempo",
                    "correta": False,
                    "feedback": "Splitter é passivo: ele divide a luz sempre igual, com ou sem tráfego. Congestionamento existe, mas aparece como lentidão no horário de pico, não como queda de sinal óptico.",
                },
            ]},
            {"cena": "Você desconecta e reconecta o conector óptico na ONT, limpando bem antes de reencaixar.",
             "pergunta": "Por que a limpeza é especialmente importante nesse tipo de problema?",
             "opcoes": [
                {
                    "texto": "Poeira ou resíduo na ponta do conector aumenta bastante a reflexão da luz, que é justamente a suspeita nesse caso",
                    "correta": True,
                    "feedback": "Correto — sujeira na ponta do conector é uma das causas mais comuns de reflexão óptica alta, mesmo quando a potência de sinal parece normal.",
                },
                {
                    "texto": "Porque o resíduo na ponta impede o encaixe completo do conector, deixando uma folga que faz o cabo se soltar com o tempo",
                    "correta": False,
                    "feedback": "Sujeira atrapalha o contato, mas o problema aqui é óptico, não mecânico: mesmo bem encaixado, a partícula fica no caminho da luz e devolve parte dela — é a reflexão que derruba o enlace.",
                },
                {
                    "texto": "Porque a poeira acumulada absorve a luz e reduz a potência que chega até a ONT, derrubando a leitura do medidor",
                    "correta": False,
                    "feedback": "Se fosse só absorção, a potência teria caído — e ela está boa, em -18 dBm. O que a partícula faz aqui é refletir luz de volta, um efeito que a medição de potência sozinha não mostra.",
                },
            ]},
            {"cena": "Depois da limpeza e reencaixe cuidadoso, você monitora por alguns minutos e não vê mais nenhuma queda.",
             "pergunta": "O que fazer antes de encerrar o atendimento?",
             "opcoes": [
                {
                    "texto": "Confirmar novamente a potência óptica, orientar o cliente a observar por mais alguns dias, e registrar a causa (reflexão por conector sujo) no histórico",
                    "correta": True,
                    "feedback": "Boa prática — confirmar tecnicamente, dar um prazo de observação realista, e documentar a causa ajuda em qualquer atendimento futuro relacionado.",
                },
                {
                    "texto": "Confirmar a potência, registrar a limpeza feita e encerrar informando ao cliente que a causa foi resolvida no local",
                    "correta": False,
                    "feedback": "Está quase completo, e falta o que mais importa num caso de instabilidade: pedir que o cliente observe alguns dias. Sem essa combinação, uma queda daqui a uma semana começa como chamado novo.",
                },
                {
                    "texto": "Deixar o notebook conectado medindo a estabilidade por meia hora antes de sair, pra garantir que não cai mais nenhuma vez",
                    "correta": False,
                    "feedback": "Meia hora não prova nada num problema que tem janela de dias, e ainda prende você numa visita que já cumpriu o objetivo. Quem confirma isso é o acompanhamento do cliente, não o cronômetro.",
                },
            ]},
            {"cena": "O Sr. Deusdete pergunta se ele mesmo pode limpar o conector no futuro, caso o problema volte.",
             "pergunta": "Qual orientação é mais adequada?",
             "opcoes": [
                {
                    "texto": "Explica que essa limpeza exige uma caneta/kit específico e cuidado técnico, e que o mais seguro é chamar a assistência caso o problema volte",
                    "correta": True,
                    "feedback": "Orientação responsável — limpeza de conector óptico malfeita pode piorar o problema; melhor recomendar suporte técnico do que incentivar uma tentativa sem ferramenta adequada.",
                },
                {
                    "texto": "Explica o procedimento e deixa com ele um cotonete e álcool isopropílico, orientando a limpar com cuidado se o problema voltar",
                    "correta": False,
                    "feedback": "Álcool comum deixa resíduo e fiapo de algodão na face do conector — o resultado costuma ser pior que a sujeira original. A limpeza de ferrolho tem material próprio justamente por isso.",
                },
                {
                    "texto": "Explica que ele pode simplesmente desconectar e reconectar o cordão algumas vezes, que isso já remove a maior parte da sujeira",
                    "correta": False,
                    "feedback": "Reconectar arrasta a partícula pela face polida e pode riscar o ferrolho de vez, transformando um problema reversível em troca de cordão. Melhor ele não manusear e chamar a gente.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54630",
        "bairro": "Jardim América",
        "titulo": "Suporte — Casa Grande com Sinal Fraco no Fundo",
        "cliente": "Família Bezerra",
        "equipamento": "ONT com Wi-Fi integrado",
        "briefing": "A internet funciona bem na sala, mas o Wi-Fi praticamente não chega no quarto dos fundos, que fica longe do roteador.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "56676",
            "horario": "13h30",
            "assunto": "Realizar serviços - configurações",
            "endereco": "RUA DAS FLORES, 195",
            "cidade": "Conselvan",
            "referencia": "Próximo à igreja",
            "caixa_atendimento": "AYPO 02",
            "porta_ftth": "2",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Rafael\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99197-1951\n"
                "Ocorrência: Cliente relata que o Wi-Fi não chega no quarto dos fundos, distante do roteador. Solicita verificação técnica no local."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você mede o sinal Wi-Fi no quarto dos fundos: está muito fraco, quase inutilizável.",
             "pergunta": "Qual é a melhor solução técnica pra esse cenário, considerando que é uma casa grande?",
             "opcoes": [
                {
                    "texto": "Instalar um sistema mesh (múltiplos pontos de acesso trabalhando juntos), que cobre a casa toda com uma rede única e contínua",
                    "correta": True,
                    "feedback": "Correto — pra casas grandes com pontos mortos, mesh é a solução mais robusta: os pontos conversam entre si e o dispositivo troca de ponto sem cair a conexão.",
                },
                {
                    "texto": "Reposicionar o roteador atual pra um ponto mais central da casa, longe de parede de concreto e de espelho, e refazer a medição no quarto dos fundos",
                    "correta": False,
                    "feedback": "Boa ideia como primeiro teste, e em casa pequena costuma resolver. Numa casa grande, porém, você só muda o cômodo que fica sem sinal — a área total que um único ponto cobre continua a mesma.",
                },
                {
                    "texto": "Instalar um repetidor simples no meio do caminho, criando uma segunda rede pro quarto dos fundos",
                    "correta": False,
                    "feedback": "O repetidor cria uma rede separada (o aparelho não troca sozinho) e divide a banda pela metade, já que fala e escuta no mesmo rádio. Resolve na marra, mas entrega uma experiência pior que a do mesh.",
                },
            ]},
            {"cena": "A família pergunta a diferença entre o mesh que você sugeriu e um simples 'repetidor de sinal' que um vizinho usa.",
             "pergunta": "Como você explica a diferença de forma simples?",
             "opcoes": [
                {
                    "texto": "O repetidor simples geralmente cria uma segunda rede (o dispositivo pode ficar 'preso' nela) e ainda perde velocidade; o mesh cria uma rede única e troca o dispositivo de ponto automaticamente, sem perceber",
                    "correta": True,
                    "feedback": "Boa explicação prática — é exatamente essa a principal vantagem do mesh sobre um repetidor comum: continuidade sem o usuário precisar trocar de rede manualmente.",
                },
                {
                    "texto": "O mesh usa uma frequência exclusiva pra conversar entre os pontos, enquanto o repetidor divide a mesma internet contratada com a casa toda",
                    "correta": False,
                    "feedback": "Alguns mesh têm mesmo um canal dedicado, mas não é isso que separa os dois: a diferença que o cliente sente é a rede única com troca automática, contra a segunda rede em que o aparelho fica preso.",
                },
                {
                    "texto": "O repetidor precisa ser da mesma marca do roteador pra funcionar, e o mesh funciona com qualquer equipamento da casa",
                    "correta": False,
                    "feedback": "É o contrário: repetidor costuma funcionar com qualquer marca, e é o mesh que precisa ser do mesmo sistema pra os pontos se enxergarem. Compatibilidade não é o ponto forte aqui.",
                },
            ]},
            {"cena": "Você instala um ponto mesh adicional num corredor central da casa, equidistante da sala e do quarto dos fundos.",
             "pergunta": "Por que a posição do ponto adicional importa?",
             "opcoes": [
                {
                    "texto": "Um ponto mal posicionado (muito perto do roteador principal, por exemplo) não estende a cobertura de forma eficiente pro ponto que estava fraco",
                    "correta": True,
                    "feedback": "Isso — a posição estratégica é o que faz o mesh funcionar de verdade; colocar o ponto extra perto demais do roteador principal desperdiça a cobertura.",
                },
                {
                    "texto": "Porque o ponto adicional deve ficar o mais longe possível do roteador principal, já que assim a soma das duas áreas de cobertura fica maior dentro da casa",
                    "correta": False,
                    "feedback": "Longe demais e o próprio ponto adicional recebe sinal fraco do roteador — ele repassa pra frente a má qualidade que recebeu. A cobertura aumenta no mapa e piora na prática.",
                },
                {
                    "texto": "Porque quanto mais perto do roteador principal, mais forte fica o ponto adicional e melhor a rede",
                    "correta": False,
                    "feedback": "Perto demais os dois cobrem a mesma área e sobra o mesmo ponto cego de antes. O ganho real vem do meio-termo: perto o bastante pra receber bem, longe o bastante pra estender.",
                },
            ]},
            {"cena": "Depois da instalação, o sinal no quarto dos fundos está forte e a família testa andando pela casa sem perceber quedas.",
             "pergunta": "O que mais vale orientar a família antes de encerrar o atendimento?",
             "opcoes": [
                {
                    "texto": "Que os pontos mesh precisam ficar sempre ligados e conectados à energia pra manter a cobertura funcionando — não são acessórios que podem ser desligados à vontade",
                    "correta": True,
                    "feedback": "Orientação importante — é comum famílias desligarem tomadas 'pra economizar energia' sem perceber que aquele ponto é parte essencial da rede.",
                },
                {
                    "texto": "Que o ponto adicional pode ser desligado durante a noite pra economizar energia, já que ninguém usa o quarto dos fundos dormindo",
                    "correta": False,
                    "feedback": "O consumo de um ponto mesh é irrisório, e desligar todo dia significa esperar ele voltar a formar a malha toda manhã. Ainda por cima, é justamente à noite que o celular fica carregando no quarto.",
                },
                {
                    "texto": "Que se quiserem mais cobertura no futuro, basta ligar um repetidor comum a partir de um dos pontos mesh já instalados",
                    "correta": False,
                    "feedback": "Misturar repetidor comum no mesh devolve o problema que o mesh resolveu: uma segunda rede, sem troca automática. Se precisar de mais alcance, o caminho é acrescentar outro ponto do mesmo sistema.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54689",
        "bairro": "Cidade Nova",
        "titulo": "Suporte — Cliente Confuso com Rede 5GHz",
        "cliente": "Sr. Anísio",
        "equipamento": "Roteador dual-band",
        "briefing": "Cliente reclama que a rede '5G' da internet dele 'não pega em lugar nenhum', enquanto a outra rede pega em toda a casa.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "51686",
            "horario": "15h30",
            "assunto": "Realizar serviços - configurações",
            "endereco": "AVENIDA BRASIL, 477",
            "cidade": "Aripuanã",
            "referencia": "Ponto branco com azul, casa nos fundos",
            "caixa_atendimento": "AYP 02",
            "porta_ftth": "3",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Aline\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99911-8131\n"
                "Ocorrência: Cliente relata que a rede de 5GHz do roteador não alcança a maior parte da casa, diferente da rede de 2.4GHz."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você percebe que o cliente confundiu o nome '5GHz' (frequência de Wi-Fi) com '5G' (tecnologia de internet móvel de celular).",
             "pergunta": "Qual é a explicação mais clara pra desfazer essa confusão?",
             "opcoes": [
                {
                    "texto": "Explicar que são duas coisas diferentes: 5GHz é uma das duas frequências de Wi-Fi da casa dele (mais rápida, mas de alcance menor), sem relação com o '5G' do celular",
                    "correta": True,
                    "feedback": "Boa explicação — essa confusão de nomes é super comum, e esclarecer evita frustração desnecessária do cliente.",
                },
                {
                    "texto": "Explicar que o 5GHz é a mesma tecnologia do 5G do celular, só que aplicada dentro de casa pelo roteador em vez da antena da operadora",
                    "correta": False,
                    "feedback": "É a confusão que ele já tinha, agora confirmada por você. São coisas sem parentesco: uma é frequência de Wi-Fi dentro de casa, a outra é padrão de telefonia móvel. Confirmar o engano hoje gera cobrança amanhã.",
                },
                {
                    "texto": "Explicar que o 5GHz é a versão anterior do 5G, e que o roteador dele receberá a atualização quando a operadora liberar",
                    "correta": False,
                    "feedback": "Não existe essa atualização, e o 5GHz não vira 5G. Criar essa expectativa é pior que não explicar: o cliente vai cobrar uma entrega que nunca vai acontecer.",
                },
            ]},
            {"cena": "Você explica que a rede 5GHz é mais rápida, mas atravessa paredes com mais dificuldade que a rede 2.4GHz.",
             "pergunta": "Qual orientação prática faz sentido pro Sr. Anísio?",
             "opcoes": [
                {
                    "texto": "Usar a rede 5GHz nos cômodos próximos ao roteador (mais velocidade) e a 2.4GHz nos cômodos mais distantes (mais alcance)",
                    "correta": True,
                    "feedback": "Exatamente — essa é a lógica prática de uso das duas bandas: velocidade perto, alcance longe.",
                },
                {
                    "texto": "Deixar o celular sempre na rede 5GHz, que é a mais rápida, e usar a 2.4GHz só nos aparelhos antigos que não enxergam a outra",
                    "correta": False,
                    "feedback": "Faz sentido pra velocidade e ignora o alcance: no cômodo distante o 5GHz cai, e o aparelho fica insistindo numa rede fraca em vez de usar a 2.4GHz, que ali entregaria mais.",
                },
                {
                    "texto": "Configurar as duas redes com o mesmo nome e senha, deixando o celular decidir sozinho qual usar em cada cômodo da casa",
                    "correta": False,
                    "feedback": "É uma boa ideia, e existe como recurso do roteador (banda unificada). Mas só nomear igual não basta em todo aparelho: sem o recurso ativado, alguns grudam numa banda e não largam.",
                },
            ]},
            {"cena": "O cliente pergunta se dá pra ter só UMA rede Wi-Fi que 'escolha sozinha' a melhor banda automaticamente.",
             "pergunta": "Como você responde?",
             "opcoes": [
                {
                    "texto": "Sim — muitos roteadores modernos têm essa opção (banda unificada/'smart connect'), que ativa e você pode habilitar no painel do roteador",
                    "correta": True,
                    "feedback": "Correto — essa função existe e resolve exatamente esse tipo de dúvida recorrente, simplificando a experiência do cliente.",
                },
                {
                    "texto": "Sim, mas o recurso costuma deixar a conexão instável em casa com muitos aparelhos, então o padrão é manter as duas redes separadas",
                    "correta": False,
                    "feedback": "Instabilidade acontece em casos pontuais com aparelho antigo, não como regra. Desaconselhar por padrão priva o cliente de um recurso que resolve exatamente a dúvida dele.",
                },
                {
                    "texto": "Sim, e ativando esse recurso o roteador passa a somar a velocidade das duas frequências numa conexão única mais rápida",
                    "correta": False,
                    "feedback": "O recurso escolhe uma banda por vez, não soma as duas. Prometer velocidade somada é vender um ganho que não existe e que o cliente vai tentar medir depois.",
                },
            ]},
            {"cena": "Você ativa a opção de banda unificada no roteador do Sr. Anísio.",
             "pergunta": "O que é importante testar antes de encerrar o atendimento?",
             "opcoes": [
                {
                    "texto": "Reconectar os dispositivos da casa na rede (já que o nome pode ter mudado) e confirmar que a internet funciona em pelo menos dois cômodos diferentes",
                    "correta": True,
                    "feedback": "Correto — mudar a configuração de rede geralmente exige reconectar os aparelhos, e testar em mais de um cômodo confirma que a solução realmente cobre a necessidade dele.",
                },
                {
                    "texto": "Confirmar no painel do roteador que as duas frequências continuam ativas e que o recurso ficou salvo na configuração",
                    "correta": False,
                    "feedback": "Confere o lado do roteador e ignora o lado que quebra: com o nome da rede mudando, os aparelhos da casa saem do ar. Quem precisa ser testado é a TV, o celular, a impressora.",
                },
                {
                    "texto": "Medir a velocidade num aparelho conectado na rede unificada, pra confirmar que o recurso não degradou o desempenho",
                    "correta": False,
                    "feedback": "Medir é útil, mas não é o risco desta mudança. O problema previsível aqui é aparelho sem reconectar — velocidade boa num celular não diz nada sobre a TV que ficou offline.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54741",
        "bairro": "Bairro Redenção",
        "titulo": "Suporte — Pedido de Controle Parental",
        "cliente": "Sra. Valquíria",
        "equipamento": "Roteador com app de gerenciamento",
        "briefing": "Cliente quer limitar o tempo de internet do filho adolescente e bloquear alguns sites.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "54947",
            "horario": "10h00",
            "assunto": "Realizar serviços - configurações",
            "endereco": "AVENIDA MARECHAL RONDON, 670",
            "cidade": "Juína",
            "referencia": "Esquina com a rua principal",
            "caixa_atendimento": "JNA 02",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Camila\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99955-6599\n"
                "Ocorrência: Cliente solicita configuração de controle parental, para limitar o tempo de acesso e bloquear determinados sites."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "A Sra. Valquíria pergunta se isso é algo que só um técnico consegue configurar, ou se ela mesma pode fazer depois.",
             "pergunta": "Como você orienta ela da melhor forma?",
             "opcoes": [
                {
                    "texto": "Configura o controle parental básico agora, e mostra pra ela, no app do roteador, como ajustar horários e bloqueios por conta própria no futuro",
                    "correta": True,
                    "feedback": "Ótima abordagem — resolve a necessidade imediata e ainda deixa a cliente autônoma pra pequenos ajustes futuros, sem precisar chamar suporte toda hora.",
                },
                {
                    "texto": "Configura o controle parental completo com todas as regras que ela descrever agora, deixando tudo pronto pra não precisar de retorno",
                    "correta": False,
                    "feedback": "Deixar pronto é bom, mas a necessidade dela vai mudar (férias, prova, castigo) e ela ficaria dependente de visita a cada ajuste. Ensinar a mexer no app entrega autonomia junto com o serviço.",
                },
                {
                    "texto": "Explica que o controle parental fica melhor configurado direto no celular do filho, e orienta ela a instalar um aplicativo próprio pra isso",
                    "correta": False,
                    "feedback": "App no celular do filho é uma alternativa real, mas ele desinstala. O controle no roteador vale pra rede toda da casa e não depende da colaboração de quem está sendo controlado.",
                },
            ]},
            {"cena": "Você configura um horário de bloqueio noturno pro dispositivo do filho adolescente.",
             "pergunta": "Qual cuidado técnico é importante nessa configuração?",
             "opcoes": [
                {
                    "texto": "Vincular a regra ao dispositivo específico dele (por endereço MAC ou identificação no app), não à rede toda, pra não bloquear os outros moradores da casa",
                    "correta": True,
                    "feedback": "Correto — controle parental bem feito é direcionado, não afeta o restante da família sem necessidade.",
                },
                {
                    "texto": "Vincular a regra ao endereço IP que o aparelho dele recebeu, que é o identificador mais direto de encontrar no painel do roteador",
                    "correta": False,
                    "feedback": "O IP é distribuído por tempo determinado e muda: basta o celular reconectar noutro momento pra pegar outro endereço e escapar da regra. O MAC acompanha o aparelho, o IP não.",
                },
                {
                    "texto": "Vincular a regra ao nome do dispositivo que aparece na lista do roteador, que é mais fácil da cliente reconhecer depois no aplicativo",
                    "correta": False,
                    "feedback": "O nome ajuda a identificar na tela, e vale usar como etiqueta. Mas ele vem do próprio aparelho e pode ser trocado nas configurações do celular em dez segundos — não serve de trava.",
                },
            ]},
            {"cena": "A cliente também pede pra bloquear alguns sites específicos.",
             "pergunta": "Qual é a forma tecnicamente adequada de fazer isso pelo roteador?",
             "opcoes": [
                {
                    "texto": "Usar a função de bloqueio de conteúdo/DNS do próprio roteador, adicionando os sites ou categorias na lista de restrição",
                    "correta": True,
                    "feedback": "Isso — a maioria dos roteadores modernos com controle parental já tem essa função integrada, sem precisar de nenhum equipamento extra.",
                },
                {
                    "texto": "Cadastrar os sites na lista de bloqueio do navegador do computador do filho, que é onde o acesso realmente acontece",
                    "correta": False,
                    "feedback": "Vale zero na prática: ele abre outro navegador, ou usa o celular. Bloqueio que fica no aparelho controlado só funciona enquanto o controlado colaborar.",
                },
                {
                    "texto": "Configurar o roteador pra usar um servidor DNS com filtro de conteúdo, aplicando o bloqueio a todos os aparelhos da casa de uma vez",
                    "correta": False,
                    "feedback": "Boa solução, e é praticamente o que a função do roteador faz por baixo. O detalhe é que ela vale pra casa inteira: se a cliente quer bloquear só pro filho, a regra tem que ser por dispositivo.",
                },
            ]},
            {"cena": "Configuração concluída e testada. A Sra. Valquíria agradece e pergunta se isso vai deixar a internet mais lenta pro resto da casa.",
             "pergunta": "Como você responde?",
             "opcoes": [
                {
                    "texto": "Explica que não — o controle parental filtra acesso, não consome banda adicional nem afeta a velocidade dos outros dispositivos",
                    "correta": True,
                    "feedback": "Resposta correta e tranquilizadora — controle parental é sobre permissão de acesso, não sobre desempenho de rede.",
                },
                {
                    "texto": "Explica que pode haver uma pequena perda de velocidade, já que cada acesso passa a ser conferido na lista antes de ser liberado",
                    "correta": False,
                    "feedback": "A conferência acontece na resolução do nome do site, custa milissegundos e não entra na banda. Sugerir perda de velocidade dá à cliente um motivo pra desligar a proteção depois.",
                },
                {
                    "texto": "Explica que a velocidade não muda, mas que o roteador pode esquentar mais por estar processando as regras o tempo todo",
                    "correta": False,
                    "feedback": "Filtrar nome de site é tarefa leve, e não é o que aquece roteador. Criar essa preocupação faz a cliente associar o recurso a desgaste de equipamento sem nenhuma razão técnica.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54803",
        "bairro": "Bairro Nacional",
        "titulo": "Suporte — Muitos Dispositivos IoT Derrubando o Wi-Fi",
        "cliente": "Sr. Régis",
        "equipamento": "Roteador doméstico comum",
        "briefing": "Cliente tem cerca de 25 dispositivos conectados (lâmpadas inteligentes, câmeras, tomadas Wi-Fi) e reclama de quedas frequentes.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "50615",
            "horario": "15h30",
            "assunto": "Internet Lenta",
            "endereco": "RUA DOS IPÊS, 260",
            "cidade": "Colniza",
            "referencia": "Ponto branco com azul, casa nos fundos",
            "caixa_atendimento": "CNIZ 02",
            "porta_ftth": "7",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Fernanda\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99550-2753\n"
                "Ocorrência: Cliente relata quedas frequentes de conexão. Possui grande quantidade de dispositivos conectados (aproximadamente 25, entre lâmpadas, câmeras e tomadas inteligentes)."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você confere no painel do roteador: são realmente muitos dispositivos IoT conectados na mesma rede usada pelos celulares e notebooks da família.",
             "pergunta": "Por que isso pode causar instabilidade?",
             "opcoes": [
                {
                    "texto": "Muitos dispositivos IoT ao mesmo tempo podem sobrecarregar a tabela de conexões do roteador doméstico, que tem um limite prático de dispositivos simultâneos bem gerenciados",
                    "correta": True,
                    "feedback": "Isso — roteadores domésticos comuns não são pensados pra dezenas de dispositivos simultâneos; a sobrecarga pode causar quedas e lentidão pra todo mundo na rede.",
                },
                {
                    "texto": "Porque cada dispositivo IoT conectado consome uma parte fixa da banda contratada, mesmo quando está parado sem transmitir nada",
                    "correta": False,
                    "feedback": "Parado, um sensor consome banda quase nula. O gargalo aqui não é a banda: é a quantidade de conexões simultâneas que o roteador doméstico precisa manter em memória ao mesmo tempo.",
                },
                {
                    "texto": "Porque dispositivos IoT costumam usar apenas a rede 2.4GHz, e concentrar tudo numa frequência só congestiona o canal utilizado",
                    "correta": False,
                    "feedback": "Eles usam mesmo o 2.4GHz, e isso contribui. Mas a instabilidade aparece igual quando o tráfego é baixo — o que satura primeiro é a tabela de conexões do roteador, não o canal de rádio.",
                },
            ]},
            {"cena": "Você sugere separar os dispositivos IoT numa rede própria (separada da rede principal da família).",
             "pergunta": "Qual é o principal benefício dessa separação?",
             "opcoes": [
                {
                    "texto": "Isola o tráfego dos dispositivos IoT, reduzindo a chance deles sobrecarregarem ou afetarem a rede usada pelos celulares/notebooks da família",
                    "correta": True,
                    "feedback": "Correto — essa segmentação é uma prática recomendada justamente pra esse tipo de cenário com muitos dispositivos IoT.",
                },
                {
                    "texto": "Aumenta a segurança da casa, já que dispositivos IoT costumam ter falhas conhecidas e ficariam isolados dos computadores da família",
                    "correta": False,
                    "feedback": "É uma vantagem real da separação e vale citar. Só que o problema que trouxe você aqui é instabilidade: o benefício principal, neste caso, é aliviar a rede que a família usa.",
                },
                {
                    "texto": "Permite dar prioridade de banda pros aparelhos da família, garantindo que os dispositivos IoT nunca atrapalhem uma videochamada",
                    "correta": False,
                    "feedback": "Priorização é outro recurso, e nem toda separação de rede faz isso sozinha. O ganho direto da segmentação é tirar a disputa de conexões, não reservar velocidade.",
                },
            ]},
            {"cena": "Você cria uma segunda rede Wi-Fi (SSID separado) no mesmo roteador, dedicada aos dispositivos IoT.",
             "pergunta": "O que é importante orientar o cliente sobre essa segunda rede?",
             "opcoes": [
                {
                    "texto": "Que os dispositivos IoT precisam ser reconfigurados manualmente pra se conectar na rede nova — ele vai precisar entrar no app de cada um",
                    "correta": True,
                    "feedback": "Orientação importante e realista — trocar de rede não é automático pros dispositivos já conectados; o cliente precisa saber disso pra não ficar frustrado depois.",
                },
                {
                    "texto": "Que a rede nova herda a senha da principal, então os dispositivos vão reconectar sozinhos assim que ela for criada no roteador",
                    "correta": False,
                    "feedback": "Rede nova é rede nova: nome e senha próprios, e nenhum aparelho migra sozinho. Prometer o contrário faz o cliente achar que deu errado quando nada acontecer.",
                },
                {
                    "texto": "Que ele deve migrar tudo de uma vez no mesmo dia, senão o roteador vai manter as duas redes disputando e o problema continua igual",
                    "correta": False,
                    "feedback": "Migração parcial já alivia, e é justamente o que dá pra fazer no ritmo dele. Exigir tudo de uma vez transforma uma melhoria simples numa tarefa que ele vai adiar.",
                },
            ]},
            {"cena": "Depois de reconfigurar alguns dispositivos como teste, o Wi-Fi principal da família já melhora visivelmente.",
             "pergunta": "O que você recomenda pro cliente terminar de resolver sozinho?",
             "opcoes": [
                {
                    "texto": "Migrar aos poucos o restante dos dispositivos IoT pra rede nova, no ritmo dele, sem pressa",
                    "correta": True,
                    "feedback": "Boa orientação prática — não precisa ser feito tudo de uma vez, e o cliente já viu o resultado positivo com os primeiros dispositivos migrados.",
                },
                {
                    "texto": "Migrar o restante e, depois de tudo na rede nova, desativar a rede principal antiga pra não deixar duas redes ativas na casa",
                    "correta": False,
                    "feedback": "A rede principal é a da família — é ela que fica. Quem muda de rede são os dispositivos IoT; desativar a principal deixaria a casa inteira sem Wi-Fi.",
                },
                {
                    "texto": "Migrar o restante e reiniciar o roteador ao final, pra que ele reorganize a tabela de conexões e o ganho seja completo",
                    "correta": False,
                    "feedback": "O reinício limpa a tabela na hora, mas ela se reconstrói sozinha conforme os aparelhos saem da rede antiga. É passo dispensável — e mais uma coisa pro cliente lembrar de fazer.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54855",
        "bairro": "Bairro Areal",
        "titulo": "Suporte — Rede de Visitantes",
        "cliente": "Sr. Osmar",
        "equipamento": "Roteador doméstico",
        "briefing": "Cliente recebe muitas visitas e não gosta de passar a senha da rede principal toda vez. Quer uma rede separada só pra convidados.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "50338",
            "horario": "09h30",
            "assunto": "Realizar serviços - configurações",
            "endereco": "AVENIDA CASTELO BRANCO, 189",
            "cidade": "Pimenta Bueno",
            "referencia": "Perto do campo de futebol",
            "caixa_atendimento": "PBW 02",
            "porta_ftth": "5",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Juliana\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99811-8269\n"
                "Ocorrência: Cliente solicita configuração de uma rede Wi-Fi separada para visitantes, sem uso da senha da rede principal."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O Sr. Osmar pergunta se dá pra criar essa 'rede de visitas' sem comprar nenhum equipamento novo.",
             "pergunta": "Qual é a resposta tecnicamente correta?",
             "opcoes": [
                {
                    "texto": "Sim — a maioria dos roteadores modernos já tem essa função de rede de convidados (guest network) integrada, só precisa ativar nas configurações",
                    "correta": True,
                    "feedback": "Correto — não é necessário equipamento adicional na maioria dos casos, é uma função nativa comum em roteadores atuais.",
                },
                {
                    "texto": "Sim, e a forma de fazer é criar uma segunda rede com a mesma senha da principal, só mudando o nome pra identificar as visitas",
                    "correta": False,
                    "feedback": "Mesma senha significa mesma porta de entrada: quem entra pela rede de visitas enxerga tudo o que a rede da casa enxerga. O ponto da rede de convidados é justamente ser separada.",
                },
                {
                    "texto": "Sim, dá pra usar a função de convidados que já vem no roteador, mas ela costuma exigir que o equipamento seja reiniciado toda vez que a senha muda",
                    "correta": False,
                    "feedback": "Não exige. Ativar e mudar senha da rede de convidados é imediato na maioria dos modelos — dizer o contrário faz o cliente evitar usar um recurso que é justamente pra trocar sempre.",
                },
            ]},
            {"cena": "Você ativa a rede de convidados com uma senha própria, diferente da rede principal da casa.",
             "pergunta": "Qual configuração de segurança é importante ativar nessa rede de visitantes?",
             "opcoes": [
                {
                    "texto": "Isolamento de rede (impedir que dispositivos na rede de convidados acessem outros aparelhos da casa, como computadores e impressoras)",
                    "correta": True,
                    "feedback": "Isso — isolamento é uma prática essencial de segurança: visitantes acessam a internet, mas não os dispositivos privados da casa.",
                },
                {
                    "texto": "Definir um prazo de validade pra senha da rede de convidados, pra que ela expire sozinha depois que a visita for embora",
                    "correta": False,
                    "feedback": "É um recurso ótimo quando existe, e vale ativar junto. Mas ele controla por quanto tempo entram; o que protege a casa é impedir que quem entrou enxergue a TV, a impressora e os computadores.",
                },
                {
                    "texto": "Limitar a velocidade da rede de convidados, pra que uma visita baixando arquivo pesado não prejudique o restante da casa",
                    "correta": False,
                    "feedback": "Boa configuração, e o Sr. Osmar vai pedir isso adiante. Só que é conforto, não segurança: sem isolamento, o visitante continua com acesso aos aparelhos da rede interna.",
                },
            ]},
            {"cena": "O Sr. Osmar pergunta se a rede de convidados vai 'roubar' velocidade da rede principal quando muitas visitas estiverem conectadas.",
             "pergunta": "Como você explica?",
             "opcoes": [
                {
                    "texto": "Explica que sim, elas compartilham a mesma internet do plano contratado — mas se quiser, dá pra limitar a velocidade máxima da rede de convidados nas configurações",
                    "correta": True,
                    "feedback": "Resposta honesta e completa — explica a realidade (é o mesmo link de internet) e já oferece uma solução prática (limitar banda) se isso virar um problema real.",
                },
                {
                    "texto": "Explica que não — a rede de convidados tem banda reservada pelo roteador e por isso não interfere na velocidade da rede principal",
                    "correta": False,
                    "feedback": "Não existe banda reservada: as duas redes saem da mesma conexão contratada. Prometer que não interfere é garantir algo que o cliente vai desmentir na primeira visita que baixar um jogo.",
                },
                {
                    "texto": "Explica que sim, mas que dá pra evitar isso deixando a rede de convidados só no 2.4GHz, separando as visitas da família por frequência",
                    "correta": False,
                    "feedback": "Separar por frequência divide o rádio, não a internet: o download da visita continua saindo do mesmo plano. O que resolve é limitar a velocidade da rede de convidados.",
                },
            ]},
            {"cena": "Configuração concluída, com isolamento ativado e um limite de velocidade razoável pra rede de convidados.",
             "pergunta": "O que você anota na O.S. antes de encerrar?",
             "opcoes": [
                {
                    "texto": "O nome e a senha da rede de convidados configurada, e as opções de segurança ativadas — útil caso o cliente esqueça e precise de suporte depois",
                    "correta": True,
                    "feedback": "Bom registro — documentar o que foi configurado ajuda tanto o cliente quanto um próximo atendimento, caso seja necessário.",
                },
                {
                    "texto": "O nome da rede de convidados e a confirmação de que o isolamento foi ativado, sem registrar a senha, que é informação do cliente",
                    "correta": False,
                    "feedback": "A senha de convidados existe justamente pra ser passada adiante e trocada quando quiser — não é segredo do mesmo nível da rede principal. Sem ela no registro, um próximo atendimento começa do zero.",
                },
                {
                    "texto": "O nome e a senha da rede, o limite de velocidade aplicado e também a senha da rede principal da casa, pra ter tudo num lugar só",
                    "correta": False,
                    "feedback": "Registrar a senha da rede principal é justamente o que não se faz: ela dá acesso a todos os aparelhos da família. O registro cobre o que foi configurado no serviço, não o resto da casa.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54910",
        "bairro": "Centro (Ji-Paraná)",
        "titulo": "Instalação — Patch Panel em Escritório",
        "cliente": "Clínica Odontológica Sorriso",
        "equipamento": "Patch panel, switch, cabos Cat6, etiquetas",
        "briefing": "Clínica com 5 pontos de rede (recepção e 4 consultórios) que precisam ser organizados num rack pequeno.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "55775",
            "horario": "14h30",
            "assunto": "Serviços - Cabeamento",
            "endereco": "RUA SETE DE SETEMBRO, 295",
            "cidade": "Alta Floresta",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "AFT 02",
            "porta_ftth": "3",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Serviços - Cabeamento\n"
                "Descrição O.S. anterior: - Solicitante: atendente Aline\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99717-8195\n"
                "Ocorrência: Cliente (clínica) solicita organização do cabeamento de rede — 5 pontos (recepção e 4 consultórios) em rack pequeno."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção de cabo drop",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você termina de crimpar os 5 cabos no patch panel, todos funcionando conforme testado no testador de cabo.",
             "pergunta": "Antes de fechar o rack, o que é essencial fazer nos pontos do patch panel?",
             "opcoes": [
                {
                    "texto": "Etiquetar cada porta do patch panel indicando o cômodo/ponto que ela atende (ex: 'Consultório 1')",
                    "correta": True,
                    "feedback": "Isso é fundamental — sem etiquetas, qualquer manutenção futura vira um jogo de adivinhação sobre qual porta é qual, mesmo pra um técnico experiente.",
                },
                {
                    "texto": "Anotar a numeração das portas do patch panel no relatório da O.S., que fica registrado no sistema e não se perde nem se apaga com o tempo",
                    "correta": False,
                    "feedback": "O relatório ajuda, mas quem abre o rack daqui a dois anos é outro técnico, com pressa, sem o histórico na mão. A etiqueta está onde a informação é necessária: na própria porta.",
                },
                {
                    "texto": "Testar cada porta uma última vez e prender os cabos com abraçadeira, deixando o rack fechado e organizado pro cliente",
                    "correta": False,
                    "feedback": "Teste e organização você já fez, e são importantes. Mas sem identificação, na próxima manutenção alguém vai puxar cabo pra descobrir qual é qual — e derrubar um consultório que estava funcionando.",
                },
            ]},
            {"cena": "A recepcionista da clínica pergunta por que você está organizando os cabos com tanto cuidado dentro do rack, já que 'funciona do mesmo jeito'.",
             "pergunta": "Como você explica a importância da organização?",
             "opcoes": [
                {
                    "texto": "Explica que cabos organizados facilitam identificar problemas rapidamente e evitam danificar outros cabos numa manutenção futura",
                    "correta": True,
                    "feedback": "Boa explicação prática — organização não é só estética, ela reduz tempo de diagnóstico e risco de erro em manutenções futuras.",
                },
                {
                    "texto": "Explica que a organização evita que os cabos aqueçam demais dentro do rack, o que com o tempo degrada o desempenho da rede da clínica",
                    "correta": False,
                    "feedback": "Cabo de rede não esquenta a ponto de virar problema. O ganho é outro e bem concreto: achar o cabo certo na hora do defeito, sem mexer nos que estão funcionando.",
                },
                {
                    "texto": "Explica que a organização é exigência da norma de cabeamento estruturado e que sem ela a instalação não pode ser liberada pelo técnico",
                    "correta": False,
                    "feedback": "Existe norma sobre isso, mas transformar a explicação em regra burocrática perde a chance de mostrar o benefício real pra ela: manutenção mais rápida e menos risco de derrubar outro ponto.",
                },
            ]},
            {"cena": "Você percebe que o switch tem só 8 portas, e a clínica já usa 5 mais a porta de uplink da internet — sobrando pouca margem.",
             "pergunta": "O que você orienta pra clínica pensando no crescimento futuro?",
             "opcoes": [
                {
                    "texto": "Avisa que restam poucas portas livres, e que se a clínica pensar em expandir (mais um consultório, uma câmera), pode valer considerar um switch maior desde já",
                    "correta": True,
                    "feedback": "Orientação proativa e útil — antecipar essa limitação evita uma nova visita técnica e uma parada de atendimento quando a clínica crescer.",
                },
                {
                    "texto": "Sugere já instalar um segundo switch ligado em cascata no primeiro, deixando a clínica preparada pra qualquer expansão futura sem precisar trocar o equipamento atual depois",
                    "correta": False,
                    "feedback": "Cascatear resolve, mas você estaria instalando equipamento que ninguém pediu e que hoje ficaria ocioso. O papel aqui é informar a limitação; a decisão de investir é da clínica.",
                },
                {
                    "texto": "Não comenta agora e registra a observação na O.S., pra que a central avalie internamente se vale propor um upgrade pra esse cliente",
                    "correta": False,
                    "feedback": "Registrar é bom e você vai fazer. Mas quem decide sobre a rede da clínica é a clínica: passar a informação direto a quem vai expandir evita que ela descubra o limite no meio de uma obra.",
                },
            ]},
            {"cena": "Antes de encerrar, você testa a internet em cada um dos 5 pontos, incluindo os 4 consultórios.",
             "pergunta": "Por que testar em CADA ponto individualmente, e não só no primeiro que funcionar?",
             "opcoes": [
                {
                    "texto": "Porque um problema pode ser específico de um único cabo ou porta (ex: crimpagem malfeita), então cada ponto precisa ser confirmado individualmente antes de encerrar",
                    "correta": True,
                    "feedback": "Exatamente — testar só um ponto e assumir que os outros estão bons é um erro comum que gera retorno desnecessário depois.",
                },
                {
                    "texto": "Porque o switch pode ter portas com defeito, e testar todos os pontos é a forma de identificar qual porta do equipamento precisa ser substituída",
                    "correta": False,
                    "feedback": "Porta de switch com defeito é possível, mas raro. O que falha com muito mais frequência num serviço de cabeamento é a crimpagem de uma ponta específica — e ela só aparece testando aquele ponto.",
                },
                {
                    "texto": "Porque a norma de cabeamento estruturado exige certificação individual de cada ponto instalado antes da entrega formal do serviço, com laudo assinado pelo responsável técnico",
                    "correta": False,
                    "feedback": "Certificação com equipamento próprio é outro nível de serviço, que não é o desta O.S. O motivo aqui é mais simples e mais prático: cada cabo é um trabalho manual diferente, e cada um pode ter falhado.",
                },
            ]},
        ],
    },
    {
        "id": "OS-54962",
        "bairro": "Centro (Cacoal)",
        "titulo": "Suporte — Cliente Confunde Hub e Switch",
        "cliente": "Sr. Vanderlei",
        "equipamento": "Switch de 8 portas",
        "briefing": "Cliente comprou um 'hub' usado numa loja de eletrônicos pra dividir a internet entre vários computadores, mas está achando tudo lento.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "56719",
            "horario": "15h00",
            "assunto": "Internet Lenta",
            "endereco": "RUA SETE DE SETEMBRO, 106",
            "cidade": "Cujubim",
            "referencia": "Perto da praça central",
            "caixa_atendimento": "CUJU 02",
            "porta_ftth": "3",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Fernanda\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99746-2932\n"
                "Ocorrência: Cliente relata lentidão na rede após instalar, por conta própria, um equipamento comprado em loja de eletrônicos para dividir a internet entre computadores."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você examina o equipamento que ele comprou: é de fato um hub antigo, não um switch — um equipamento bem mais simples e ultrapassado.",
             "pergunta": "Qual é a diferença prática mais importante entre hub e switch, que explica a lentidão?",
             "opcoes": [
                {
                    "texto": "O hub retransmite os dados pra todas as portas ao mesmo tempo (gerando mais colisões de tráfego), enquanto o switch envia os dados só pra porta certa de destino, sendo bem mais eficiente",
                    "correta": True,
                    "feedback": "Exato — essa diferença de funcionamento é justamente o que explica a lentidão: hub é uma tecnologia antiga e ineficiente comparado a um switch.",
                },
                {
                    "texto": "O hub trabalha em velocidade fixa de 10 Mbps, enquanto o switch negocia automaticamente a maior velocidade suportada por cada equipamento conectado, chegando a 100 ou 1000 Mbps conforme a placa de rede",
                    "correta": False,
                    "feedback": "Existem hubs de 100 Mbps, então não é a velocidade nominal que separa os dois. A diferença que causa a lentidão é o hub repetir tudo pra todas as portas, fazendo os computadores colidirem entre si.",
                },
                {
                    "texto": "O hub precisa de configuração manual pra cada porta, e sem essa configuração ele entrega apenas uma fração da banda disponível pra cada computador",
                    "correta": False,
                    "feedback": "Hub não tem configuração nenhuma, é totalmente passivo — e é justamente por isso que ele não sabe separar o tráfego. A lentidão vem da colisão, não de uma configuração faltando.",
                },
            ]},
            {"cena": "Você explica a diferença pro Sr. Vanderlei e sugere trocar o hub por um switch.",
             "pergunta": "Ele pergunta se um switch 'atrapalha' a internet de alguma forma, já que ele nunca ouviu falar desse equipamento antes.",
             "opcoes": [
                {
                    "texto": "Explica que o switch só melhora a distribuição da rede entre os computadores, sem nenhuma desvantagem em relação ao hub antigo",
                    "correta": True,
                    "feedback": "Resposta correta e tranquilizadora — não há nenhum motivo pra evitar o switch, é estritamente uma melhoria em relação ao hub.",
                },
                {
                    "texto": "Explica que o switch é mais moderno, mas que ele vai precisar deixar os computadores ligados em portas fixas pra a rede funcionar corretamente",
                    "correta": False,
                    "feedback": "Switch não exige porta fixa pra nada: ele aprende sozinho qual equipamento está em cada porta. Criar essa regra imaginária deixa o cliente com medo de mexer na própria rede.",
                },
                {
                    "texto": "Explica que o switch melhora a rede interna, mas que a internet contratada continua a mesma — então parte da lentidão que ele sente pode não desaparecer",
                    "correta": False,
                    "feedback": "A ressalva é honesta e vale dizer. Só que neste caso a lentidão era da colisão do hub mesmo: começar prevenindo que talvez não resolva enfraquece uma solução que vai resolver.",
                },
            ]},
            {"cena": "Com o switch novo instalado no lugar do hub, você testa a velocidade em dois computadores ao mesmo tempo.",
             "pergunta": "O que você espera observar em comparação com a situação anterior?",
             "opcoes": [
                {
                    "texto": "Velocidade bem mais estável e consistente nos dois computadores simultaneamente, sem a lentidão de antes",
                    "correta": True,
                    "feedback": "Isso é exatamente o resultado esperado — o switch elimina o gargalo de eficiência que o hub antigo causava.",
                },
                {
                    "texto": "Um aumento da velocidade contratada nos dois computadores, já que agora a banda não precisa mais ser dividida entre as portas do equipamento",
                    "correta": False,
                    "feedback": "A velocidade contratada não muda com equipamento interno. O que melhora é o aproveitamento dela: sem colisão, os dois computadores usam bem a banda que sempre esteve disponível.",
                },
                {
                    "texto": "Melhora só no computador que estiver na primeira porta do switch, já que ela costuma ter prioridade sobre as demais no encaminhamento",
                    "correta": False,
                    "feedback": "Porta de switch não tem hierarquia: a primeira não vale mais que a última. O ganho aparece nos dois ao mesmo tempo, que é justamente o que o hub não conseguia entregar.",
                },
            ]},
            {"cena": "Serviço concluído. O Sr. Vanderlei pergunta se deveria jogar o hub antigo fora.",
             "pergunta": "O que você orienta?",
             "opcoes": [
                {
                    "texto": "Sugere que ele pode descartar o equipamento eletrônico de forma correta (ponto de coleta de eletrônicos), já que não tem mais utilidade prática pra rede dele",
                    "correta": True,
                    "feedback": "Boa orientação, incluindo a preocupação com descarte correto de lixo eletrônico, que é uma prática ambientalmente responsável.",
                },
                {
                    "texto": "Sugere guardar o hub como reserva, pra usar caso o switch novo apresente algum problema e a rede precise voltar a funcionar rapidamente",
                    "correta": False,
                    "feedback": "Parece prudente e é uma armadilha: no dia do problema alguém liga o hub, a lentidão volta e ninguém relaciona com a troca. Reserva ruim atrapalha mais do que a falta dela.",
                },
                {
                    "texto": "Sugere que ele devolva o hub na loja onde comprou, já que o equipamento não atende ao uso pretendido e provavelmente ainda está dentro do prazo de troca por outro produto",
                    "correta": False,
                    "feedback": "Pode até valer tentar, mas o hub não tem defeito — ele faz exatamente o que promete. Orientar devolução por inadequação de uso costuma render uma discussão sem ganho pro cliente.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55018",
        "bairro": "Setor 02 (Ariquemes)",
        "titulo": "Instalação — Câmera de Segurança via POE",
        "cliente": "Mercearia Bom Preço",
        "equipamento": "Câmera IP, injetor POE, cabo Cat6",
        "briefing": "O dono do mercado quer instalar uma câmera de segurança na entrada, ligada por rede em vez de precisar de uma tomada de energia extra ali.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "55497",
            "horario": "15h30",
            "assunto": "Serviços - Cabeamento",
            "endereco": "AVENIDA CASTELO BRANCO, 56",
            "cidade": "Alto Alegre",
            "referencia": "Portão de madeira, casa de esquina",
            "caixa_atendimento": "AAPC 02",
            "porta_ftth": "7",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Serviços - Cabeamento\n"
                "Descrição O.S. anterior: - Solicitante: atendente Fernanda\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99439-5713\n"
                "Ocorrência: Cliente (mercado) solicita instalação de câmera de segurança na entrada, com alimentação via rede (POE)."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção de cabo drop",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O cliente pergunta como a câmera vai funcionar sem um cabo de energia próprio na entrada, já que lá não tem tomada.",
             "pergunta": "Como você explica a tecnologia que resolve isso?",
             "opcoes": [
                {
                    "texto": "Explica que vai usar PoE (Power over Ethernet) — o mesmo cabo de rede também leva energia elétrica suficiente pra câmera funcionar, sem precisar de tomada no local",
                    "correta": True,
                    "feedback": "Boa explicação — PoE é exatamente a solução técnica pra esse tipo de situação, evitando obra elétrica extra.",
                },
                {
                    "texto": "Explica que a câmera funciona com a energia que o próprio cabo de rede transporta, e que por causa dessa alimentação ela precisa ficar a no máximo 15 metros de distância do rack",
                    "correta": False,
                    "feedback": "A parte da energia pelo cabo está certa; o limite é que não. PoE segue o mesmo alcance do Ethernet, até 100 metros — inventar um limite curto reduz onde a câmera pode ser instalada sem motivo.",
                },
                {
                    "texto": "Explica que vai instalar uma tomada nova perto da entrada, já que câmera com boa qualidade de imagem precisa de alimentação elétrica própria",
                    "correta": False,
                    "feedback": "Puxar rede elétrica até a entrada é obra, custo e risco que o PoE dispensa. Câmeras nesse porte trabalham bem com a energia que vem pelo cabo de rede.",
                },
            ]},
            {"cena": "Você instala o injetor PoE perto do rack e passa o cabo Cat6 até a posição da câmera na entrada.",
             "pergunta": "Qual cuidado é importante nesse tipo de instalação externa (câmera do lado de fora)?",
             "opcoes": [
                {
                    "texto": "Usar conectores e proteção adequados pra ambiente externo (exposição a chuva/sol), e verificar se o cabo já tem capa própria pra uso externo",
                    "correta": True,
                    "feedback": "Correto — cabo e conectores comuns de uso interno se degradam rápido em ambiente externo; vale usar material apropriado desde o início.",
                },
                {
                    "texto": "Deixar uma volta de folga no cabo logo abaixo da câmera, pra que a água escorra por ali e não entre no conector pela ação da gravidade",
                    "correta": False,
                    "feedback": "Essa alça de gotejamento é boa prática de verdade e vale fazer. Só que sozinha ela não basta: sem conector e cabo próprios pra ambiente externo, o sol e a chuva degradam a capa em poucos meses.",
                },
                {
                    "texto": "Aterrar o suporte metálico da câmera junto ao aterramento do rack, protegendo o equipamento contra descarga elétrica atmosférica, que é frequente na região nessa época",
                    "correta": False,
                    "feedback": "Aterramento importa em instalação externa e vale considerar. Mas o que mais derruba câmera externa não é raio: é umidade entrando por conector comum usado do lado de fora.",
                },
            ]},
            {"cena": "Câmera instalada e ligada. Você confere a imagem no aplicativo de monitoramento do celular do cliente.",
             "pergunta": "A imagem aparece cortando/travando de vez em quando. O que você verifica primeiro?",
             "opcoes": [
                {
                    "texto": "A qualidade da conexão de internet disponível pro streaming da câmera, e se o cabo/conectores estão bem crimpados e firmes",
                    "correta": True,
                    "feedback": "Boa abordagem — imagem cortando geralmente aponta pra instabilidade na conexão de rede/internet, então checar a qualidade do cabeamento e do link é o caminho certo.",
                },
                {
                    "texto": "A capacidade do injetor PoE, já que uma alimentação insuficiente faz a câmera reiniciar sozinha e a imagem travar de forma intermitente",
                    "correta": False,
                    "feedback": "PoE subdimensionado dá esse sintoma mesmo, e é uma boa hipótese. Mas antes disso vale conferir o caminho do dado: crimpagem e conexão explicam travamento com muito mais frequência.",
                },
                {
                    "texto": "A configuração de resolução e taxa de quadros da câmera no aplicativo, reduzindo a qualidade até a imagem parar de travar no monitoramento",
                    "correta": False,
                    "feedback": "Baixar a qualidade esconde o sintoma e entrega ao cliente uma câmera pior do que ele comprou. Primeiro se descobre por que trava; ajustar resolução vem depois, se for mesmo o caso.",
                },
            ]},
            {"cena": "Você identifica que o conector RJ45 na ponta da câmera estava mal crimpado, causando perda intermitente de conexão. Depois de recrimpar, a imagem fica estável.",
             "pergunta": "O que registrar nessa O.S.?",
             "opcoes": [
                {
                    "texto": "Que a instalação foi feita com PoE, e que a causa da instabilidade inicial foi um conector mal crimpado, já corrigido e testado",
                    "correta": True,
                    "feedback": "Registro completo e útil — detalha a solução aplicada (PoE) e documenta a causa e correção de um problema encontrado durante o próprio atendimento.",
                },
                {
                    "texto": "Que a instalação foi feita com PoE e que a câmera apresentou travamento de imagem, resolvido com ajuste no ponto de conexão do equipamento",
                    "correta": False,
                    "feedback": "'Ajuste no ponto de conexão' não diz nada a quem ler depois. Registrar que era conector mal crimpado é o que permite reconhecer o padrão se acontecer de novo em outra instalação sua.",
                },
                {
                    "texto": "Que a instalação foi feita com PoE, a distância do cabo até a câmera e o modelo do injetor utilizado, com a data e o horário da conclusão",
                    "correta": False,
                    "feedback": "São dados úteis e vale ter. Mas falta a informação mais valiosa do atendimento: houve uma falha, ela foi diagnosticada e corrigida — sem isso, o registro conta só metade da história.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55074",
        "bairro": "Centro (Rolim de Moura)",
        "titulo": "Suporte — Rede Lenta por Loop Acidental",
        "cliente": "Escola de Idiomas Falla Bene",
        "equipamento": "Switch, cabos de rede",
        "briefing": "A rede da escola ficou extremamente lenta do nada, quase parada. Ninguém mexeu em nada, segundo a equipe.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "58141",
            "horario": "14h30",
            "assunto": "Internet Lenta",
            "endereco": "TRAVESSA DAS PALMEIRAS, 927",
            "cidade": "Cacoal",
            "referencia": "Portão de madeira, casa de esquina",
            "caixa_atendimento": "CWL 03",
            "porta_ftth": "6",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Bruna\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99546-3267\n"
                "Ocorrência: Cliente (escola) relata rede extremamente lenta, sem alteração recente identificada pela equipe local."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você percebe que as luzes do switch estão piscando freneticamente em várias portas ao mesmo tempo, sem nenhum tráfego de uso normal acontecendo.",
             "pergunta": "O que esse comportamento sugere?",
             "opcoes": [
                {
                    "texto": "Um possível loop de rede — alguém pode ter conectado um cabo criando um caminho circular entre duas portas do mesmo switch (ou switches diferentes), gerando uma tempestade de tráfego (broadcast storm)",
                    "correta": True,
                    "feedback": "Exatamente esse tipo de sintoma (luzes piscando muito, rede toda lenta) é clássico de loop de rede — um erro comum quando alguém conecta as duas pontas de um cabo em portas diferentes do mesmo switch sem perceber.",
                },
                {
                    "texto": "Que algum equipamento da escola está com defeito e inundando a rede de tráfego, provavelmente uma placa de rede queimada em algum computador do laboratório de informática, que fica ligado o dia inteiro",
                    "correta": False,
                    "feedback": "Placa defeituosa pode gerar tráfego estranho, e é uma hipótese razoável. Mas o padrão de várias portas piscando juntas, no mesmo ritmo, é a assinatura clássica de um caminho circular na rede.",
                },
                {
                    "texto": "Que a rede está com muitos dispositivos conectados ao mesmo tempo, e o switch não dá conta de encaminhar todo esse volume simultâneo",
                    "correta": False,
                    "feedback": "Switch saturado fica lento, não frenético: as luzes acompanhariam o uso real, com variação. Piscar todas juntas sem parar indica o mesmo pacote circulando sem fim.",
                },
            ]},
            {"cena": "Você percorre as salas e encontra um cabo de rede com as duas pontas conectadas em tomadas de rede diferentes da mesma sala — provavelmente alguém tentando 'estender' um ponto sem saber que criava um loop.",
             "pergunta": "O que fazer imediatamente?",
             "opcoes": [
                {
                    "texto": "Desconectar uma das pontas desse cabo imediatamente pra interromper o loop",
                    "correta": True,
                    "feedback": "Correto — a prioridade é interromper o loop o quanto antes, já que ele está sobrecarregando a rede inteira da escola.",
                },
                {
                    "texto": "Etiquetar esse cabo, fotografar a ligação e comunicar a direção da escola antes de desconectar, pra que fique registrado quem fez a ligação errada",
                    "correta": False,
                    "feedback": "Documentar é útil e leva segundos, mas a rede da escola inteira está parada agora. Primeiro se interrompe o loop; a foto e o registro vêm logo em seguida, com a rede já funcionando.",
                },
                {
                    "texto": "Desconectar as duas pontas do cabo e removê-lo por completo, pra garantir que ninguém volte a ligá-lo por engano nas mesmas portas",
                    "correta": False,
                    "feedback": "Tirar o cabo de circulação faz sentido como prevenção, mas basta uma ponta pra o loop acabar. Remover tudo antes de conferir pode desligar um ponto que estava em uso legítimo na outra extremidade.",
                },
            ]},
            {"cena": "Com o cabo do loop desconectado, a rede volta ao normal quase instantaneamente — luzes do switch normalizadas, navegação rápida de novo.",
             "pergunta": "O que você explica pra equipe da escola sobre como evitar isso no futuro?",
             "opcoes": [
                {
                    "texto": "Orienta que nunca se deve conectar as duas pontas de um mesmo cabo em portas de rede diferentes, e que qualquer necessidade de mais pontos deve passar por um técnico",
                    "correta": True,
                    "feedback": "Orientação clara e prática — evita que o mesmo erro se repita, e direciona necessidades futuras de expansão pro caminho certo (técnico especializado).",
                },
                {
                    "texto": "Orienta a escola a manter o rack trancado, já que o problema só acontece quando alguém sem conhecimento técnico mexe nas portas do switch",
                    "correta": False,
                    "feedback": "Trancar ajuda, mas o loop nasceu de um cabo ligado na sala, não dentro do rack. A orientação precisa alcançar quem mexe em tomada de rede pela escola, não só quem chega perto do equipamento.",
                },
                {
                    "texto": "Orienta que qualquer cabo sobrando seja enrolado e guardado no armário, e que a escola mantenha um inventário atualizado de todos os pontos de rede ativos em cada sala",
                    "correta": False,
                    "feedback": "Inventário é ótima prática e ajuda no longo prazo. Mas o que evita a repetição amanhã é a regra simples e concreta: as duas pontas de um mesmo cabo nunca vão em duas tomadas de rede.",
                },
            ]},
            {"cena": "Antes de sair, você percebe que alguns switches menores/baratos não têm proteção automática contra loop, enquanto modelos mais avançados detectam e bloqueiam automaticamente.",
             "pergunta": "Vale mencionar isso pra escola?",
             "opcoes": [
                {
                    "texto": "Sim — explicar que existe a opção de um switch com proteção contra loop pode evitar que esse tipo de parada aconteça de novo no futuro",
                    "correta": True,
                    "feedback": "Boa prática consultiva — informar sobre uma melhoria disponível ajuda o cliente a tomar uma decisão informada sobre prevenção futura.",
                },
                {
                    "texto": "Sim — e vale explicar que a proteção contra loop também evita que a rede caia quando um cabo é ligado errado, sem precisar de intervenção técnica",
                    "correta": False,
                    "feedback": "A explicação está correta, mas 'sem precisar de intervenção técnica' promete demais: a proteção bloqueia a porta e alguém ainda precisa descobrir e corrigir a ligação errada.",
                },
                {
                    "texto": "Sim, e o melhor caminho é registrar na O.S. como recomendação técnica formal, pra que a compra seja avaliada pela direção com o orçamento do ano",
                    "correta": False,
                    "feedback": "Registrar é bom, mas deixar só no papel faz a informação chegar tarde. Quem estava ali na parada de hoje é quem entende o valor da proteção — vale explicar na hora, e registrar também.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55130",
        "bairro": "Setor Industrial",
        "titulo": "Suporte — Cliente Exaltado por Atraso",
        "cliente": "Sr. Cristóvão",
        "equipamento": "Nenhum equipamento — atendimento é sobre comunicação",
        "briefing": "Você chega 40 minutos atrasado numa visita agendada por conta de um atendimento anterior que demorou mais que o previsto. O cliente está visivelmente irritado.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "50933",
            "horario": "09h00",
            "assunto": "Sem Internet",
            "endereco": "RUA BOA VISTA, 660",
            "cidade": "São Miguel",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "SMGE 03",
            "porta_ftth": "3",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Sem Internet\n"
                "Descrição O.S. anterior: - Solicitante: atendente Camila\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99806-9633\n"
                "Ocorrência: Cliente sem internet. Solicitou atendimento com urgência e aguarda visita técnica agendada."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Assim que você chega, o Sr. Cristóvão já começa reclamando alto, dizendo que perdeu a manhã de trabalho esperando.",
             "pergunta": "Qual é a primeira atitude correta?",
             "opcoes": [
                {
                    "texto": "Se desculpar de forma sincera pelo atraso, explicar objetivamente o motivo (sem exagerar desculpas), e perguntar se ainda é um bom momento pra ele",
                    "correta": True,
                    "feedback": "Boa conduta — reconhecer o erro com sinceridade, sem drama nem desculpas longas demais, e confirmar disponibilidade dele demonstra respeito pelo tempo do cliente.",
                },
                {
                    "texto": "Reconhecer o atraso brevemente e propor começar imediatamente pelo serviço, pra recuperar parte do tempo que ele perdeu esperando por você",
                    "correta": False,
                    "feedback": "A intenção é boa, mas atropela: ele acabou de dizer que perdeu a manhã. Perguntar se ainda é um bom momento devolve a ele o controle sobre o próprio dia, e isso desarma mais que pressa.",
                },
                {
                    "texto": "Explicar em detalhes tudo o que atrasou a agenda do dia, deixando claro que o atendimento anterior se estendeu por causa de um problema que ninguém tinha como prever",
                    "correta": False,
                    "feedback": "Uma explicação objetiva ajuda; alongar demais vira justificativa e soa como se você estivesse pedindo compreensão em vez de reconhecer o transtorno dele.",
                },
            ]},
            {"cena": "O Sr. Cristóvão aceita seguir com o atendimento, mas continua com um tom seco durante o serviço.",
             "pergunta": "Como você conduz o restante do atendimento?",
             "opcoes": [
                {
                    "texto": "Mantém profissionalismo, foca em resolver o problema técnico com eficiência, e comunica claramente o que está fazendo em cada etapa",
                    "correta": True,
                    "feedback": "Boa abordagem — demonstrar competência e transparência durante o serviço costuma reconstruir a confiança do cliente, mesmo depois de um começo ruim.",
                },
                {
                    "texto": "Puxa conversa sobre assuntos leves durante o serviço, pra quebrar o gelo e deixar o clima do atendimento mais confortável pros dois lados",
                    "correta": False,
                    "feedback": "Funciona com alguns clientes e irrita justamente o que está com pressa e ainda chateado. Com ele, o que reconstrói confiança é ver o serviço andando bem e entender o que está sendo feito.",
                },
                {
                    "texto": "Trabalha em silêncio pra não incomodar, e explica tudo de uma vez só no final, quando o problema já estiver resolvido e testado",
                    "correta": False,
                    "feedback": "Deixar tudo pro fim mantém ele no escuro durante o atendimento inteiro — e quem está incomodado interpreta silêncio como descaso. Narrar cada etapa custa pouco e mostra progresso.",
                },
            ]},
            {"cena": "Ao final, o serviço foi concluído com sucesso e o Sr. Cristóvão parece mais calmo.",
             "pergunta": "O que fazer antes de ir embora?",
             "opcoes": [
                {
                    "texto": "Confirmar que está tudo funcionando corretamente, perguntar se ele tem mais alguma dúvida, e se desculpar mais uma vez, brevemente, pelo atraso inicial",
                    "correta": True,
                    "feedback": "Bom fechamento — confirma a qualidade do serviço entregue e deixa uma última impressão positiva, mesmo depois de um começo difícil.",
                },
                {
                    "texto": "Confirmar que está tudo funcionando, explicar o que foi feito e deixar o contato do suporte caso ele precise de alguma coisa nos próximos dias",
                    "correta": False,
                    "feedback": "Está bem próximo do ideal e falta um detalhe que pesa neste atendimento: uma última desculpa breve pelo atraso. É o que fecha o assunto que abriu a visita.",
                },
                {
                    "texto": "Confirmar que está tudo funcionando e se desculpar novamente pelo atraso, explicando mais uma vez o motivo da agenda ter estourado pra ele entender que não houve descaso",
                    "correta": False,
                    "feedback": "A desculpa é bem-vinda; repetir o motivo não. Explicar de novo devolve o cliente ao incômodo e transfere pra ele o trabalho de te absolver — breve é mais eficaz que insistente.",
                },
            ]},
            {"cena": "De volta ao carro, você registra o atendimento no sistema.",
             "pergunta": "Vale mencionar o atraso e a reação do cliente no registro interno?",
             "opcoes": [
                {
                    "texto": "Sim, de forma objetiva — registrar que houve atraso (e o motivo) ajuda a central a entender o contexto caso o cliente entre em contato novamente sobre isso",
                    "correta": True,
                    "feedback": "Boa prática — um registro objetivo e factual ajuda toda a equipe a ter contexto completo, sem julgamento sobre o comportamento do cliente.",
                },
                {
                    "texto": "Sim, registrando o atraso e também que o cliente ficou insatisfeito, pra que a central saiba que ele pode reclamar formalmente depois",
                    "correta": False,
                    "feedback": "Registrar a insatisfação é legítimo, mas a forma importa: descreva o fato (atraso, motivo, cliente incomodado) sem rotular o cliente. O registro é contexto, não avaliação de quem chamou.",
                },
                {
                    "texto": "Sim, registrando o atraso e sugerindo à central que entre em contato com o cliente pra oferecer algum tipo de compensação pelo período de trabalho que ele acabou perdendo",
                    "correta": False,
                    "feedback": "Sugerir compensação cria uma expectativa que não é sua pra prometer, e nem toda situação comporta. Registre o ocorrido; a decisão sobre compensar é da área que trata disso.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55182",
        "bairro": "Bairro Liberdade",
        "titulo": "Suporte — Pedido pra Pular o Processo",
        "cliente": "Sr. Fabrício",
        "equipamento": "Nenhum — situação de atendimento",
        "briefing": "O cliente pede pra você fazer uma alteração no plano dele 'só verbalmente', sem passar pela central, porque ele 'confia em você'.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "51950",
            "horario": "15h00",
            "assunto": "Realizar serviços - configurações",
            "endereco": "RUA DOS PIONEIROS, 816",
            "cidade": "Conselvan",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "AYPO 03",
            "porta_ftth": "4",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Mayara\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99876-4282\n"
                "Ocorrência: Cliente solicita atendimento técnico para ajuste de configurações do plano contratado."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O Sr. Fabrício pede pra você mudar o plano dele agora mesmo, direto com você, sem precisar ligar pra central ou assinar nada.",
             "pergunta": "Qual é a resposta correta?",
             "opcoes": [
                {
                    "texto": "Explicar com educação que alterações de plano/contrato precisam passar pelo canal oficial da empresa, mesmo que pareça mais rápido fazer diretamente com você",
                    "correta": True,
                    "feedback": "Resposta correta — processos formais existem pra proteger tanto o cliente quanto a empresa (registro correto de cobrança, termos, etc.); pular isso gera risco pra ambos os lados.",
                },
                {
                    "texto": "Explicar que você pode até registrar a solicitação por aqui, mas que o novo valor só passa a valer depois que a central entrar em contato e confirmar a alteração diretamente com ele",
                    "correta": False,
                    "feedback": "Registrar o interesse é justamente o que se faz — e você vai fazer. O problema da resposta é sugerir que a alteração começou por aqui: ela começa e termina no canal oficial, não na visita.",
                },
                {
                    "texto": "Explicar que alterações de plano precisam do canal oficial e ligar você mesmo pra central agora, resolvendo o pedido dele durante a visita",
                    "correta": False,
                    "feedback": "A intenção é boa, mas o pedido de plano é do titular e passa por confirmação com ele. Ligar em nome dele mistura os papéis e pode travar o processo depois, por falta de validação.",
                },
            ]},
            {"cena": "O cliente insiste, dizendo que 'é só um detalhe pequeno' e que confia totalmente em você pra resolver.",
             "pergunta": "Como você conduz melhor essa insistência?",
             "opcoes": [
                {
                    "texto": "Reforça a explicação com empatia, e se oferece pra ajudar ele a fazer o contato certo com a central (ex: informando o número/canal) pra resolver rapidinho",
                    "correta": True,
                    "feedback": "Boa conduta — mantém o limite profissional necessário, mas ainda ajuda ativamente o cliente a resolver pelo canal certo, sem deixá-lo sem solução.",
                },
                {
                    "texto": "Explica de novo o motivo da regra, detalhando que existe registro e auditoria de qualquer alteração contratual feita fora do canal oficial",
                    "correta": False,
                    "feedback": "Repetir com mais peso soa como se você estivesse se defendendo de uma acusação. O que resolve a insistência não é reforçar a norma, é dar a ele um caminho prático pra conseguir o que quer.",
                },
                {
                    "texto": "Sugere que ele mesmo ligue pra central assim que você terminar o serviço e sair, e segue com o atendimento técnico sem se envolver mais no assunto da alteração de plano",
                    "correta": False,
                    "feedback": "Está correto e um pouco seco: 'ligue depois' devolve o problema sem ajudar. Informar o número, o horário e o que ele deve pedir transforma a recusa em encaminhamento.",
                },
            ]},
            {"cena": "O cliente entende a explicação e pergunta se você pode pelo menos anotar o pedido dele pra 'agilizar' quando ele ligar pra central.",
             "pergunta": "Isso é apropriado?",
             "opcoes": [
                {
                    "texto": "Sim — anotar o pedido dele (ex: no relatório da sua visita) pra que a central tenha esse contexto quando ele entrar em contato é uma forma legítima de ajudar",
                    "correta": True,
                    "feedback": "Isso é diferente de fazer a alteração você mesmo — é só documentar o interesse dele, mantendo o processo formal intacto.",
                },
                {
                    "texto": "Sim, e vale já explicar a ele quais planos costumam ter o valor que ele procura, pra que ele chegue à central sabendo exatamente o que pedir",
                    "correta": False,
                    "feedback": "Passar valores de plano não é atribuição do técnico e muda com promoção e região. Se você errar o número, a central vira a portadora de uma má notícia que você criou.",
                },
                {
                    "texto": "Sim, e é melhor anotar também o valor que ele disse pagar hoje e quanto ele gostaria de pagar, pra que a central já chegue nele com uma proposta pronta e feche na primeira ligação",
                    "correta": False,
                    "feedback": "Anotar o interesse basta. Registrar números que o cliente mencionou de passagem cria uma negociação que não começou, e a central acaba tendo que desdizer o que ficou no papel.",
                },
            ]},
            {"cena": "Você conclui o atendimento técnico original (não relacionado ao pedido de plano) e se despede do cliente.",
             "pergunta": "O que registrar na O.S. sobre esse pedido de alteração de plano?",
             "opcoes": [
                {
                    "texto": "Uma observação objetiva de que o cliente demonstrou interesse em alterar o plano, sugerindo que a central entre em contato",
                    "correta": True,
                    "feedback": "Bom registro — ajuda o time comercial/central a dar seguimento, sem você ter assumido uma responsabilidade que não é sua.",
                },
                {
                    "texto": "Que o cliente pediu alteração de plano durante a visita e que você explicou o procedimento correto, sem indicar necessidade de novo contato",
                    "correta": False,
                    "feedback": "Registrar a orientação é bom, mas parar aí faz a informação morrer: o interesse dele se perde. A observação vale justamente pra que alguém da central procure o cliente.",
                },
                {
                    "texto": "Que o cliente pediu alteração de plano, que a solicitação foi encaminhada pela sua visita e que ele aguarda retorno com o novo valor confirmado",
                    "correta": False,
                    "feedback": "Você não encaminhou solicitação nenhuma — o pedido ainda precisa partir dele pelo canal oficial. Registrar como encaminhado faz o cliente esperar por um retorno que ninguém vai fazer.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55240",
        "bairro": "Bairro Panorama",
        "titulo": "Suporte — Cliente Oferece Pagamento Extra",
        "cliente": "Sr. Osiel",
        "equipamento": "Nenhum — situação de atendimento",
        "briefing": "Durante o atendimento, o cliente oferece um dinheiro 'por fora' pra você priorizar a visita dele da próxima vez que precisar de suporte.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "55305",
            "horario": "08h30",
            "assunto": "Realizar serviços - configurações",
            "endereco": "AVENIDA BRASIL, 809",
            "cidade": "Aripuanã",
            "referencia": "Em frente ao posto de saúde",
            "caixa_atendimento": "AYP 03",
            "porta_ftth": "6",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Rafael\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99918-1998\n"
                "Ocorrência: Cliente solicita atendimento técnico para ajustes e configurações gerais da rede."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O Sr. Osiel te oferece uma quantia em dinheiro, dizendo que é 'só um agrado' pra você sempre priorizar ele nas próximas vezes.",
             "pergunta": "Qual é a atitude correta?",
             "opcoes": [
                {
                    "texto": "Recusar educadamente, explicando que o atendimento segue a ordem e critérios da empresa, e que isso não seria correto aceitar",
                    "correta": True,
                    "feedback": "Atitude correta e profissional — aceitar esse tipo de oferta compromete a integridade do processo de atendimento e pode ter consequências sérias pra você e pra empresa.",
                },
                {
                    "texto": "Recusar e explicar que, se ele quiser agilizar, o caminho é falar com a central e verificar se o chamado dele se enquadra em alguma prioridade",
                    "correta": False,
                    "feedback": "A recusa está certa e o encaminhamento parece prestativo, mas sugere que existe um jeito de furar fila mediante pedido. Prioridade se define por critério técnico, não por quem liga pedindo.",
                },
                {
                    "texto": "Recusar o dinheiro e aceitar apenas se for algo simbólico, como um café ou um lanche, que não configura vantagem financeira nenhuma",
                    "correta": False,
                    "feedback": "Café oferecido no meio do serviço é uma coisa; aceitar algo em troca de prioridade é outra, independente do valor. O que define aqui não é o quanto vale, é o que está sendo pedido em troca.",
                },
            ]},
            {"cena": "O cliente insiste, dizendo que 'todo mundo faz isso' e que não é nada demais.",
             "pergunta": "Como você reforça sua posição?",
             "opcoes": [
                {
                    "texto": "Reforça com tranquilidade que essa não é uma prática da empresa, e garante que o atendimento dele vai ser tratado com o mesmo cuidado de qualquer outro cliente, sem precisar de nenhum 'agrado'",
                    "correta": True,
                    "feedback": "Boa resposta — reforça o limite profissional sem constranger o cliente, e ainda garante a ele que não perde qualidade de atendimento por não pagar nada extra.",
                },
                {
                    "texto": "Explica que aceitar poderia custar seu emprego, e pede que ele entenda a sua situação e não insista mais com você sobre esse assunto",
                    "correta": False,
                    "feedback": "Colocar o próprio risco no centro faz parecer que o problema é a punição, não a prática. E transfere pro cliente a responsabilidade de te proteger, quando a recusa deveria ser simplesmente a regra.",
                },
                {
                    "texto": "Repete a recusa e muda de assunto, seguindo o serviço sem alongar a conversa, pra que o cliente entenda pelo silêncio que o assunto acabou",
                    "correta": False,
                    "feedback": "Encerrar sem constrangimento tem seu valor. Mas o cliente fica sem entender por que não, e sai com a impressão de que quem aceita consegue algo — vale dizer que o atendimento dele já é igual ao de todos.",
                },
            ]},
            {"cena": "O cliente entende e não insiste mais no assunto, seguindo normalmente com o atendimento técnico.",
             "pergunta": "Você deve reportar esse episódio internamente?",
             "opcoes": [
                {
                    "texto": "Sim — é uma boa prática registrar esse tipo de situação, mesmo tendo sido recusada corretamente, como transparência e proteção pra você mesmo",
                    "correta": True,
                    "feedback": "Correto — reportar situações assim, mesmo resolvidas bem, cria um histórico transparente que protege tanto você quanto a empresa.",
                },
                {
                    "texto": "Não é necessário: como a oferta foi recusada na hora, não houve irregularidade nenhuma, e registrar poderia constranger o cliente à toa",
                    "correta": False,
                    "feedback": "Justamente por não ter havido irregularidade é que registrar é fácil e seguro. O registro protege você: se um dia a história for contada de outro jeito, existe a sua versão feita no mesmo dia.",
                },
                {
                    "texto": "Sim, mas apenas de forma verbal com o supervisor, sem registrar por escrito, pra não deixar um documento que constranja o cliente depois",
                    "correta": False,
                    "feedback": "Conversa verbal some. Um registro objetivo do que aconteceu não acusa ninguém de nada — descreve um fato e a conduta correta que você teve, que é exatamente o que protege os dois lados.",
                },
            ]},
            {"cena": "Semanas depois, você atende o Sr. Osiel de novo em outro chamado, dentro da ordem normal de atendimento.",
             "pergunta": "Como deve ser esse próximo atendimento?",
             "opcoes": [
                {
                    "texto": "Exatamente com a mesma qualidade e atenção de qualquer outro cliente, sem nenhum tratamento diferenciado por causa do episódio anterior",
                    "correta": True,
                    "feedback": "Isso — o episódio anterior não deve influenciar em nada a qualidade do atendimento atual, pra melhor ou pra pior.",
                },
                {
                    "texto": "Com atenção redobrada e capricho extra, pra deixar claro pra ele que um bom atendimento nunca dependeu de nenhum tipo de agrado",
                    "correta": False,
                    "feedback": "A intenção é boa e o efeito é o contrário: capricho extra pra provar um ponto ainda é tratamento diferenciado, só que na outra direção. O que prova o ponto é o padrão normal, igual pra todos.",
                },
                {
                    "texto": "Normalmente, mas evitando qualquer conversa que possa lembrar o episódio anterior, mantendo o contato o mais estritamente técnico possível",
                    "correta": False,
                    "feedback": "Evitar o assunto faz sentido; ficar seco de propósito não. Você não tem nada a esconder do episódio, e um atendimento frio hoje é justamente o tratamento diferenciado que se quer evitar.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55296",
        "bairro": "Setor Industrial",
        "titulo": "Suporte — Cliente Idoso com Dificuldade Técnica",
        "cliente": "Dona Zulmira",
        "equipamento": "ONT com Wi-Fi, celular do cliente",
        "briefing": "Cliente de 78 anos precisa reconectar o celular no Wi-Fi depois de uma troca de senha, mas tem bastante dificuldade com tecnologia.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "54749",
            "horario": "14h30",
            "assunto": "Realizar serviços - configurações",
            "endereco": "RUA TIRADENTES, 778",
            "cidade": "Juína",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "JNA 03",
            "porta_ftth": "2",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Camila\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99494-2046\n"
                "Ocorrência: Cliente relata dificuldade para reconectar o celular ao Wi-Fi após alteração de senha. Solicita apoio técnico presencial."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você troca a senha do Wi-Fi (a pedido da própria cliente, por segurança) e agora precisa reconectar o celular dela na rede.",
             "pergunta": "Qual é a abordagem mais adequada pra esse cliente específico?",
             "opcoes": [
                {
                    "texto": "Fazer a reconexão passo a passo, explicando com calma e paciência cada etapa, sem pressa e sem usar termos técnicos desnecessários",
                    "correta": True,
                    "feedback": "Abordagem correta — clientes com menos familiaridade com tecnologia se beneficiam de explicações pausadas e linguagem simples, sem pressa.",
                },
                {
                    "texto": "Reconectar o celular dela e deixar anotado num papel o passo a passo detalhado, pra que ela possa repetir sozinha se precisar em outro aparelho",
                    "correta": False,
                    "feedback": "O papel ajuda depois, mas ela está aqui agora: fazer junto, no ritmo dela, ensina muito mais que um roteiro que ela vai tentar seguir sozinha e travar no primeiro passo diferente.",
                },
                {
                    "texto": "Reconectar todos os aparelhos da casa você mesmo, com calma, pra que ela não precise se preocupar com esse tipo de configuração no futuro",
                    "correta": False,
                    "feedback": "Resolver por ela hoje garante o dia e não o mês que vem, quando ela comprar um aparelho novo. O ganho maior é ela sair sabendo fazer, mesmo que devagar.",
                },
            ]},
            {"cena": "Dona Zulmira pede pra anotar a senha nova num papel, porque ela não confia em guardar só no celular.",
             "pergunta": "Como você atende esse pedido da melhor forma?",
             "opcoes": [
                {
                    "texto": "Anota a senha de forma clara e legível num papel, e sugere que ela guarde num lugar seguro em casa, como perto do roteador",
                    "correta": True,
                    "feedback": "Bom atendimento — respeita a preferência da cliente e ainda orienta uma forma prática e segura de guardar a informação.",
                },
                {
                    "texto": "Anota a senha e sugere colar o papel na parte de baixo do próprio roteador, que é onde ela sempre vai lembrar de procurar quando precisar",
                    "correta": False,
                    "feedback": "Prático e arriscado: qualquer visita que passe perto do roteador lê a senha. Melhor um lugar que ela lembre e que não fique exposto a quem entra na casa.",
                },
                {
                    "texto": "Anota a senha e também tira uma foto do papel com o celular dela, deixando salvo na galeria pra ela não perder se o papel sumir",
                    "correta": False,
                    "feedback": "A intenção é boa, mas foto de senha na galeria acaba em backup na nuvem e em qualquer aplicativo que peça acesso às fotos. Se ela prefere papel, o papel bem guardado já resolve.",
                },
            ]},
            {"cena": "Depois de reconectar o celular dela com sucesso, Dona Zulmira pergunta se pode te ligar diretamente da próxima vez que tiver dúvida.",
             "pergunta": "Como você responde da forma mais adequada?",
             "opcoes": [
                {
                    "texto": "Explica com gentileza que o canal oficial de suporte é o mais indicado, porque garante atendimento mesmo quando você não estiver disponível, e anota o número de suporte pra ela",
                    "correta": True,
                    "feedback": "Boa resposta — orienta pro canal certo sem parecer frio, e ainda ajuda deixando o contato de suporte anotado pra facilitar a vida dela.",
                },
                {
                    "texto": "Explica que prefere não passar o número pessoal, mas se oferece pra deixar o contato do seu supervisor, caso ela precise de ajuda depois",
                    "correta": False,
                    "feedback": "Recusar está certo, mas o supervisor não é canal de suporte — ele também vai encaminhar pra central. Dar o número do suporte resolve direto, sem etapa no meio.",
                },
                {
                    "texto": "Dá o número pessoal, mas explica que ela deve usá-lo só em emergência, e que o caminho normal continua sendo ligar pro suporte oficial",
                    "correta": False,
                    "feedback": "Na prática ela vai usar sempre, porque é o contato de alguém que ela confia. E no dia em que você estiver de folga ou tiver saído da empresa, ela fica sem atendimento nenhum.",
                },
            ]},
            {"cena": "Antes de sair, você confirma que o celular dela está de fato conectado e navegando normalmente.",
             "pergunta": "Isso é um passo dispensável, já que a reconexão pareceu funcionar?",
             "opcoes": [
                {
                    "texto": "Não é dispensável — confirmar navegação de verdade (abrindo um site ou app) evita que a cliente descubra sozinha, depois que você for embora, que algo não está funcionando",
                    "correta": True,
                    "feedback": "Correto — 'conectado ao Wi-Fi' nem sempre significa 'navegando normalmente'; testar de verdade evita frustração da cliente depois que você sair.",
                },
                {
                    "texto": "É dispensável neste caso: se o celular mostra que conectou na rede e a senha foi aceita, a navegação necessariamente está funcionando",
                    "correta": False,
                    "feedback": "Conectar e navegar são coisas diferentes: dá pra estar na rede e sem internet, por configuração ou pela própria conexão. Abrir um site leva cinco segundos e elimina a dúvida.",
                },
                {
                    "texto": "É dispensável se você já testou a navegação no seu próprio celular conectado na mesma rede, o que confirma que o Wi-Fi está entregando internet",
                    "correta": False,
                    "feedback": "Seu celular confirma que a rede está boa, não que o dela ficou certo. Como o objetivo do atendimento era o aparelho dela, é nele que o teste tem que ser feito.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55351",
        "bairro": "Bairro Nacional",
        "titulo": "Suporte — Cliente Culpa a Norte Tel por Problema de Outro Provedor",
        "cliente": "Sr. Gilmar",
        "equipamento": "ONT Huawei EG8145",
        "briefing": "Cliente reclama que 'a internet da Norte Tel' não deixa ele acessar o site do banco, mas ele também tem um plano de dados móvel de outra operadora no celular.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "59284",
            "horario": "11h00",
            "assunto": "Realizar serviços - configurações",
            "endereco": "AVENIDA BRASIL, 63",
            "cidade": "Colniza",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "CNIZ 03",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Bruna\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99200-3105\n"
                "Ocorrência: Cliente relata não conseguir acessar o site do banco pela internet fixa. Possui também plano de dados móvel de outra operadora."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você testa a internet da casa (Wi-Fi da Norte Tel) num notebook: o site do banco abre perfeitamente. No celular dele, usando dados móveis de outra operadora, o site não abre.",
             "pergunta": "O que esse teste indica?",
             "opcoes": [
                 {"texto": "O problema não está relacionado à internet da Norte Tel — o site abre normalmente pela rede da casa; a falha está no plano de dados móveis de outra operadora", "correta": True,
                  "feedback": "Exatamente esse tipo de teste comparativo é essencial pra isolar a causa real — e nesse caso, claramente não é responsabilidade da Norte Tel."},
                 {"texto": "O problema com certeza é da Norte Tel, já que o cliente reclamou primeiro dela", "correta": False,
                  "feedback": "O teste mostra o contrário — a internet da Norte Tel está funcionando bem; o problema está no celular usando outra rede."},
                 {"texto": "Não dá pra saber a causa sem testar em pelo menos 5 dispositivos diferentes", "correta": False,
                  "feedback": "O teste comparativo simples (funciona numa rede, não funciona na outra) já é suficiente pra isolar a causa nesse caso."},
             ]},
            {"cena": "Você mostra o resultado do teste pro Sr. Gilmar, explicando que a internet de casa está funcionando normalmente.",
             "pergunta": "Como você conduz essa explicação com respeito, já que ele estava convencido de que era culpa da Norte Tel?",
             "opcoes": [
                {
                    "texto": "Explica com calma e mostra o teste na prática (funciona no Wi-Fi, não funciona nos dados móveis), sem soar como se estivesse 'ganhando uma discussão'",
                    "correta": True,
                    "feedback": "Boa conduta — mostrar o teste de forma objetiva e respeitosa ajuda o cliente a entender sem se sentir constrangido por ter presumido errado.",
                },
                {
                    "texto": "Mostra o resultado do teste de velocidade, confirma que a internet contratada está entregando o combinado e encerra o atendimento registrando que estava tudo normal",
                    "correta": False,
                    "feedback": "O número prova o seu ponto, mas não ensina nada ao cliente: ele sai sem entender por que o celular dele falha e volta a chamar. Mostrar a diferença na prática é o que encerra o assunto de verdade.",
                },
                {
                    "texto": "Refaz o teste de velocidade várias vezes até o cliente se convencer de que o resultado é consistente",
                    "correta": False,
                    "feedback": "Repetir o mesmo teste não responde a dúvida dele. O que convence é a demonstração comparada: funciona no Wi-Fi, não funciona nos dados móveis — aí fica claro onde está o problema.",
                },
            ]},
            {"cena": "O Sr. Gilmar entende a explicação e pergunta se você pode ajudar ele a resolver o problema com a outra operadora também.",
             "pergunta": "Qual é a orientação apropriada?",
             "opcoes": [
                 {"texto": "Explica que esse é um problema da outra operadora, fora do escopo da Norte Tel, e sugere que ele entre em contato com o suporte dela", "correta": True,
                  "feedback": "Orientação correta e honesta — reconhece o limite do seu escopo de atuação, mas ainda ajuda o cliente a saber pra onde direcionar o problema real."},
                 {"texto": "Tenta mexer no celular e nas configurações da outra operadora mesmo assim", "correta": False,
                  "feedback": "Isso está fora do seu escopo de trabalho e conhecimento sobre a rede de outra empresa — não é apropriado tentar resolver."},
                 {"texto": "Diz que não é problema seu e sai sem dar nenhuma orientação", "correta": False,
                  "feedback": "Mesmo fora do seu escopo, vale orientar minimamente o cliente sobre pra onde ele deve direcionar o problema."},
             ]},
            {"cena": "Antes de encerrar, você registra o atendimento no sistema da Norte Tel.",
             "pergunta": "O que é importante constar no registro?",
             "opcoes": [
                {
                    "texto": "Que a internet da Norte Tel foi testada e confirmada funcionando normalmente, e que o problema relatado era de outra operadora (fora do escopo do atendimento)",
                    "correta": True,
                    "feedback": "Registro claro e correto — documenta que a rede da Norte Tel foi validada, protegendo o histórico do atendimento contra reclamações futuras sobre o mesmo caso.",
                },
                {
                    "texto": "Só o resultado do teste de velocidade, o horário e o equipamento testado, já que o número medido comprova por si que a entrega estava dentro do contratado",
                    "correta": False,
                    "feedback": "O número sozinho não conta a história: daqui a três meses ninguém vai lembrar que o chamado era sobre a operadora de celular. Sem o contexto, um novo chamado parecido vira retrabalho.",
                },
                {
                    "texto": "A descrição do problema que o cliente relatou, sem citar o resultado do teste feito no local",
                    "correta": False,
                    "feedback": "Registrar a queixa sem a evidência deixa o atendimento sem conclusão. Se o cliente reabrir o caso, não há como mostrar que a rede da Norte Tel foi verificada e estava normal.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55404",
        "bairro": "Bairro Areal",
        "titulo": "Suporte — Pedido de Desconto Não Autorizado",
        "cliente": "Dona Marisa",
        "equipamento": "Nenhum — situação de atendimento",
        "briefing": "Durante o atendimento técnico, a cliente pede pra você aplicar um desconto na mensalidade dela, dizendo que está com dificuldades financeiras.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "54766",
            "horario": "17h00",
            "assunto": "TV - configurações",
            "endereco": "RUA BOA VISTA, 446",
            "cidade": "Pimenta Bueno",
            "referencia": "Em frente ao posto de saúde",
            "caixa_atendimento": "PBW 03",
            "porta_ftth": "2",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: TV - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Fernanda\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99722-8072\n"
                "Ocorrência: Cliente solicita atendimento técnico para configuração do serviço de TV."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Dona Marisa pede, de forma emotiva, que você aplique um desconto na conta dela agora mesmo, já que ela está passando por um momento difícil.",
             "pergunta": "Como você responde com empatia mas dentro do seu papel?",
             "opcoes": [
                {
                    "texto": "Demonstra empatia genuína com a situação dela, mas explica que decisões sobre desconto e negociação de plano são do setor financeiro/comercial, e se oferece pra orientar como entrar em contato com eles",
                    "correta": True,
                    "feedback": "Boa resposta — equilibra empatia real com honestidade sobre os limites do seu papel, sem deixar a cliente sem direção nenhuma.",
                },
                {
                    "texto": "Demonstra empatia e explica que ela pode pedir desconto pelo aplicativo, que costuma ter ofertas de retenção melhores que as do atendimento",
                    "correta": False,
                    "feedback": "Você não tem como saber o que o aplicativo oferece pra ela, e criar essa expectativa pode virar frustração. Encaminhar pro setor certo é ajudar; prometer resultado não.",
                },
                {
                    "texto": "Escuta com atenção e explica que, como técnico, você não tem acesso a essas informações e prefere não opinar sobre a parte financeira do contrato",
                    "correta": False,
                    "feedback": "Está correto e sai pela tangente: ela continua sem saber o que fazer. Não opinar sobre valores é certo, mas indicar o caminho até quem decide é a parte que ajuda de verdade.",
                },
            ]},
            {"cena": "Você conclui o atendimento técnico normalmente, e a cliente agradece a atenção mesmo sem o desconto imediato.",
             "pergunta": "Antes de sair, o que mais você pode fazer pra ajudar de forma dentro do seu papel?",
             "opcoes": [
                {
                    "texto": "Anota o pedido dela no relatório da O.S., sugerindo que o setor comercial entre em contato pra avaliar possibilidades — sem prometer resultado",
                    "correta": True,
                    "feedback": "Isso é uma ajuda real e dentro do seu papel — encaminha a demanda pro setor certo, sem criar falsa expectativa.",
                },
                {
                    "texto": "Ligar você mesmo pro setor comercial ali na frente dela, pra que o pedido seja registrado na hora e ela veja com os próprios olhos que o assunto foi encaminhado",
                    "correta": False,
                    "feedback": "Parece atencioso, mas negociação de plano se faz com o titular, e o setor vai precisar falar com ela de qualquer jeito. A ligação vira uma etapa a mais, não uma a menos.",
                },
                {
                    "texto": "Explicar o passo a passo do contato com o comercial e o horário de atendimento, deixando com ela a decisão de procurar quando puder",
                    "correta": False,
                    "feedback": "Informar o caminho é bom. Mas ela é uma cliente fragilizada, e registrar o pedido no seu relatório faz a empresa vir até ela — em vez de depender de mais uma iniciativa dela.",
                },
            ]},
            {"cena": "Alguns dias depois, você fica sabendo que o setor comercial entrou em contato com Dona Marisa e ofereceu uma condição especial temporária.",
             "pergunta": "O que isso mostra sobre a forma como você conduziu a situação?",
             "opcoes": [
                {
                    "texto": "Que encaminhar corretamente pro setor responsável, sem tentar resolver sozinho, foi a abordagem certa e realmente ajudou a cliente no final",
                    "correta": True,
                    "feedback": "Exatamente — respeitar os limites do seu papel não significa deixar de ajudar; muitas vezes significa encaminhar pra quem pode realmente resolver.",
                },
                {
                    "texto": "Que o setor comercial teria entrado em contato de qualquer forma, já que existe rotina de retenção pra clientes com dificuldade de pagamento",
                    "correta": False,
                    "feedback": "Pode haver rotina, mas quem colocou o caso dela na frente de quem decide foi o seu registro. Descartar a própria contribuição faz perder a lição sobre o que funcionou aqui.",
                },
                {
                    "texto": "Que valeu a pena ter encaminhado, e que da próxima vez você pode adiantar mais o processo já indicando qual desconto pedir ao comercial",
                    "correta": False,
                    "feedback": "Sugerir valores é entrar numa negociação que não é sua, e cria expectativa que o comercial pode não confirmar. O encaminhamento funcionou justamente por ficar no lugar certo.",
                },
            ]},
            {"cena": "Dona Marisa comenta com você, num atendimento futuro, que ficou muito grata pela forma como tudo foi conduzido, mesmo sem resposta imediata.",
             "pergunta": "O que esse retorno reforça sobre atender pedidos fora do seu escopo técnico?",
             "opcoes": [
                {
                    "texto": "Que tratar o cliente com respeito e encaminhar corretamente, mesmo sem poder resolver na hora, já constrói confiança e uma boa experiência com a empresa",
                    "correta": True,
                    "feedback": "Isso — a forma como uma demanda é conduzida, mesmo fora do seu alcance direto, tem grande peso na percepção do cliente sobre o atendimento como um todo.",
                },
                {
                    "texto": "Que a boa experiência veio principalmente do desconto conseguido, e que sem esse resultado ela teria ficado insatisfeita com o atendimento",
                    "correta": False,
                    "feedback": "Ela agradeceu a atenção, não o valor. Amarrar a experiência ao resultado sugere que só vale atender bem quando dá pra resolver — e a maior parte dos pedidos fora do escopo não dá.",
                },
                {
                    "texto": "Que encaminhar pedidos fora do escopo é sempre positivo, e que vale prometer o encaminhamento mesmo quando não houver a quem encaminhar",
                    "correta": False,
                    "feedback": "Encaminhar quando existe destino é uma coisa; prometer encaminhamento no vazio é criar espera por um retorno que não vem. A confiança vem de cumprir, não de acolher.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55458",
        "bairro": "Cidade Nova",
        "titulo": "Suporte — Comunicação Clara ao Encerrar o Atendimento",
        "cliente": "Sr. Tadeu",
        "equipamento": "ONT Huawei EG8145, roteador",
        "briefing": "Você resolveu um problema técnico relativamente complexo (troca de configuração da ONT), mas o cliente não entende bem o que foi feito.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "56832",
            "horario": "11h00",
            "assunto": "Realizar serviços - configurações",
            "endereco": "RUA RIO BRANCO, 573",
            "cidade": "Alta Floresta",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "AFT 03",
            "porta_ftth": "5",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Rafael\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99409-2607\n"
                "Ocorrência: Cliente relata instabilidade na conexão. Solicita verificação técnica no local."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O serviço foi tecnicamente bem resolvido, mas o Sr. Tadeu pergunta, um pouco perdido: 'Mas o que exatamente você fez aí?'",
             "pergunta": "Qual é a melhor forma de responder?",
             "opcoes": [
                {
                    "texto": "Resumir em linguagem simples o que mudou e por quê (ex: 'a ONT estava configurada de um jeito que travava sua internet às vezes; eu ajustei isso'), sem entrar em jargão técnico desnecessário",
                    "correta": True,
                    "feedback": "Boa comunicação — o cliente não precisa entender os detalhes técnicos completos, mas merece uma explicação clara do que mudou e por que isso ajuda ele.",
                },
                {
                    "texto": "Explicar tecnicamente o que foi ajustado e oferecer anotar os termos, pra que ele possa pesquisar depois e entender melhor cada um deles",
                    "correta": False,
                    "feedback": "Transfere pro cliente o trabalho de entender o que você poderia ter explicado em uma frase. Ele quer saber o que aconteceu com a internet dele, não estudar redes.",
                },
                {
                    "texto": "Explicar que o problema era de configuração e que já está resolvido, sem detalhar o que foi alterado, pra não confundir o cliente com detalhes",
                    "correta": False,
                    "feedback": "Poupar detalhes é bom; omitir o essencial não. Sem entender o que mudou, ele não sabe o que observar nem o que contar se o sintoma voltar num próximo chamado.",
                },
            ]},
            {"cena": "O Sr. Tadeu, satisfeito com a explicação, pergunta se esse tipo de problema pode voltar a acontecer.",
             "pergunta": "Como você responde com honestidade?",
             "opcoes": [
                {
                    "texto": "Explica honestamente que a mudança feita reduz bastante a chance do problema voltar, mas que ele deve avisar se notar o mesmo sintoma de novo",
                    "correta": True,
                    "feedback": "Resposta honesta e realista — não promete uma garantia absoluta impossível, mas também tranquiliza o cliente com informação real.",
                },
                {
                    "texto": "Explica que o problema não deve voltar, e que se voltar provavelmente será por outra causa, já que essa configuração ficou corrigida em definitivo",
                    "correta": False,
                    "feedback": "Está quase certo, mas descarta antecipadamente a hipótese mais útil: se o mesmo sintoma reaparecer, saber que ele já ocorreu por essa causa é a primeira pista do próximo atendimento.",
                },
                {
                    "texto": "Explica que depende de vários fatores fora do controle da empresa, e que problemas de internet podem voltar a qualquer momento por muitos motivos",
                    "correta": False,
                    "feedback": "É verdade em tese e inútil na prática: deixa o cliente sem noção nenhuma do que esperar. Ele merece saber que a chance caiu bastante, e o que fazer se ainda assim acontecer.",
                },
            ]},
            {"cena": "Antes de sair, você entrega ao cliente um resumo simples por escrito (ou por WhatsApp) do que foi feito.",
             "pergunta": "Qual é o principal benefício dessa prática?",
             "opcoes": [
                {
                    "texto": "Dá ao cliente um registro que ele pode consultar depois, e facilita caso outro técnico precise dar continuidade ao atendimento no futuro",
                    "correta": True,
                    "feedback": "Exatamente — documentação clara pro próprio cliente é uma boa prática que evita retrabalho e melhora a experiência dele com a empresa.",
                },
                {
                    "texto": "Serve principalmente pra comprovar o serviço executado, caso haja divergência sobre o que foi feito ou cobrado naquela visita técnica",
                    "correta": False,
                    "feedback": "Comprovação é um efeito colateral, não o objetivo. O resumo existe pro cliente entender e pro próximo técnico não começar do zero — o benefício é operacional, não jurídico.",
                },
                {
                    "texto": "Serve pra que o cliente possa repassar as informações ao suporte por telefone, evitando que ele precise de uma nova visita técnica no futuro",
                    "correta": False,
                    "feedback": "Ajuda nisso, sim. Mas o ganho maior é mais amplo: o registro fica com o cliente E orienta quem atender a próxima ocorrência, mesmo que seja outra pessoa da equipe.",
                },
            ]},
            {"cena": "O Sr. Tadeu agradece e comenta que o técnico anterior, numa visita antiga, saiu sem explicar nada, o que o deixou inseguro sobre o serviço.",
             "pergunta": "Como você recebe esse comentário comparativo do cliente?",
             "opcoes": [
                {
                    "texto": "Agradece o feedback com humildade, sem criticar o colega anterior, e reforça que a Norte Tel valoriza deixar o cliente bem informado",
                    "correta": True,
                    "feedback": "Boa conduta profissional — recebe o elogio sem usar isso pra falar mal de um colega, mantendo uma postura de equipe.",
                },
                {
                    "texto": "Agradece e explica que a equipe tem padrões diferentes de atendimento, e que ele pode registrar essa observação na pesquisa de satisfação",
                    "correta": False,
                    "feedback": "Empurra pra pesquisa um elogio que ele fez agora, e ainda insinua que a equipe é desigual. Receber bem e reforçar o padrão que a empresa busca vale mais do que redirecionar.",
                },
                {
                    "texto": "Agradece e comenta que cada técnico tem seu jeito de trabalhar, e que o colega anterior provavelmente estava com a agenda apertada naquele dia",
                    "correta": False,
                    "feedback": "Justificar o colega sem saber o que houve é chute, e ainda soa como se explicar informar o cliente fosse opcional quando o dia aperta. Não é: é parte do serviço.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55512",
        "bairro": "Bairro Redenção",
        "titulo": "Instalação — Trabalho em Altura com Escada",
        "cliente": "Sr. Belisário",
        "equipamento": "Escada, cinto de segurança, fibra drop",
        "briefing": "A entrada de fibra precisa ser fixada na parte alta da fachada da casa, a uns 4 metros do chão.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "53379",
            "horario": "15h00",
            "assunto": "Ancoragem Drop/Fibra",
            "endereco": "TRAVESSA DAS PALMEIRAS, 880",
            "cidade": "Cujubim",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "CUJU 03",
            "porta_ftth": "5",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Ancoragem Drop/Fibra\n"
                "Descrição O.S. anterior: - Solicitante: atendente Patrícia\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99858-7026\n"
                "Ocorrência: Cliente contratou instalação de fibra óptica. Entrada deverá ser fixada na parte alta da fachada do imóvel."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": True,
            "atividade_esperada": "Infraestrutura de Fibra",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [
                "Cinto tipo paraquedas com ancoragem dorsal, torácica, ponto de ancoragem para posicionamento e suspensão",
            ],
        },
        "decisoes": [
            {"cena": "Você posiciona a escada numa superfície de terra irregular, um pouco inclinada, perto do local onde precisa trabalhar.",
             "pergunta": "O que fazer antes de subir?",
             "opcoes": [
                {
                    "texto": "Nivelar e estabilizar bem a base da escada (usando calços se necessário) e testar a firmeza antes de subir com qualquer ferramenta",
                    "correta": True,
                    "feedback": "Correto — a maioria dos acidentes com escada acontece por base instável; conferir isso antes de subir é o passo de segurança mais básico e importante.",
                },
                {
                    "texto": "Reposicionar a escada num trecho de piso firme, mesmo que isso obrigue a trabalhar num ângulo pior pra alcançar o ponto de fixação",
                    "correta": False,
                    "feedback": "Piso firme é o ideal quando existe. Mas trabalhar em ângulo ruim em cima da escada cria outro risco: com calços e a base nivelada, dá pra manter o ponto certo com segurança.",
                },
                {
                    "texto": "Abrir bem a escada, apoiar firme na parede e pedir que alguém fique por perto observando, pra reagir rápido caso ela comece a escorregar no terreno",
                    "correta": False,
                    "feedback": "Alguém observando não segura escada em queda — a essa altura já é tarde. A estabilidade tem que estar na base antes de você subir, não na reação de quem está embaixo.",
                },
            ]},
            {"cena": "Com a escada estabilizada, você sobe pra fixar o suporte da fibra na fachada, a cerca de 4 metros de altura.",
             "pergunta": "Qual equipamento de proteção é importante nesse trabalho em altura?",
             "opcoes": [
                {
                    "texto": "Cinto de segurança apropriado pra trabalho em altura, seguindo as normas e o treinamento da empresa",
                    "correta": True,
                    "feedback": "Isso — trabalho em altura acima de determinada distância exige proteção contra queda, e essa é uma exigência de segurança que não deve ser pulada.",
                },
                {
                    "texto": "Capacete e luvas de proteção, já que o principal risco em fachada é a queda de material e o contato com bordas cortantes durante a fixação",
                    "correta": False,
                    "feedback": "Capacete e luva entram no conjunto, mas protegem contra o que cai, não contra você cair. Trabalho em altura exige, antes de tudo, o que impede a queda.",
                },
                {
                    "texto": "Calçado de segurança com solado antiderrapante, que é o que evita escorregar nos degraus durante a subida e a descida com ferramenta na mão",
                    "correta": False,
                    "feedback": "Calçado adequado é obrigatório e reduz mesmo o risco de escorregão. Só que se o escorregão acontecer, é o cinto que decide se foi um susto ou uma queda.",
                },
            ]},
            {"cena": "No meio do trabalho, você percebe que esqueceu uma ferramenta no carro.",
             "pergunta": "Qual é a atitude correta?",
             "opcoes": [
                {
                    "texto": "Descer da escada com segurança (seguindo o procedimento normal), buscar a ferramenta, e só então subir de novo",
                    "correta": True,
                    "feedback": "Correto — mesmo que pareça 'perda de tempo', descer e subir corretamente é sempre mais seguro do que tentar improvisar em cima da escada.",
                },
                {
                    "texto": "Terminar primeiro a etapa que já está em andamento e descer uma vez só, evitando subir e descer várias vezes durante o mesmo serviço",
                    "correta": False,
                    "feedback": "Menos subidas é bom princípio, mas não vale improvisar pra chegar lá. Se a etapa depende da ferramenta que ficou no carro, terminar sem ela é justamente o improviso a evitar.",
                },
                {
                    "texto": "Pedir pro cliente trazer a ferramenta até o pé da escada, e descer só até o degrau mais baixo pra pegar sem precisar sair completamente",
                    "correta": False,
                    "feedback": "Melhor que receber jogado, mas continua sendo manobra na escada com uma mão ocupada. Descer por completo custa vinte segundos e é o procedimento que existe justamente pra isso.",
                },
            ]},
            {"cena": "Serviço concluído com segurança. O Sr. Belisário comenta que o vizinho dele 'sempre sobe sem cinto e nunca aconteceu nada'.",
             "pergunta": "Como você responde a esse comentário?",
             "opcoes": [
                {
                    "texto": "Explica com respeito que seguir o procedimento de segurança não é sobre 'nunca ter acontecido nada', é sobre reduzir o risco de um acidente sério que pode acontecer a qualquer momento",
                    "correta": True,
                    "feedback": "Boa resposta — explica a lógica da segurança preventiva sem julgar o vizinho, focando na sua própria prática correta.",
                },
                {
                    "texto": "Concorda que muitos profissionais trabalham assim, mas explica que a Norte Tel exige o equipamento e que você prefere não correr risco",
                    "correta": False,
                    "feedback": "Colocar como preferência pessoal enfraquece: vira 'ele é mais medroso'. O ponto é que acidente em altura é raro e grave — o cinto existe pra esse dia, não pros outros.",
                },
                {
                    "texto": "Explica que o vizinho pode ser autônomo e não ter as mesmas obrigações, e que empresas seguem regras mais rígidas de segurança do trabalho",
                    "correta": False,
                    "feedback": "Autônomo também cai. Reduzir a questão a obrigação de empresa sugere que o cinto é burocracia — quando o motivo é que a queda não avisa antes de acontecer.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55566",
        "bairro": "Bairro Nacional",
        "titulo": "Instalação — Proximidade de Rede Elétrica",
        "cliente": "Sr. Elienai",
        "equipamento": "Fibra drop, EPI",
        "briefing": "A rota da fibra até a casa passa perto de fiação elétrica de baixa tensão na fachada.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "59415",
            "horario": "09h00",
            "assunto": "Ancoragem Drop/Fibra",
            "endereco": "AVENIDA MARECHAL RONDON, 708",
            "cidade": "Alto Alegre",
            "referencia": "Casa de dois andares, grade preta",
            "caixa_atendimento": "AAPC 03",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Ancoragem Drop/Fibra\n"
                "Descrição O.S. anterior: - Solicitante: atendente Rafael\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99511-1027\n"
                "Ocorrência: Cliente contratou instalação de fibra óptica. Rota de entrada passa próxima à fiação elétrica da fachada."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": True,
            "atividade_esperada": "Infraestrutura de Fibra",
            "riscos_obrigatorios": [
                "Fiação exposta ou cabos soltos, Cruzetas ou Roldanas danificadas",
            ],
            "epis_obrigatorios": [
                "Luva isolante elétrica",
            ],
        },
        "decisoes": [
            {"cena": "Você percebe que o ponto onde precisa fixar o suporte da fibra fica bem próximo de um fio elétrico exposto.",
             "pergunta": "Qual é a atitude correta antes de continuar o trabalho?",
             "opcoes": [
                {
                    "texto": "Avaliar a distância de segurança necessária, e se estiver arriscado demais, buscar uma rota alternativa ou solicitar apoio especializado antes de continuar",
                    "correta": True,
                    "feedback": "Correto — proximidade com rede elétrica é um risco sério; a prioridade é sempre avaliar e garantir distância segura antes de qualquer manuseio.",
                },
                {
                    "texto": "Continuar com atenção redobrada, usando ferramentas com cabo isolado e evitando encostar na rede elétrica durante a fixação do suporte",
                    "correta": False,
                    "feedback": "Ferramenta isolada protege contra contato direto, não contra arco elétrico em rede energizada, que salta sem toque. Distância mínima não é cuidado extra: é o que define se dá pra trabalhar ali.",
                },
                {
                    "texto": "Fotografar a situação, registrar na O.S. que o ponto está próximo da rede elétrica e seguir o trabalho mantendo o máximo de atenção possível",
                    "correta": False,
                    "feedback": "O registro é útil pra depois e não muda nada agora. Se a distância não é segura, nenhum grau de atenção compensa — o que muda o risco é mudar a rota ou pedir apoio.",
                },
            ]},
            {"cena": "Você decide buscar uma rota alternativa, um pouco mais longa, mas que mantém distância segura da fiação elétrica.",
             "pergunta": "Isso é a decisão certa mesmo custando mais tempo de trabalho?",
             "opcoes": [
                {
                    "texto": "Sim — segurança sempre vem antes de rapidez; alguns minutos a mais de trabalho não se comparam ao risco de um acidente elétrico",
                    "correta": True,
                    "feedback": "Exatamente essa é a prioridade correta — nenhuma economia de tempo justifica um risco elétrico desnecessário.",
                },
                {
                    "texto": "Sim, e vale registrar o tempo extra na O.S. pra que a central saiba que o atraso na agenda teve motivo técnico e não foi falta de produtividade",
                    "correta": False,
                    "feedback": "Registrar o motivo é razoável. Mas colocar isso como o ponto principal inverte a lógica: a decisão se justifica sozinha pela segurança, não por precisar de defesa perante a agenda.",
                },
                {
                    "texto": "Sim, desde que a rota alternativa não comprometa a qualidade do sinal, o que precisaria ser confirmado com o medidor antes de aceitar o desvio",
                    "correta": False,
                    "feedback": "Medir depois é parte do serviço de qualquer forma. Mas condicionar a escolha segura à qualidade do sinal inverte a prioridade: se a rota curta é perigosa, ela está fora antes de qualquer medição.",
                },
            ]},
            {"cena": "Durante o trabalho na rota alternativa, você percebe um fio elétrico da própria residência com isolamento visivelmente danificado, sem relação com o seu serviço.",
             "pergunta": "O que fazer diante dessa observação?",
             "opcoes": [
                {
                    "texto": "Avisar o cliente sobre o risco identificado e sugerir que ele contrate um eletricista, mesmo não sendo parte do seu serviço",
                    "correta": True,
                    "feedback": "Boa conduta — mesmo fora do seu escopo de trabalho, alertar sobre um risco de segurança que você identificou é uma atitude responsável.",
                },
                {
                    "texto": "Avisar o cliente e se oferecer pra isolar provisoriamente o trecho danificado com fita isolante, reduzindo o risco até ele chamar um eletricista",
                    "correta": False,
                    "feedback": "A intenção é boa e o gesto é indevido: fita sobre fiação danificada esconde o problema e assume responsabilidade sobre um serviço que não é seu. Avisar já é a contribuição correta.",
                },
                {
                    "texto": "Registrar a observação na O.S. e deixar que a central informe o cliente pelo canal oficial, evitando alarmar ele durante a visita técnica",
                    "correta": False,
                    "feedback": "Esperar o canal oficial atrasa um aviso de risco que ele pode resolver esta semana. Falar com calma no local não alarma — informa a pessoa que pode agir.",
                },
            ]},
            {"cena": "Serviço concluído com segurança. Você registra o atendimento antes de seguir pro próximo cliente.",
             "pergunta": "Vale mencionar no registro a observação sobre o fio elétrico danificado da casa?",
             "opcoes": [
                {
                    "texto": "Sim, como uma observação separada — documenta que você alertou o cliente sobre um risco identificado, mesmo fora do escopo do serviço contratado",
                    "correta": True,
                    "feedback": "Boa prática — documentar esse tipo de alerta protege você e demonstra o cuidado profissional durante o atendimento.",
                },
                {
                    "texto": "Sim, registrando junto que o cliente foi orientado e ficou ciente, o que encerra a responsabilidade da Norte Tel sobre aquele risco identificado",
                    "correta": False,
                    "feedback": "O registro documenta o alerta, e é bom que documente. Mas enquadrar como 'encerra a responsabilidade' muda o propósito: o registro serve pra proteger o cliente, não pra blindar a empresa.",
                },
                {
                    "texto": "Sim, e vale sugerir na mesma observação que a central agende uma nova visita depois pra verificar se o cliente chegou a resolver o problema elétrico da casa",
                    "correta": False,
                    "feedback": "A rede elétrica interna não é serviço da Norte Tel, e agendar visita pra fiscalizar o cliente ultrapassa o papel. Registrar o alerta é o suficiente.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55618",
        "bairro": "Costa e Silva",
        "titulo": "Suporte — Cão Solto no Local",
        "cliente": "Sra. Neuza",
        "equipamento": "Nenhum — situação de segurança",
        "briefing": "Você chega na casa pra um atendimento agendado, mas há um cão de porte grande solto no quintal, sem contenção visível.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "57754",
            "horario": "08h30",
            "assunto": "Sem Internet",
            "endereco": "RUA RIO BRANCO, 764",
            "cidade": "Cacoal",
            "referencia": "Portão de madeira, casa de esquina",
            "caixa_atendimento": "CWL 04",
            "porta_ftth": "7",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Sem Internet\n"
                "Descrição O.S. anterior: - Solicitante: atendente Aline\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99628-1387\n"
                "Ocorrência: Cliente sem internet. Solicita visita técnica para verificação do sinal."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Ao chegar no portão, você vê o cachorro se aproximando, latindo, sem ninguém por perto pra contê-lo.",
             "pergunta": "Qual é a atitude correta?",
             "opcoes": [
                {
                    "texto": "Não entrar no local, e pedir educadamente (por interfone, campainha ou ligação) que o animal seja contido antes de você acessar a propriedade",
                    "correta": True,
                    "feedback": "Correto — segurança pessoal vem primeiro; entrar num local com animal solto e não contido é um risco real que deve ser evitado.",
                },
                {
                    "texto": "Ligar pra central relatando animal solto no endereço e pedir o reagendamento do atendimento pra uma data em que o acesso ao imóvel esteja liberado",
                    "correta": False,
                    "feedback": "Reagendar já é abrir mão do dia sem tentar o simples: na maioria das vezes basta pedir pra prender o cachorro e o serviço acontece agora. A central entra se o contato falhar.",
                },
                {
                    "texto": "Aguardar do lado de fora até alguém aparecer, sem chamar, já que a movimentação no portão costuma trazer o morador até a frente da casa",
                    "correta": False,
                    "feedback": "Esperar sem avisar deixa o cachorro latindo e você parado. Chamar pelo interfone ou ligar resolve em segundos e já pede o que você precisa: o animal contido antes de entrar.",
                },
            ]},
            {"cena": "A Sra. Neuza contém o cachorro numa área fechada da casa e pede desculpas pelo imprevisto.",
             "pergunta": "Como você segue com o atendimento?",
             "opcoes": [
                {
                    "texto": "Agradece a colaboração, confirma que está seguro pra entrar, e segue com o atendimento normalmente",
                    "correta": True,
                    "feedback": "Isso — depois que o risco foi removido (animal contido), o atendimento pode prosseguir com segurança e normalidade.",
                },
                {
                    "texto": "Agradece, entra e pede pra ela permanecer por perto durante todo o serviço, caso o cachorro escape da área onde foi colocado",
                    "correta": False,
                    "feedback": "Pedir que ela fique de prontidão transfere pra cliente a função de te proteger e prende ela no atendimento inteiro. Se o animal está contido, o serviço segue normalmente.",
                },
                {
                    "texto": "Agradece e aproveita pra orientar que, em visitas futuras, o animal já esteja contido antes do horário marcado pra não atrasar o atendimento",
                    "correta": False,
                    "feedback": "A orientação faz sentido e a hora não: ela acabou de resolver e se desculpar. Fica melhor como observação no registro da O.S. do que como cobrança logo depois do gesto dela.",
                },
            ]},
            {"cena": "Durante o serviço, o cachorro late incessantemente do outro lado da porta, deixando o ambiente tenso.",
             "pergunta": "Isso deve interromper o atendimento?",
             "opcoes": [
                {
                    "texto": "Não necessariamente — desde que o animal esteja de fato contido e não represente risco real, o latido por si só não impede a continuidade do serviço",
                    "correta": True,
                    "feedback": "Correto — o latido é desconfortável, mas o que importa pra segurança é a contenção efetiva do animal, não o barulho em si.",
                },
                {
                    "texto": "Não, mas vale pedir pra cliente colocar o animal num cômodo mais distante, pra que o latido não atrapalhe sua concentração durante o serviço",
                    "correta": False,
                    "feedback": "Pedido razoável em tese, mas você está na casa dela e o animal já foi contido. Latido incomoda e não impede o trabalho — insistir por conforto vira exigência.",
                },
                {
                    "texto": "Sim, porque o latido contínuo indica que o animal está agitado e pode acabar forçando a porta, criando um risco real enquanto você trabalha ali dentro",
                    "correta": False,
                    "feedback": "Cachorro late por estranho na casa, agitado ou não — o latido sozinho não indica que a contenção vai falhar. O que se avalia é se a área é realmente segura, e ela é.",
                },
            ]},
            {"cena": "Atendimento concluído com sucesso, sem nenhum incidente.",
             "pergunta": "Vale registrar essa situação do animal solto na O.S.?",
             "opcoes": [
                {
                    "texto": "Sim, uma nota breve sobre o animal ajuda a preparar melhor uma próxima visita técnica a esse endereço",
                    "correta": True,
                    "feedback": "Boa prática — esse tipo de informação ajuda o próximo técnico (ou você mesmo, numa futura visita) a já chegar preparado pra pedir a contenção do animal com antecedência.",
                },
                {
                    "texto": "Não, já que o problema foi resolvido pela cliente na hora e não houve incidente nenhum durante todo o atendimento realizado no endereço",
                    "correta": False,
                    "feedback": "Não houve incidente justamente porque você não entrou. A nota não é queixa: é informação pro próximo técnico chegar já sabendo que precisa chamar antes de abrir o portão.",
                },
                {
                    "texto": "Sim, registrando que o acesso ficou bloqueado por animal solto e sugerindo que os próximos atendimentos nesse endereço sejam agendados por telefone antes",
                    "correta": False,
                    "feedback": "A nota é bem-vinda, mas 'acesso bloqueado' exagera o que aconteceu e a sugestão cria regra pro endereço. Basta a observação de que há cachorro solto na área.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55670",
        "bairro": "Tiradentes",
        "titulo": "Instalação — Aproximação de Tempestade",
        "cliente": "Sr. Nivaldo",
        "equipamento": "Fibra drop, ferramentas de instalação externa",
        "briefing": "Você está no meio de uma instalação externa quando o céu começa a fechar, com sinais claros de tempestade se aproximando.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "58788",
            "horario": "17h00",
            "assunto": "Instalação Fibra Optica",
            "endereco": "RUA RIO BRANCO, 37",
            "cidade": "São Miguel",
            "referencia": "Perto do campo de futebol",
            "caixa_atendimento": "SMGE 04",
            "porta_ftth": "5",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Instalação Fibra Optica\n"
                "Descrição O.S. anterior: - Solicitante: atendente Patrícia\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99743-8578\n"
                "Ocorrência: Cliente contratou instalação de fibra óptica, com execução externa agendada."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": True,
            "atividade_esperada": "Instalação, manutenção ou retirada de rede Fibra Optica",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O vento começa a aumentar e você ouve trovões distantes enquanto ainda está em cima da escada, trabalhando na fachada externa.",
             "pergunta": "Qual é a atitude correta diante desse cenário?",
             "opcoes": [
                {
                    "texto": "Descer da escada com segurança imediatamente e interromper o trabalho externo até a tempestade passar",
                    "correta": True,
                    "feedback": "Correto — trovoada com risco de raio é motivo suficiente pra interromper qualquer trabalho em altura ou ao ar livre imediatamente, mesmo com o serviço incompleto.",
                },
                {
                    "texto": "Descer da escada e continuar a parte do serviço que dá pra fazer no chão, aproveitando o tempo até a tempestade passar completamente",
                    "correta": False,
                    "feedback": "Descer está certo, e a intenção de aproveitar o tempo também. O cuidado é não seguir com nada que exija estar do lado de fora perto de cabo e estrutura metálica enquanto há raio.",
                },
                {
                    "texto": "Terminar apenas a fixação do suporte, que já está quase pronta, e descer em seguida antes que a chuva realmente comece a cair no local",
                    "correta": False,
                    "feedback": "É exatamente o pensamento que causa acidente: 'falta pouco'. Raio cai antes da chuva chegar, e você está no ponto mais alto com estrutura metálica na mão.",
                },
            ]},
            {"cena": "Você desce, guarda as ferramentas e explica ao Sr. Nivaldo que vai aguardar a tempestade passar antes de continuar.",
             "pergunta": "Como você conduz essa comunicação com o cliente?",
             "opcoes": [
                {
                    "texto": "Explica com clareza que é uma pausa de segurança necessária, e que retomará assim que for seguro, sem prometer um horário exato",
                    "correta": True,
                    "feedback": "Boa comunicação — transparente sobre o motivo real da pausa, sem criar uma expectativa de tempo que pode não se cumprir (já que depende do clima).",
                },
                {
                    "texto": "Explica que precisa interromper por segurança e dá uma previsão aproximada, dizendo que costuma dar pra retomar em uns 30 ou 40 minutos",
                    "correta": False,
                    "feedback": "Uma previsão acalma o cliente e vira problema se o tempo não colaborar. Dizer que retoma assim que for seguro é honesto e não cria uma expectativa que não depende de você.",
                },
                {
                    "texto": "Explica a pausa e sugere que o cliente aproveite pra decidir se prefere reagendar, já que não há garantia de que o tempo vai melhorar hoje",
                    "correta": False,
                    "feedback": "Oferecer reagendamento antes de saber se será preciso empurra pro cliente uma decisão que ainda não existe. A pausa costuma ser curta; reagendar é o plano B, não o primeiro assunto.",
                },
            ]},
            {"cena": "Depois de 40 minutos, a tempestade passa e o tempo melhora visivelmente, sem mais trovões.",
             "pergunta": "O que fazer antes de retomar o trabalho em altura?",
             "opcoes": [
                {
                    "texto": "Confirmar que não há mais risco aparente de raio, e verificar se a escada e o local de trabalho não ficaram escorregadios pela chuva",
                    "correta": True,
                    "feedback": "Correto — além do risco de raio ter passado, vale checar condições físicas (escorregão) que a própria chuva pode ter deixado como novo risco.",
                },
                {
                    "texto": "Verificar se a escada e a fachada secaram o suficiente e retomar, já que o fim da chuva indica que a formação de raios também passou",
                    "correta": False,
                    "feedback": "Chuva parando não significa raio parando: descarga acontece com o tempo já limpando, inclusive a alguns quilômetros da nuvem. As duas coisas precisam ser conferidas separadamente.",
                },
                {
                    "texto": "Secar a escada e os degraus com um pano, calçar luva antiderrapante e retomar o trabalho com atenção redobrada ao apoio dos pés em cada degrau",
                    "correta": False,
                    "feedback": "Secar e melhorar a aderência é bom, mas trata só metade: falta confirmar que não há mais risco de descarga elétrica antes de voltar pro ponto mais alto da fachada.",
                },
            ]},
            {"cena": "Serviço concluído com segurança, já mais tarde do que planejado por causa da pausa.",
             "pergunta": "Como você trata esse atraso causado pelo clima com o cliente?",
             "opcoes": [
                {
                    "texto": "Explica com transparência que o atraso foi por segurança durante a tempestade, e agradece a paciência dele",
                    "correta": True,
                    "feedback": "Boa conduta — reconhecer o atraso com uma explicação honesta relacionada à segurança é totalmente compreensível e profissional.",
                },
                {
                    "texto": "Explica que o atraso foi da tempestade e comenta que, se ele preferir, pode registrar na avaliação que o serviço saiu fora do horário previsto",
                    "correta": False,
                    "feedback": "Trazer a avaliação à tona sugere que houve falha a ser reportada. Não houve: a pausa foi correta. Explicar e agradecer a paciência encerra bem, sem convidar a uma queixa.",
                },
                {
                    "texto": "Não comenta o atraso pra não dar destaque ao ocorrido, já que o cliente acompanhou tudo e sabe exatamente por que o serviço demorou mais",
                    "correta": False,
                    "feedback": "Ele acompanhou, mas o reconhecimento tem valor: nomear o motivo e agradecer a espera é o que transforma um contratempo em boa impressão do atendimento.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55722",
        "bairro": "Aponiã",
        "titulo": "Instalação — Ferramenta com Defeito",
        "cliente": "Sr. Wellington",
        "equipamento": "Máquina de fusão óptica",
        "briefing": "Ao preparar a máquina de fusão pra fazer uma emenda, você percebe que ela está apresentando um comportamento estranho.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "55874",
            "horario": "16h00",
            "assunto": "Instalação Fibra Optica",
            "endereco": "RUA DOS PIONEIROS, 362",
            "cidade": "Conselvan",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "AYPO 04",
            "porta_ftth": "3",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Instalação Fibra Optica\n"
                "Descrição O.S. anterior: - Solicitante: atendente Aline\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99345-4061\n"
                "Ocorrência: Cliente contratou instalação de fibra óptica, com necessidade de emenda na rede externa."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Instalação, manutenção ou retirada de rede Fibra Optica",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "A máquina de fusão está emitindo um som diferente do normal e um alerta de erro intermitente na tela, mesmo depois de reiniciada.",
             "pergunta": "Qual é a atitude correta?",
             "opcoes": [
                {
                    "texto": "Não usar o equipamento nesse estado, e reportar o problema pra central pra avaliação ou substituição antes de continuar o serviço",
                    "correta": True,
                    "feedback": "Correto — usar um equipamento com sinais de defeito pode comprometer a qualidade da emenda (e o sinal do cliente) ou até representar risco; reportar é o caminho certo.",
                },
                {
                    "texto": "Testar a máquina em uma emenda de descarte primeiro e, se a fusão sair dentro do padrão, usar normalmente no serviço do cliente",
                    "correta": False,
                    "feedback": "Uma emenda boa não garante a próxima: alerta de erro indica falha que pode ser intermitente. O cliente ficaria com uma emenda de qualidade duvidosa no meio do enlace.",
                },
                {
                    "texto": "Desligar e religar a máquina, limpar os eletrodos e refazer a calibração, procedimentos que costumam resolver a maior parte dos alertas do equipamento",
                    "correta": False,
                    "feedback": "Limpeza e calibração fazem parte da rotina e podem mesmo resolver. Mas o alerta veio acompanhado de ruído diferente — isso é sintoma mecânico, e aí a máquina precisa ser avaliada.",
                },
            ]},
            {"cena": "Você liga pra central explicando a situação e pede orientação, já que o cliente está esperando o serviço.",
             "pergunta": "Como você comunica isso ao Sr. Wellington enquanto aguarda a resposta da central?",
             "opcoes": [
                {
                    "texto": "Explica com transparência que identificou um problema no equipamento e que está verificando a melhor solução, sem prometer um prazo que ainda não está confirmado",
                    "correta": True,
                    "feedback": "Boa comunicação — honesta sobre a situação real, sem criar expectativa de prazo antes de ter uma resposta concreta da central.",
                },
                {
                    "texto": "Explica o problema no equipamento e dá uma estimativa própria de prazo, tomando como base quanto a central costuma demorar pra resolver esse tipo de situação",
                    "correta": False,
                    "feedback": "Sua estimativa vira promessa da empresa na cabeça do cliente. Enquanto a central não confirmar, o honesto é dizer que está sendo verificado — sem número.",
                },
                {
                    "texto": "Explica que houve um imprevisto com o equipamento e sugere que o cliente reagende, já que a solução pode demorar mais do que o previsto",
                    "correta": False,
                    "feedback": "Reagendar antes da resposta da central é decidir pelo cliente e pode ser desnecessário — neste caso um colega chegou com equipamento reserva no mesmo dia.",
                },
            ]},
            {"cena": "A central orienta que outro técnico da região, com equipamento reserva, pode vir dar continuidade ao serviço ainda no mesmo dia.",
             "pergunta": "O que você faz até a chegada do colega?",
             "opcoes": [
                {
                    "texto": "Deixa tudo preparado (fibra limpa, posicionada) pra que o colega possa fazer a fusão rapidamente assim que chegar, otimizando o tempo",
                    "correta": True,
                    "feedback": "Boa atitude colaborativa — preparar o terreno pro colega reduz o tempo total de espera do cliente, mesmo com a troca de técnico.",
                },
                {
                    "texto": "Aguarda o colega mantendo tudo como está, pra que ele avalie a situação por conta própria e conduza a fusão do jeito que preferir trabalhar",
                    "correta": False,
                    "feedback": "Respeitar o jeito de cada um faz sentido, mas limpar e posicionar a fibra é preparo padrão, não preferência. Deixar pronto economiza o tempo do cliente e o do colega.",
                },
                {
                    "texto": "Aproveita pra concluir todo o restante da instalação e deixa apenas a fusão pendente, avisando ao cliente que o serviço já está quase finalizado",
                    "correta": False,
                    "feedback": "Adiantar o restante é bom uso do tempo. O cuidado é com o 'quase finalizado': sem a fusão não há sinal nenhum, e o cliente pode entender que já dá pra usar a internet.",
                },
            ]},
            {"cena": "O colega chega, faz a fusão com o equipamento reserva, e o serviço é concluído com sucesso ainda no mesmo dia.",
             "pergunta": "O que registrar sobre esse atendimento?",
             "opcoes": [
                {
                    "texto": "O problema identificado no equipamento original, a ação tomada (reportar e não usar), e que o serviço foi concluído com apoio de outro técnico — útil pra manutenção do equipamento com defeito",
                    "correta": True,
                    "feedback": "Registro completo — ajuda a central a dar manutenção correta no equipamento com defeito e documenta bem como o atendimento foi resolvido apesar do imprevisto.",
                },
                {
                    "texto": "Que o serviço foi concluído com apoio de outro técnico por indisponibilidade de equipamento, sem detalhar o alerta específico da máquina",
                    "correta": False,
                    "feedback": "Sem o sintoma descrito, a manutenção recebe uma máquina 'com problema' e vai ter que descobrir qual. O alerta e o ruído são a informação que acelera o conserto.",
                },
                {
                    "texto": "Que a máquina apresentou alerta de erro e foi reportada, e sugerir na mesma observação que o equipamento seja substituído em definitivo",
                    "correta": False,
                    "feedback": "Registrar o alerta está certo; decidir pela substituição não é sua alçada. Descreva o que observou — quem avalia o equipamento decide entre reparo e troca.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55780",
        "bairro": "Setor Industrial",
        "titulo": "Suporte — Ligação Clandestina Encontrada",
        "cliente": "Comércio Depósito São José",
        "equipamento": "Cabo de rede, CTO",
        "briefing": "Durante um atendimento de rotina, você percebe um cabo saindo de forma irregular da CTO, aparentando uma ligação não autorizada de sinal.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "57053",
            "horario": "16h30",
            "assunto": "Reativar Cliente na CTO",
            "endereco": "RUA JK, 942",
            "cidade": "Aripuanã",
            "referencia": "Perto do campo de futebol",
            "caixa_atendimento": "AYP 04",
            "porta_ftth": "8",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Reativar Cliente na CTO\n"
                "Descrição O.S. anterior: - Solicitante: atendente Lucas\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99347-9031\n"
                "Ocorrência: Cliente solicita atendimento técnico de rotina para verificação de sinal na região atendida pela CTO local."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Ampliação ou manutenção CTO",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você identifica um cabo conectado numa porta da CTO que não corresponde a nenhum cliente cadastrado naquele ponto.",
             "pergunta": "Qual é a atitude correta?",
             "opcoes": [
                {
                    "texto": "Registrar o que encontrou (foto, localização, descrição) e reportar à central pra investigação, sem confrontar ninguém no local por conta própria",
                    "correta": True,
                    "feedback": "Correto — identificar e documentar é seu papel; investigar e confrontar formalmente é responsabilidade da central/equipe própria pra isso, não do técnico sozinho em campo.",
                },
                {
                    "texto": "Desconectar o cabo irregular da porta e deixar a CTO apenas com os clientes cadastrados, registrando a remoção no relatório do atendimento do dia",
                    "correta": False,
                    "feedback": "Parece a correção óbvia e cria dois problemas: você pode derrubar uma ligação legítima ainda não atualizada no sistema, e apaga a evidência que a investigação precisa.",
                },
                {
                    "texto": "Fotografar e reportar, e também colocar um lacre ou identificação na porta irregular, pra impedir que o cabo seja reconectado até a apuração",
                    "correta": False,
                    "feedback": "Documentar está certo, mas intervir na porta é agir sobre algo que ainda não foi apurado. Registrar e reportar já garante que a central trate o caso do jeito certo.",
                },
            ]},
            {"cena": "Enquanto você fotografa a situação pra documentar, um funcionário do comércio se aproxima perguntando o que você está fazendo.",
             "pergunta": "Como você conduz essa conversa?",
             "opcoes": [
                {
                    "texto": "Explica de forma neutra e profissional que está fazendo uma verificação de rotina na infraestrutura, sem acusar ninguém diretamente",
                    "correta": True,
                    "feedback": "Boa conduta — manter neutralidade e profissionalismo evita conflito desnecessário; acusações formais cabem à investigação da empresa, não a você no momento.",
                },
                {
                    "texto": "Explica que encontrou uma ligação fora do cadastro e pergunta se ele sabe quem fez a instalação, aproveitando que ele está ali pra apurar",
                    "correta": False,
                    "feedback": "Investigar no local coloca você num papel que não é seu e alerta quem porventura esteja envolvido. Verificação de rotina é resposta suficiente; a apuração é da central.",
                },
                {
                    "texto": "Encerra a conversa dizendo que não pode dar informações sobre o serviço e segue trabalhando sem responder mais nada ao funcionário",
                    "correta": False,
                    "feedback": "Recusar informação é razoável, mas o silêncio total desperta mais curiosidade do que uma resposta neutra. 'Verificação de rotina na infraestrutura' encerra sem criar clima.",
                },
            ]},
            {"cena": "Você conclui o registro da situação e segue com o atendimento de rotina que originalmente foi até ali fazer.",
             "pergunta": "O que fazer com as fotos e informações coletadas?",
             "opcoes": [
                {
                    "texto": "Enviar pra central pelo canal oficial de reporte, com local, data e descrição clara do que foi encontrado",
                    "correta": True,
                    "feedback": "Correto — um reporte claro e pelo canal certo garante que a central possa investigar e agir adequadamente sobre a situação.",
                },
                {
                    "texto": "Enviar pra central e também para o grupo de mensagens da equipe técnica da região, pra que os outros técnicos fiquem atentos a casos parecidos",
                    "correta": False,
                    "feedback": "Alertar a equipe parece útil, mas espalha material de uma apuração em curso por um canal que não controla registro nem acesso. O canal oficial é o que garante o tratamento certo.",
                },
                {
                    "texto": "Enviar pra central e guardar uma cópia das fotos no seu celular, como respaldo caso a documentação se perca no caminho até a investigação",
                    "correta": False,
                    "feedback": "A intenção é boa, mas guardar cópia de material de apuração no aparelho pessoal cria um risco de vazamento que não é seu pra assumir. Enviado pelo canal oficial, está registrado.",
                },
            ]},
            {"cena": "Alguns dias depois, você fica sabendo que a central investigou e identificou que era, de fato, uma ligação irregular feita por terceiros.",
             "pergunta": "O que essa situação reforça sobre o seu papel em casos assim?",
             "opcoes": [
                {
                    "texto": "Que observar, documentar com cuidado e reportar corretamente — sem tentar julgar ou resolver sozinho em campo — é a forma certa de contribuir com esse tipo de problema",
                    "correta": True,
                    "feedback": "Exatamente esse é o papel do técnico nesse tipo de situação: identificar e reportar com profissionalismo, deixando a investigação formal para quem é responsável por isso.",
                },
                {
                    "texto": "Que o registro fotográfico foi decisivo, e que vale sempre fotografar qualquer irregularidade encontrada, mesmo sem reportar em todos os casos",
                    "correta": False,
                    "feedback": "A foto ajudou porque veio acompanhada do reporte. Fotografar e guardar sem enviar não protege ninguém e ainda deixa você com material de um caso que não é seu pra tratar.",
                },
                {
                    "texto": "Que o mais importante foi ter agido rápido, e que em situações assim vale interromper o atendimento em curso pra tratar da irregularidade encontrada",
                    "correta": False,
                    "feedback": "Você documentou e seguiu com o atendimento agendado — foi o certo. Parar o serviço de um cliente pra tratar de algo que a central vai apurar em dias não acelera nada.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55835",
        "bairro": "São Cristóvão",
        "titulo": "Suporte — Dados de Cliente e Privacidade",
        "cliente": "Sra. Débora",
        "equipamento": "Nenhum — situação de atendimento",
        "briefing": "Durante o atendimento, um vizinho aparece perguntando informações sobre o plano e o valor que a Sra. Débora paga de internet.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "58329",
            "horario": "10h30",
            "assunto": "Realizar serviços - configurações",
            "endereco": "AVENIDA MARECHAL RONDON, 77",
            "cidade": "Juína",
            "referencia": "Perto da praça central",
            "caixa_atendimento": "JNA 04",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Diego\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99405-4979\n"
                "Ocorrência: Cliente (Sra. Débora) relata instabilidade na internet. Solicita verificação técnica no local."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O vizinho pergunta diretamente pra você quanto a Sra. Débora paga de mensalidade e qual é o plano dela, dizendo que também quer contratar.",
             "pergunta": "Qual é a resposta correta?",
             "opcoes": [
                {
                    "texto": "Explicar educadamente que não pode compartilhar informações de outros clientes, e orientar o vizinho a entrar em contato com a Norte Tel diretamente pra saber sobre planos disponíveis",
                    "correta": True,
                    "feedback": "Correto — informações de conta e plano de um cliente são privadas; a orientação certa é direcionar o interessado ao canal oficial de vendas.",
                },
                {
                    "texto": "Explicar que não pode falar de contrato de outro cliente e comentar apenas a faixa de preço geral dos planos residenciais oferecidos na região",
                    "correta": False,
                    "feedback": "A recusa está certa e a segunda parte a desfaz: falar de faixa de preço já é assumir papel comercial, com números que mudam por promoção. Encaminhar pra empresa é o caminho inteiro.",
                },
                {
                    "texto": "Explicar que não pode informar, e sugerir que ele converse com a própria vizinha depois, já que a informação é dela e ela pode compartilhar se quiser",
                    "correta": False,
                    "feedback": "Tecnicamente verdade, mas você acaba sugerindo ao vizinho que pressione a cliente por um dado do contrato dela. Direcionar pra Norte Tel tira ela do meio.",
                },
            ]},
            {"cena": "O vizinho insiste, dizendo que só quer 'uma ideia' do preço, sem noção exata.",
             "pergunta": "Como você mantém a resposta adequada mesmo com a insistência?",
             "opcoes": [
                {
                    "texto": "Reforça educadamente que não é a pessoa certa pra falar sobre planos e preços, e sugere que ele contate o setor comercial da Norte Tel",
                    "correta": True,
                    "feedback": "Boa conduta — mantém o limite de forma educada e ainda direciona o vizinho pra um caminho útil (contato comercial), sem comprometer a privacidade da cliente.",
                },
                {
                    "texto": "Reforça que não pode informar e explica que os valores variam bastante conforme endereço, disponibilidade e promoção vigente naquele momento",
                    "correta": False,
                    "feedback": "A explicação é verdadeira e útil, mas fica incompleta: sem indicar onde ele consegue o número certo, o vizinho continua sem caminho e provavelmente vai insistir de novo.",
                },
                {
                    "texto": "Reforça a recusa e retoma o serviço, deixando claro pelo comportamento que o assunto está encerrado e que não vai voltar a comentar sobre isso",
                    "correta": False,
                    "feedback": "Encerra o incômodo e não resolve o dele. Como ele demonstrou interesse real em contratar, indicar o setor comercial atende sem quebrar nenhuma regra.",
                },
            ]},
            {"cena": "A Sra. Débora, que ouviu parte da conversa, comenta que não se importaria de compartilhar essa informação com o vizinho dela mesma.",
             "pergunta": "Isso muda a sua conduta como técnico?",
             "opcoes": [
                {
                    "texto": "Não muda — mesmo com a cliente presente e despreocupada, o procedimento correto continua sendo direcionar esse tipo de dúvida comercial pro canal oficial da empresa",
                    "correta": True,
                    "feedback": "Correto — mesmo com boa vontade da cliente, o técnico não é o canal apropriado pra fornecer informações comerciais de conta; a orientação padrão continua sendo a mesma.",
                },
                {
                    "texto": "Muda, sim: com a titular presente e autorizando na hora, deixa de existir quebra de sigilo, e recusar passa a ser apenas burocracia desnecessária",
                    "correta": False,
                    "feedback": "Autorização verbal no meio de uma conversa não é consentimento registrado, e você não tem como comprovar depois que ela autorizou. O canal oficial existe justamente pra isso.",
                },
                {
                    "texto": "Muda parcialmente: dá pra confirmar apenas o nome do plano que ela usa, sem citar valores, já que foi ela mesma quem trouxe o assunto à tona",
                    "correta": False,
                    "feedback": "Nome do plano também é dado do contrato dela, e por ele se chega ao valor. A conduta não se divide em partes — informação de cliente sai pelo canal da empresa.",
                },
            ]},
            {"cena": "Você conclui o atendimento técnico original com a Sra. Débora, sem mais comentários sobre o assunto do vizinho.",
             "pergunta": "Isso é o encerramento adequado da situação?",
             "opcoes": [
                {
                    "texto": "Sim — o atendimento técnico foi realizado normalmente, e a questão de privacidade foi tratada corretamente ao longo da visita, sem necessidade de mais nenhuma ação",
                    "correta": True,
                    "feedback": "Correto — a situação foi conduzida de forma apropriada do início ao fim, mantendo a privacidade da cliente e orientando o vizinho pro canal certo.",
                },
                {
                    "texto": "Sim, mas vale registrar na O.S. que houve um pedido de informação sobre o contrato da cliente por parte de terceiro durante a visita técnica",
                    "correta": False,
                    "feedback": "Registrar não faz mal, mas transforma uma conversa comum de vizinho curioso em ocorrência. A pergunta foi respondida corretamente e não deixou consequência nenhuma.",
                },
                {
                    "texto": "Sim, e como o vizinho demonstrou interesse real, vale registrar o contato dele na O.S. pra que o setor comercial faça uma abordagem depois",
                    "correta": False,
                    "feedback": "Anotar contato de quem não é cliente, sem ele pedir, é usar um dado pessoal obtido de passagem. Se ele quiser contratar, o caminho é ele mesmo procurar a empresa.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55890",
        "bairro": "Bairro Panorama",
        "titulo": "Suporte — Atalho que Fura Procedimento",
        "cliente": "Múltiplos clientes (rota do dia)",
        "equipamento": "Diversos",
        "briefing": "Você está com a agenda cheia e atrasada. Um colega sugere pular a etapa de teste final de sinal em cada atendimento pra 'ganhar tempo'.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "58104",
            "horario": "17h00",
            "assunto": "Internet Lenta",
            "endereco": "RUA DOS PIONEIROS, 402",
            "cidade": "Colniza",
            "referencia": "Perto da praça central",
            "caixa_atendimento": "CNIZ 04",
            "porta_ftth": "6",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Lucas\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99652-3404\n"
                "Ocorrência: Cliente relata lentidão na internet. Solicita verificação técnica do sinal."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O colega argumenta que, na maioria das vezes, o sinal já está bom de qualquer jeito, então testar formalmente seria 'perda de tempo' num dia corrido.",
             "pergunta": "Qual é a atitude correta diante dessa sugestão?",
             "opcoes": [
                {
                    "texto": "Recusar pular a etapa de teste, já que ela existe justamente pra pegar os casos em que o sinal NÃO está bom, evitando retorno e insatisfação do cliente",
                    "correta": True,
                    "feedback": "Correto — o procedimento de teste existe exatamente pros casos excepcionais; pular ele 'porque geralmente está bom' é assumir um risco desnecessário pro cliente e pra empresa.",
                },
                {
                    "texto": "Concordar em pular o teste apenas quando a instalação for recente e o histórico daquele cliente não mostrar nenhuma ocorrência anterior de queda de sinal",
                    "correta": False,
                    "feedback": "Critério que parece razoável e falha justamente onde importa: instalação recente também tem conector mal encaixado, e histórico limpo é o de quem ainda não teve problema.",
                },
                {
                    "texto": "Manter o teste no seu atendimento e não comentar nada com o colega, já que a forma como ele conduz o próprio dia de trabalho é escolha dele",
                    "correta": False,
                    "feedback": "Respeitar a autonomia dele é justo, mas o assunto não é preferência: é procedimento que existe pra evitar retorno. Conversar sem impor é diferente de deixar passar.",
                },
            ]},
            {"cena": "Você explica ao colega por que prefere manter o procedimento completo, mesmo com a agenda apertada.",
             "pergunta": "Qual argumento é mais sólido pra essa conversa?",
             "opcoes": [
                {
                    "texto": "Um retorno por causa de sinal ruim não detectado custa muito mais tempo (e prejudica a confiança do cliente) do que os poucos minutos economizados pulando o teste",
                    "correta": True,
                    "feedback": "Esse é o argumento mais forte — a 'economia' de tempo pulando o teste é ilusória, já que um retorno futuro custaria bem mais tempo e desgaste.",
                },
                {
                    "texto": "Que o teste faz parte do procedimento oficial da empresa, e que deixar de cumprir pode gerar advertência caso a central identifique a omissão",
                    "correta": False,
                    "feedback": "É verdade e é o argumento mais fraco: transforma o teste em obediência, não em razão técnica. Quem cumpre por medo de advertência pula assim que ninguém está olhando.",
                },
                {
                    "texto": "Que sem a medição registrada não há como comprovar depois que o sinal estava bom no momento da visita, deixando o técnico sem respaldo",
                    "correta": False,
                    "feedback": "O respaldo é um bom efeito colateral, mas coloca o foco em se proteger. O motivo maior é encontrar o problema antes do cliente — o que evita o retorno e a insatisfação.",
                },
            ]},
            {"cena": "Ao final do dia, mesmo mantendo o procedimento completo, você percebe que conseguiu concluir todos os atendimentos da agenda dentro do horário.",
             "pergunta": "O que isso demonstra?",
             "opcoes": [
                {
                    "texto": "Que é possível manter a qualidade do procedimento e ainda gerenciar bem o tempo, sem precisar cortar etapas essenciais do atendimento",
                    "correta": True,
                    "feedback": "Exatamente — uma boa gestão de tempo (organização de rota, agilidade em outras partes) resolve o problema de agenda sem comprometer a qualidade técnica.",
                },
                {
                    "texto": "Que o teste toma menos tempo do que parece, e que a percepção do colega sobre a demora provavelmente estava exagerada desde o começo",
                    "correta": False,
                    "feedback": "Pode ser, mas reduzir a isso ignora o que realmente ficou provado: dá pra manter o procedimento e ainda organizar bem o dia, sem tratar as duas coisas como opostas.",
                },
                {
                    "texto": "Que a agenda daquele dia estava mais folgada que o normal, e que em dias realmente cheios talvez fosse mesmo necessário cortar alguma etapa",
                    "correta": False,
                    "feedback": "Abre a porta pro corte justamente no dia corrido, que é quando o erro custa mais caro. Se a agenda aperta, o ajuste é na agenda — não na etapa que garante o serviço.",
                },
            ]},
            {"cena": "No dia seguinte, seu colega comenta que decidiu manter o procedimento completo também, depois da conversa de vocês.",
             "pergunta": "Como você reage a essa mudança de postura do colega?",
             "opcoes": [
                {
                    "texto": "Reconhece positivamente a decisão dele, reforçando que os dois saem ganhando (cliente satisfeito, menos retorno) mantendo o procedimento correto",
                    "correta": True,
                    "feedback": "Boa atitude de equipe — reconhecer e apoiar a decisão do colega fortalece uma cultura de qualidade compartilhada entre a equipe.",
                },
                {
                    "texto": "Reconhece a decisão e aproveita pra sugerir que ele revise também outras etapas que costuma abreviar durante os atendimentos do dia",
                    "correta": False,
                    "feedback": "Ele acabou de mudar de postura por conta própria; emendar uma lista do que mais ele faz errado transforma reconhecimento em cobrança. Uma coisa de cada vez.",
                },
                {
                    "texto": "Reconhece a decisão e comenta que já esperava por isso, porque o argumento do retorno é difícil de contestar por qualquer técnico com experiência de campo",
                    "correta": False,
                    "feedback": "'Já esperava' tira o mérito da escolha dele e soa como quem venceu uma discussão. O reconhecimento funciona quando é sobre o ganho dos dois, não sobre quem tinha razão.",
                },
            ]},
        ],
    },
    {
        "id": "OS-55944",
        "bairro": "Nova Porto Velho",
        "titulo": "Suporte — Revenda Não Autorizada de Sinal",
        "cliente": "Sr. Bartolomeu",
        "equipamento": "Roteador, switch adicional não identificado",
        "briefing": "Ao investigar uma reclamação de lentidão, você percebe indícios de que o cliente está compartilhando/revendendo a conexão pra vizinhos, fora dos termos do plano contratado.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "55310",
            "horario": "09h30",
            "assunto": "Internet Lenta",
            "endereco": "RUA DAS FLORES, 630",
            "cidade": "Pimenta Bueno",
            "referencia": "Perto do campo de futebol",
            "caixa_atendimento": "PBW 04",
            "porta_ftth": "6",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Patrícia\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99889-8562\n"
                "Ocorrência: Cliente relata lentidão na internet. Solicita verificação técnica da conexão contratada."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você percebe um switch adicional não identificado conectado ao roteador, com cabos saindo em direção a casas vizinhas visíveis pela janela.",
             "pergunta": "Qual é a atitude correta nessa descoberta?",
             "opcoes": [
                {
                    "texto": "Continuar o atendimento técnico original com profissionalismo, e reportar objetivamente essa observação à central depois, sem confrontar o cliente diretamente sobre isso em campo",
                    "correta": True,
                    "feedback": "Correto — sua função em campo é o atendimento técnico; questões contratuais como essa devem ser reportadas pra central avaliar e conduzir formalmente.",
                },
                {
                    "texto": "Perguntar ao cliente, de forma leve e sem acusação, pra que serve aquele switch, já que a resposta dele ajuda a descrever melhor a situação no reporte",
                    "correta": False,
                    "feedback": "Parece só curiosidade e na prática é apuração feita por você, em campo, sem preparo nem respaldo. Além disso avisa o cliente de que a empresa reparou — o que atrapalha a verificação depois.",
                },
                {
                    "texto": "Fotografar a ligação e anexar ao relatório, deixando registrado o cabeamento encontrado antes de seguir com o reparo que motivou a visita",
                    "correta": False,
                    "feedback": "A foto é útil, mas fotografar a instalação interna do cliente sem ele saber é outro tipo de exposição. A descrição objetiva do que você viu cumpre o papel sem esse problema.",
                },
            ]},
            {"cena": "Você conclui o reparo técnico original (o motivo real da visita) normalmente, sem tocar no assunto do compartilhamento.",
             "pergunta": "Isso é apropriado, mesmo tendo notado a situação?",
             "opcoes": [
                {
                    "texto": "Sim — resolver o problema técnico pelo qual foi chamado é sua responsabilidade imediata; a questão contratual segue um fluxo separado, conduzido pela empresa depois",
                    "correta": True,
                    "feedback": "Correto — as duas coisas podem (e devem) ser tratadas separadamente: o atendimento técnico agendado, e o reporte da observação contratual pelo canal próprio.",
                },
                {
                    "texto": "Sim, mas vale concluir o reparo de forma mais rápida e simplificada que o normal, já que o cliente pode estar em situação irregular com o contrato dele",
                    "correta": False,
                    "feedback": "Enquanto a irregularidade não for confirmada, ele é um cliente como qualquer outro. Entregar um serviço pior por suspeita própria é punir alguém antes de qualquer apuração.",
                },
                {
                    "texto": "Sim, e o ideal é aproveitar o reparo pra reorganizar o cabeamento, desfazendo a ligação irregular enquanto trabalha no ponto do cliente",
                    "correta": False,
                    "feedback": "Reorganizar por conta própria é mexer no que está sendo apurado e ainda pode derrubar algo em uso. O reparo é o que foi contratado; o resto segue outro caminho.",
                },
            ]},
            {"cena": "De volta à central, você registra a observação de forma objetiva no sistema.",
             "pergunta": "Como deve ser esse registro?",
             "opcoes": [
                {
                    "texto": "Descrever objetivamente o que foi observado (switch adicional, cabos aparentemente indo pra outras residências), sem afirmar com certeza absoluta que é fraude confirmada",
                    "correta": True,
                    "feedback": "Correto — reportar a observação com precisão, deixando a confirmação e decisão formal para a investigação da empresa, é a conduta mais adequada.",
                },
                {
                    "texto": "Descrever o que foi observado e acrescentar sua conclusão de que se trata de compartilhamento irregular, pra que a central priorize a verificação",
                    "correta": False,
                    "feedback": "A descrição está certa e a conclusão é que não cabe: você viu cabos, não contratos. Se a apuração mostrar outra coisa, o registro fica com uma acusação sua que não se sustenta.",
                },
                {
                    "texto": "Descrever o que foi observado sem citar o endereço nem o nome do cliente, protegendo a identidade dele até que a central confirme ou descarte por completo a irregularidade",
                    "correta": False,
                    "feedback": "Registro sem identificação é registro que ninguém consegue verificar. O sigilo aqui é da apuração, feita internamente — omitir o endereço só inviabiliza o trabalho da central.",
                },
            ]},
            {"cena": "Semanas depois, você fica sabendo que a central confirmou a irregularidade e regularizou a situação com o cliente.",
             "pergunta": "O que essa resolução reforça sobre a forma como você agiu?",
             "opcoes": [
                {
                    "texto": "Que separar bem os papéis — atendimento técnico normal e reporte objetivo de observações contratuais — permite que cada parte faça seu trabalho corretamente",
                    "correta": True,
                    "feedback": "Exatamente esse é o valor de manter os papéis bem definidos: você fez sua parte técnica e reportou com precisão, e a empresa conduziu a investigação e resolução formal.",
                },
                {
                    "texto": "Que agir cedo foi o mais importante, e que quanto antes o técnico levanta esse tipo de suspeita, menor o prejuízo acumulado pela empresa",
                    "correta": False,
                    "feedback": "A rapidez ajudou, mas não foi o que fez a coisa funcionar. Foi a separação de papéis: sem ela, uma suspeita levantada cedo e mal conduzida atrapalha a apuração em vez de acelerar.",
                },
                {
                    "texto": "Que o reporte técnico funciona bem quando o técnico tem certeza do que encontrou, e que na dúvida é melhor não registrar nada pra não gerar acusação indevida",
                    "correta": False,
                    "feedback": "É o contrário: você registrou justamente sem ter certeza, descrevendo o que viu. Guardar a observação por falta de certeza é o que faria a irregularidade seguir sem ninguém verificar.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56001",
        "bairro": "Centro (Pimenta Bueno)",
        "titulo": "Instalação — Duplex com Duas Unidades",
        "cliente": "Irmãos Cavalcante",
        "equipamento": "2x ONT Huawei EG8145, splitter",
        "briefing": "Duas unidades residenciais (duplex) contrataram planos separados, mas compartilham a mesma entrada de fibra até o poste.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "53032",
            "horario": "16h00",
            "assunto": "Instalação de Novo Ponto",
            "endereco": "RUA RIO BRANCO, 926",
            "cidade": "Alta Floresta",
            "referencia": "Ao lado do mercadinho do bairro",
            "caixa_atendimento": "AFT 04",
            "porta_ftth": "2",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Instalação de Novo Ponto\n"
                "Descrição O.S. anterior: - Solicitante: atendente Patrícia\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99230-4392\n"
                "Ocorrência: Clientes (duplex, duas unidades) contrataram planos individuais de internet. Compartilham a mesma entrada de fibra até o poste."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Instalação, manutenção ou retirada de rede Fibra Optica",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você percebe que só existe uma entrada de fibra até a área comum do duplex, mas são dois contratos distintos, um pra cada unidade.",
             "pergunta": "Qual é a solução técnica adequada?",
             "opcoes": [
                {
                    "texto": "Usar um pequeno splitter (ou já aproveitar uma porta livre da CTO externa) pra derivar o sinal em dois cordões separados, um pra cada ONT",
                    "correta": True,
                    "feedback": "Correto — cada unidade precisa da própria ONT com sinal independente; um splitter bem dimensionado resolve compartilhar a entrada física sem misturar os planos.",
                },
                {
                    "texto": "Instalar uma ONT com duas portas PON habilitadas, atendendo os dois contratos pelo mesmo equipamento na entrada comum do duplex",
                    "correta": False,
                    "feedback": "ONT residencial tem uma única entrada óptica, e mesmo que tivesse duas, um equipamento não atende dois contratos separados. Cada unidade precisa da sua ONT com registro próprio.",
                },
                {
                    "texto": "Puxar um segundo cordão desde a CTO externa até a segunda unidade do duplex, deixando cada casa com o seu caminho óptico completamente independente",
                    "correta": False,
                    "feedback": "É a solução mais limpa quando há porta livre e passagem viável, e vale considerar. Mas quando não há, o splitter na entrada comum resolve com muito menos obra — que é o caso aqui.",
                },
            ]},
            {"cena": "Depois de instalar o splitter, você mede o sinal em cada ONT separadamente.",
             "pergunta": "Por que é importante medir as duas de forma independente, e não só uma?",
             "opcoes": [
                {
                    "texto": "Porque o splitter divide a potência óptica entre as saídas — é possível que uma unidade tenha sinal bom e a outra não, dependendo de como a divisão foi feita",
                    "correta": True,
                    "feedback": "Exato — um splitter reduz a potência em cada saída; validar as duas garante que nenhuma das duas famílias fique com sinal fora da faixa ideal.",
                },
                {
                    "texto": "Porque cada ONT pode ter sensibilidade diferente conforme o modelo, então o mesmo nível de sinal pode ser suficiente numa e insuficiente na outra",
                    "correta": False,
                    "feedback": "Modelos variam pouco nesse ponto. O motivo aqui é mais direto: o splitter reparte a luz entre as saídas, e o comprimento e o estado de cada cordão fazem cada lado chegar diferente.",
                },
                {
                    "texto": "Porque a medição individual é exigida no registro de instalações compartilhadas, com um valor de sinal por contrato ativo no mesmo ponto de entrada do imóvel atendido",
                    "correta": False,
                    "feedback": "O registro pede os dois valores mesmo, mas isso é consequência, não o motivo. Mede-se separado porque as duas saídas podem estar diferentes de verdade — inclusive uma fora da faixa.",
                },
            ]},
            {"cena": "Você confirma sinal bom nas duas ONTs, mas percebe que os dois irmãos têm uma pequena divergência sobre quem seria responsável por eventuais problemas futuros na fiação compartilhada.",
             "pergunta": "Como você lida com essa dúvida deles?",
             "opcoes": [
                {
                    "texto": "Explica tecnicamente onde fica a parte compartilhada e onde cada instalação se torna independente, e sugere que qualquer acordo sobre responsabilidade seja algo que eles combinem entre si ou verifiquem com a central",
                    "correta": True,
                    "feedback": "Boa conduta — você esclarece tecnicamente o que sabe (a parte física), mas não assume o papel de árbitro de um acordo entre os dois clientes, que é uma questão deles.",
                },
                {
                    "texto": "Explica o que é compartilhado e sugere que o irmão que mora na unidade da frente, onde fica a entrada, assuma a responsabilidade pelo trecho comum",
                    "correta": False,
                    "feedback": "Sugerir quem assume é decidir por eles um acordo que é particular. Explicar a divisão técnica é seu papel; quem cuida do trecho comum, eles combinam entre si ou com a central.",
                },
                {
                    "texto": "Explica a parte técnica e orienta que, em caso de problema no trecho comum, os dois abram chamado ao mesmo tempo pra a visita ser feita de uma vez",
                    "correta": False,
                    "feedback": "A dica é prática e cria uma regra que não existe: um chamado já traz o técnico ao trecho comum. Pedir dois chamados duplica trabalho pra resolver a mesma coisa.",
                },
            ]},
            {"cena": "Ambas as unidades testadas e funcionando corretamente, cada uma com seu próprio plano ativo.",
             "pergunta": "O que registrar de importante nessa O.S. dupla?",
             "opcoes": [
                {
                    "texto": "Que é uma instalação compartilhada por splitter na entrada comum do duplex, com os dois contratos e leituras de sinal de cada unidade registrados separadamente",
                    "correta": True,
                    "feedback": "Registro completo — deixa claro pra qualquer atendimento futuro que essa é uma instalação compartilhada fisicamente, mas com contratos e sinais independentes.",
                },
                {
                    "texto": "Que foram instaladas duas ONTs no mesmo endereço, com as leituras de sinal de cada uma e a observação de que dividem a mesma entrada de fibra",
                    "correta": False,
                    "feedback": "Está quase completo e falta o essencial: são dois contratos distintos. Sem isso, um chamado futuro pode ser tratado como se as duas unidades fossem do mesmo cliente.",
                },
                {
                    "texto": "Que houve instalação compartilhada por splitter na entrada, os dois contratos envolvidos e a leitura média de sinal obtida entre as duas unidades atendidas no endereço",
                    "correta": False,
                    "feedback": "Média não serve: ela esconde justamente o caso em que uma unidade está boa e a outra no limite. O registro precisa dos dois valores separados, um por contrato.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56058",
        "bairro": "Embratel",
        "titulo": "Suporte — Streaming Trava Mesmo com Wi-Fi Bom",
        "cliente": "Sra. Conceição",
        "equipamento": "ONT com Wi-Fi, Smart TV",
        "briefing": "Cliente reclama que os vídeos na Smart TV ficam 'carregando' toda hora, mesmo com o Wi-Fi mostrando sinal cheio.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "59371",
            "horario": "14h00",
            "assunto": "Internet Lenta",
            "endereco": "RUA DOS IPÊS, 711",
            "cidade": "Cujubim",
            "referencia": "Portão de madeira, casa de esquina",
            "caixa_atendimento": "CUJU 04",
            "porta_ftth": "8",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Lucas\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99372-3747\n"
                "Ocorrência: Cliente relata que vídeos na Smart TV ficam carregando com frequência, mesmo com sinal de Wi-Fi aparentemente cheio."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você testa a velocidade de internet na TV: o resultado mostra uma velocidade boa, compatível com o plano contratado.",
             "pergunta": "Se a velocidade está boa, o que mais pode estar causando o travamento nos vídeos?",
             "opcoes": [
                {
                    "texto": "O problema pode não ser da internet/Wi-Fi em si, mas sim do próprio serviço de streaming (app, servidor do aplicativo, ou configuração de DNS) — vale investigar separadamente antes de mexer mais na rede",
                    "correta": True,
                    "feedback": "Boa linha de raciocínio — velocidade boa no teste de rede não garante que um app específico de streaming vá funcionar perfeitamente; a causa pode estar em outra camada, fora do controle da rede local.",
                },
                {
                    "texto": "O Wi-Fi pode estar oscilando em picos curtos que o teste de velocidade não captura, e vale acompanhar a conexão da TV por alguns minutos",
                    "correta": False,
                    "feedback": "Oscilação curta existe e vale de hipótese. Mas o teste rodou justamente na TV e deu bom — antes de continuar cavando na rede, vale checar se o problema é do próprio aplicativo.",
                },
                {
                    "texto": "A TV pode estar longe do roteador e receber sinal fraco apesar do teste, o que costuma aparecer como travamento em vídeo de resolução alta",
                    "correta": False,
                    "feedback": "Sinal fraco dá esse sintoma mesmo, e seria a primeira suspeita se o teste não tivesse sido feito ali. Com velocidade boa medida na própria TV, a rede já respondeu por ela.",
                },
            ]},
            {"cena": "Você testa o mesmo aplicativo de streaming num celular conectado ao mesmo Wi-Fi, e ele funciona perfeitamente, sem travar.",
             "pergunta": "O que esse teste comparativo sugere?",
             "opcoes": [
                {
                    "texto": "Que o problema provavelmente está específico da Smart TV (app desatualizado, cache cheio, ou hardware antigo), não da internet em si",
                    "correta": True,
                    "feedback": "Exato — esse teste isola bem a causa: se funciona no celular mas não na TV, na mesma rede, o problema tende a estar no dispositivo/app da TV.",
                },
                {
                    "texto": "Que a TV está numa faixa de Wi-Fi diferente da do celular, e que passar a TV pra mesma rede do celular provavelmente resolveria o travamento",
                    "correta": False,
                    "feedback": "Se fosse faixa, o teste de velocidade na TV teria acusado. Os dois no mesmo Wi-Fi, um funcionando e outro não, apontam pro aparelho — não pro caminho até ele.",
                },
                {
                    "texto": "Que o servidor do aplicativo pode estar instável só pra alguns tipos de dispositivo, e que vale aguardar algumas horas antes de mexer em qualquer coisa",
                    "correta": False,
                    "feedback": "Instabilidade por tipo de aparelho é rara e não dá pra confirmar dali. Aguardar deixa a cliente sem solução hoje, quando o suspeito mais provável está ao alcance da mão: o app da TV.",
                },
            ]},
            {"cena": "Você sugere à Sra. Conceição atualizar o aplicativo de streaming na TV e limpar o cache dele.",
             "pergunta": "Como você orienta ela sobre isso, já que é uma Smart TV com a qual ela tem pouca familiaridade?",
             "opcoes": [
                {
                    "texto": "Faz a atualização e limpeza você mesmo, se possível, e explica de forma simples o que estava causando o travamento (app desatualizado)",
                    "correta": True,
                    "feedback": "Boa conduta de atendimento — resolver com ela ali, quando possível, e explicar em linguagem simples cria uma boa experiência, mesmo o problema não sendo estritamente da rede.",
                },
                {
                    "texto": "Orienta o passo a passo com calma pra que ela mesma faça a atualização, já que assim ela aprende e consegue repetir sozinha numa próxima vez",
                    "correta": False,
                    "feedback": "Ensinar tem valor, e com ela vale mostrar. Mas menu de Smart TV é confuso até pra quem tem prática: fazer junto, e explicar enquanto faz, entrega o resultado e o aprendizado.",
                },
                {
                    "texto": "Faz a atualização você mesmo e explica em detalhes o que é cache, versão de aplicativo e por que isso afeta a reprodução do vídeo na TV",
                    "correta": False,
                    "feedback": "Resolver por ela está certo; a explicação é que passa do ponto. Ela não precisa saber o que é cache — precisa saber que o aplicativo estava desatualizado e que isso travava o vídeo.",
                },
            ]},
            {"cena": "Depois da atualização e limpeza de cache, o streaming volta a funcionar normalmente na TV.",
             "pergunta": "O que registrar sobre esse atendimento?",
             "opcoes": [
                {
                    "texto": "Que a internet/Wi-Fi foram testados e confirmados normais, e que a causa real era o aplicativo de streaming desatualizado na Smart TV, já corrigido",
                    "correta": True,
                    "feedback": "Registro preciso — deixa claro que a rede da Norte Tel não era a causa, importante pro histórico caso a cliente entre em contato de novo sobre algo parecido.",
                },
                {
                    "texto": "Que a internet foi testada e estava normal, e que o travamento foi resolvido com ajustes realizados no aparelho de TV da cliente",
                    "correta": False,
                    "feedback": "'Ajustes no aparelho' é vago demais pra servir depois. Nomear a causa — aplicativo desatualizado — é o que permite reconhecer o mesmo caso num próximo chamado parecido.",
                },
                {
                    "texto": "Que a causa era o aplicativo de streaming desatualizado na Smart TV, já corrigido ali no local, sem necessidade de detalhar os testes de rede que foram feitos",
                    "correta": False,
                    "feedback": "A causa está certa e os testes importam: sem registrar que a rede foi medida e estava normal, um chamado futuro por lentidão começa desconfiando da internet outra vez.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56110",
        "bairro": "Caiari",
        "titulo": "Instalação — Distância Além do Limite do Cabo",
        "cliente": "Sítio Recanto Feliz",
        "equipamento": "Cabo de rede, switch, ONT",
        "briefing": "A ONT fica na sede do sítio, mas o cliente quer internet também numa área de lazer a 150 metros de distância.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "53292",
            "horario": "16h30",
            "assunto": "Serviços - Cabeamento",
            "endereco": "AVENIDA PRINCIPAL, 323",
            "cidade": "Alto Alegre",
            "referencia": "Esquina com a rua principal",
            "caixa_atendimento": "AAPC 04",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Serviços - Cabeamento\n"
                "Descrição O.S. anterior: - Solicitante: atendente Lucas\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99744-7040\n"
                "Ocorrência: Cliente solicita extensão de internet para área de lazer a aproximadamente 150 metros da sede, onde está instalada a ONT."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção de cabo drop",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O cliente pergunta se é só passar um cabo de rede comum até a área de lazer, já que ele mesmo tem um rolo de cabo em casa.",
             "pergunta": "Qual é a resposta tecnicamente correta?",
             "opcoes": [
                {
                    "texto": "Explicar que cabo de rede comum (par trançado) tem limite de 100 metros — pra 150 metros, seria necessário um switch intermediário no meio do caminho, ou uma solução de fibra/wireless ponto a ponto",
                    "correta": True,
                    "feedback": "Correto — 150 metros ultrapassa o limite padrão de 100 metros do cabo par trançado; a solução exige um ponto intermediário ou tecnologia diferente.",
                },
                {
                    "texto": "Explicar que 150 metros ultrapassa o limite do cabo comum, mas que usando cabo Cat6A com blindagem dá pra chegar nessa distância sem equipamento extra",
                    "correta": False,
                    "feedback": "Categoria melhor e blindagem melhoram a resistência a ruído, não o alcance: o limite de 100 metros vale pra todas. A distância exige equipamento no caminho ou outra tecnologia.",
                },
                {
                    "texto": "Explicar que dá pra usar cabo comum desde que a velocidade contratada seja reduzida no ponto final, já que menos velocidade tolera mais distância",
                    "correta": False,
                    "feedback": "Não existe essa troca: acima de 100 metros o sinal se degrada independentemente da velocidade negociada. O enlace fica instável ou simplesmente não sobe.",
                },
            ]},
            {"cena": "Você avalia as opções: um switch intermediário a meio caminho (exigindo energia elétrica lá), ou um link wireless ponto a ponto entre os dois pontos.",
             "pergunta": "Qual pergunta é essencial fazer ao cliente antes de decidir a melhor solução?",
             "opcoes": [
                {
                    "texto": "Se existe energia elétrica disponível no meio do caminho, e se há linha de visada livre entre os dois pontos (importante pra uma solução wireless)",
                    "correta": True,
                    "feedback": "Exatamente essas duas informações são decisivas: energia disponível favorece o switch intermediário, e linha de visada livre é essencial pra uma solução wireless ponto a ponto funcionar bem.",
                },
                {
                    "texto": "Qual a velocidade que ele espera na área de lazer, já que isso define se a solução precisa ser cabeada ou se um enlace sem fio dá conta do uso",
                    "correta": False,
                    "feedback": "A expectativa de velocidade importa pro dimensionamento, mas não é o que decide entre as opções: as duas atendem uso normal. O que decide é o que existe no terreno, energia e visada.",
                },
                {
                    "texto": "Se ele aceita a obra de passar eletroduto no percurso, já que qualquer solução cabeada nesse trecho vai exigir proteção do cabo, seja enterrado ou aéreo",
                    "correta": False,
                    "feedback": "Pergunta válida se a escolha já fosse cabeada. Mas ela pressupõe a decisão: antes disso é preciso saber se há energia no meio e se a visada está livre.",
                },
            ]},
            {"cena": "Não há energia elétrica no meio do caminho, mas existe linha de visada livre entre a sede e a área de lazer.",
             "pergunta": "Qual solução faz mais sentido nesse cenário específico?",
             "opcoes": [
                {
                    "texto": "Um link wireless ponto a ponto, que dispensa a necessidade de energia no meio do caminho e aproveita a linha de visada livre",
                    "correta": True,
                    "feedback": "Correto — dado que não há energia disponível no meio do caminho, a solução wireless ponto a ponto é mais prática nesse cenário específico.",
                },
                {
                    "texto": "Levar um cabo de energia junto com o cabo de rede até o meio do caminho, alimentando ali o switch intermediário previsto na primeira avaliação",
                    "correta": False,
                    "feedback": "Puxar rede elétrica pelo terreno é obra, custo e risco — e existe uma opção que dispensa isso por completo, já que a visada entre os dois pontos está livre.",
                },
                {
                    "texto": "Usar um switch PoE no ponto inicial, alimentando pelo próprio cabo de rede um segundo switch instalado no meio do percurso até a área de lazer",
                    "correta": False,
                    "feedback": "Boa ideia, e PoE resolve energia. Só que o trecho até o meio já teria uns 75 metros e o seguinte outros tantos — continua exigindo obra de passagem que a visada livre dispensa.",
                },
            ]},
            {"cena": "Você instala o link wireless ponto a ponto e testa a conexão na área de lazer.",
             "pergunta": "O teste mostra boa velocidade e estabilidade. O que orientar o cliente sobre a manutenção dessa solução?",
             "opcoes": [
                {
                    "texto": "Explicar que é importante manter a linha de visada livre entre os dois pontos — árvores crescendo ou novas construções no meio do caminho podem prejudicar o sinal no futuro",
                    "correta": True,
                    "feedback": "Orientação importante — soluções wireless ponto a ponto dependem da linha de visada; alertar sobre isso evita surpresas futuras pro cliente.",
                },
                {
                    "texto": "Explicar que o equipamento precisa de realinhamento periódico, já que vento e dilatação deslocam as antenas aos poucos ao longo dos meses",
                    "correta": False,
                    "feedback": "Antena bem fixada não sai de posição sozinha em uso normal. Criar rotina de realinhamento sugere fragilidade que a solução não tem, e desvia do cuidado que realmente importa.",
                },
                {
                    "texto": "Explicar que o enlace pode oscilar em dias de chuva forte e que, se isso incomodar, o caminho é migrar depois pra uma solução com fibra enterrada",
                    "correta": False,
                    "feedback": "Chuva afeta pouco nessa distância. Falar em migrar pra fibra antes mesmo de haver problema planta insegurança numa solução que foi escolhida justamente por ser a adequada.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56163",
        "bairro": "Bairro Liberdade",
        "titulo": "Suporte — Cabo Roído por Roedor",
        "cliente": "Sr. Damião",
        "equipamento": "Cabo de rede, testador de cabo",
        "briefing": "Cliente reclama de internet cabeada instável há alguns dias num ponto específico da casa, próximo ao forro.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "53738",
            "horario": "09h00",
            "assunto": "Serviços - Cabeamento",
            "endereco": "RUA JK, 863",
            "cidade": "Cacoal",
            "referencia": "Casa de dois andares, grade preta",
            "caixa_atendimento": "CWL 05",
            "porta_ftth": "5",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Serviços - Cabeamento\n"
                "Descrição O.S. anterior: - Solicitante: atendente Juliana\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99817-7759\n"
                "Ocorrência: Cliente relata instabilidade na internet cabeada em um ponto específico da casa, próximo ao forro."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção de cabo drop",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Ao inspecionar o trecho do cabo que passa pelo forro, você percebe marcas de mordida e a capa do cabo parcialmente rompida.",
             "pergunta": "O que isso indica, e qual é a atitude correta?",
             "opcoes": [
                {
                    "texto": "Provável dano causado por roedor — o trecho danificado precisa ser substituído, não apenas remendado com fita isolante",
                    "correta": True,
                    "feedback": "Correto — cabo de rede danificado por roedor compromete os pares internos; a solução adequada é substituir o trecho, não tentar um remendo superficial.",
                },
                {
                    "texto": "Emendar o trecho danificado com conector de emenda apropriado, proteger a junção com espaguete termorretrátil e testar a continuidade dos 4 pares em seguida",
                    "correta": False,
                    "feedback": "Emenda em cabo de par trançado degrada o sinal e vira um ponto fraco permanente. Além disso, onde um roedor mordeu costuma haver mais dano ao longo do trecho, escondido no forro.",
                },
                {
                    "texto": "Substituir o trecho e passar o cabo novo exatamente pela mesma rota do forro, do mesmo jeito",
                    "correta": False,
                    "feedback": "Trocar sem mudar nada devolve o cabo novo pro mesmo caminho do roedor. Substituir é metade do serviço — a outra metade é proteger a passagem (conduíte) ou mudar a rota.",
                },
            ]},
            {"cena": "Você substitui o trecho danificado por um cabo novo, refazendo a conexão.",
             "pergunta": "O que mais vale conversar com o Sr. Damião sobre essa causa específica?",
             "opcoes": [
                 {"texto": "Alertar que há indício de roedores no forro da casa, o que pode ser útil pra ele resolver na raiz (dedetização ou vedação), evitando o mesmo problema se repetir com outros cabos", "correta": True,
                  "feedback": "Boa orientação proativa — informar sobre a causa real ajuda o cliente a evitar que o mesmo problema aconteça de novo, mesmo sendo uma questão fora do seu serviço direto."},
                 {"texto": "Não comentar nada sobre a causa, só focar no reparo do cabo", "correta": False,
                  "feedback": "Vale mencionar a causa provável — é uma informação útil que pode evitar problemas futuros pro próprio cliente."},
                 {"texto": "Garantir ao cliente que isso nunca mais vai acontecer, sem nenhuma ressalva", "correta": False,
                  "feedback": "Não é possível garantir isso sem que o cliente resolva a causa raiz (presença de roedores) — melhor ser honesto sobre essa dependência."},
             ]},
            {"cena": "Depois da substituição, você testa o cabo com o testador e confirma os 4 pares funcionando corretamente.",
             "pergunta": "O que fazer antes de considerar o atendimento encerrado?",
             "opcoes": [
                {
                    "texto": "Testar a navegação real num dispositivo conectado naquele ponto, além do teste de continuidade do cabo",
                    "correta": True,
                    "feedback": "Correto — o teste de continuidade confirma o cabo fisicamente, mas testar a navegação real confirma que a experiência do cliente também está resolvida de ponta a ponta.",
                },
                {
                    "texto": "Conferir a crimpagem das duas pontas no testador mais uma vez, garantindo os 4 pares na sequência certa do padrão, e só então liberar o ponto pro cliente",
                    "correta": False,
                    "feedback": "Isso repete o teste que você já fez. Continuidade confirma que o cabo conduz, mas não que o cliente consegue navegar — falta o teste que o cliente realmente vai fazer.",
                },
                {
                    "texto": "Registrar o atendimento e orientar o cliente a avisar caso o problema volte nos próximos dias",
                    "correta": False,
                    "feedback": "Encerrar sem testar a navegação transfere pro cliente a tarefa de descobrir se deu certo. O teste leva um minuto e evita um retorno à mesma casa.",
                },
            ]},
            {"cena": "O Sr. Damião pergunta se vale a pena proteger os cabos do forro com algum tipo de conduíte pra evitar o mesmo problema.",
             "pergunta": "Como você responde?",
             "opcoes": [
                 {"texto": "Confirma que sim, um conduíte ou eletroduto protege bem contra esse tipo de dano, e é uma boa prevenção especialmente se ele já identificou sinais de roedores na casa", "correta": True,
                  "feedback": "Boa orientação — conduíte é de fato uma proteção física eficaz contra esse tipo de dano, uma recomendação prática e correta pro cenário dele."},
                 {"texto": "Diz que conduíte não faz nenhuma diferença nesse tipo de situação", "correta": False,
                  "feedback": "Faz diferença sim — um conduíte protege fisicamente o cabo contra esse tipo de dano por roedores."},
                 {"texto": "Diz que só resolve definitivamente trocando toda a fiação da casa por fibra óptica", "correta": False,
                  "feedback": "Essa seria uma solução desproporcional pro problema — um conduíte simples já resolve a proteção física necessária."},
             ]},
        ],
    },
    {
        "id": "OS-56215",
        "bairro": "Bairro Nacional",
        "titulo": "Suporte — Café Oferecido pelo Cliente",
        "cliente": "Dona Aparecida",
        "equipamento": "ONT Huawei EG8145",
        "briefing": "No meio de um atendimento tranquilo, a cliente oferece um cafezinho e um pedaço de bolo, como é comum em muitas casas.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "50566",
            "horario": "08h30",
            "assunto": "Sem Internet",
            "endereco": "RUA TIRADENTES, 790",
            "cidade": "São Miguel",
            "referencia": "Esquina com a rua principal",
            "caixa_atendimento": "SMGE 05",
            "porta_ftth": "5",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Sem Internet\n"
                "Descrição O.S. anterior: - Solicitante: atendente Patrícia\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99981-3894\n"
                "Ocorrência: Cliente sem internet. Solicita visita técnica para verificação do sinal."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Dona Aparecida oferece com carinho um café e um pedaço de bolo enquanto você termina o serviço.",
             "pergunta": "Isso é diferente de uma situação de suborno, como um pagamento extra pra priorizar atendimento?",
             "opcoes": [
                {
                    "texto": "Sim, claramente diferente — um gesto simples de hospitalidade (café, água, bolo) não tem relação com tentar comprar tratamento preferencial, e pode ser aceito com naturalidade se você quiser",
                    "correta": True,
                    "feedback": "Correto — é importante saber diferenciar: hospitalidade comum do dia a dia não é a mesma coisa que uma tentativa de pagamento por favor/prioridade, que é isso sim inadequado.",
                },
                {
                    "texto": "Sim, é diferente, mas o mais seguro é recusar mesmo assim, pra manter uma linha simples e igual em qualquer situação com qualquer cliente",
                    "correta": False,
                    "feedback": "Regra simples tem valor, e o colega da última decisão pensa assim. Mas recusar por regra confunde hospitalidade com vantagem indevida, e pode soar como desprezo ao gesto dela.",
                },
                {
                    "texto": "Sim, é diferente, desde que você registre na O.S. que recebeu um café durante a visita, deixando a transparência documentada no atendimento",
                    "correta": False,
                    "feedback": "Registrar um café transforma cortesia em ocorrência e cria um precedente estranho: nenhuma regra pede isso. O que se registra é o que afeta o serviço.",
                },
            ]},
            {"cena": "Você aceita o café com educação e agradece o gesto, continuando o atendimento normalmente.",
             "pergunta": "Isso compromete de alguma forma a qualidade ou imparcialidade do seu trabalho?",
             "opcoes": [
                {
                    "texto": "Não — aceitar um gesto simples de hospitalidade não influencia a qualidade técnica do serviço nem cria nenhuma obrigação especial com a cliente",
                    "correta": True,
                    "feedback": "Correto — o serviço continua sendo prestado com o mesmo padrão de qualidade e imparcialidade, independente do cafezinho oferecido.",
                },
                {
                    "texto": "Não compromete, mas convém encurtar a pausa e voltar logo ao serviço, pra que a cliente não interprete a conversa como parte do tempo de atendimento",
                    "correta": False,
                    "feedback": "Cuidado razoável com o tempo, e não é o ponto da pergunta. Aceitar um café não cria obrigação nem tira imparcialidade — o serviço segue no mesmo padrão de sempre.",
                },
                {
                    "texto": "Não compromete, mas seria melhor recusar em atendimentos futuros no mesmo endereço, pra não criar um vínculo pessoal com a cliente ao longo do tempo",
                    "correta": False,
                    "feedback": "Cliente recorrente e gentil não é vínculo indevido. O que se evita é vantagem em troca de tratamento — e não existe nada disso num café oferecido durante a visita.",
                },
            ]},
            {"cena": "Ao final do atendimento, Dona Aparecida comenta como foi bom ter um técnico 'gente boa' que aceitou o convite dela.",
             "pergunta": "Como você recebe esse comentário?",
             "opcoes": [
                {
                    "texto": "Agradece com simpatia genuína, reforçando que foi um prazer atender ela e que o cuidado dela foi muito gentil",
                    "correta": True,
                    "feedback": "Boa forma de encerrar — um agradecimento sincero fecha bem o atendimento, mantendo a relação cordial e profissional.",
                },
                {
                    "texto": "Agradece e aproveita pra explicar que ela pode elogiar o atendimento na pesquisa de satisfação, que costuma chegar por mensagem depois da visita",
                    "correta": False,
                    "feedback": "Informar sobre a pesquisa é normal, mas emendar isso num elogio espontâneo transforma o momento em pedido de nota. Receber bem o comentário já basta.",
                },
                {
                    "texto": "Agradece e comenta que nem todos os clientes são tão receptivos assim, o que torna a visita dela bem mais agradável do que a maioria dos atendimentos",
                    "correta": False,
                    "feedback": "Simpático na intenção e desconfortável na prática: fala mal de outros clientes pra elogiar ela. O agradecimento funciona melhor sem comparação nenhuma.",
                },
            ]},
            {"cena": "Mais tarde, um colega comenta que evita aceitar até um copo d'água dos clientes, 'por segurança', e pergunta o que você acha dessa regra pessoal dele.",
             "pergunta": "Como você reage a essa diferença de postura entre colegas?",
             "opcoes": [
                {
                    "texto": "Respeita a escolha pessoal do colega sem julgar, já que cada um pode ter seu próprio nível de conforto, desde que a linha real (suborno/vantagem indevida) seja respeitada por ambos",
                    "correta": True,
                    "feedback": "Boa postura — existe uma diferença clara entre a regra ética real (não aceitar vantagem indevida) e preferências pessoais de conforto, que podem variar de técnico pra técnico sem problema.",
                },
                {
                    "texto": "Adota a postura dele por segurança, já que uma regra mais rígida elimina qualquer chance de mal-entendido sobre aceitar coisas de clientes",
                    "correta": False,
                    "feedback": "Regra rígida por medo, sem concordar com ela, não vira critério — vira desconforto. O importante é cada um saber onde está a linha real e não ultrapassá-la.",
                },
                {
                    "texto": "Explica pra ele que recusar um copo d'água pode magoar o cliente, e sugere que ele reveja essa postura pra não parecer distante nos atendimentos",
                    "correta": False,
                    "feedback": "Você pode até pensar assim, mas transformar isso em conselho não solicitado é impor seu critério ao dele. Onde não há vantagem indevida, cabe escolha pessoal.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56268",
        "bairro": "Bairro Areal",
        "titulo": "Instalação — Cliente Pede Ponto Fora do Combinado",
        "cliente": "Sr. Anacleto",
        "equipamento": "Cabo de rede, ONT",
        "briefing": "A instalação contratada é de um ponto de internet na sala. No local, o cliente pede pra você já deixar mais dois pontos passados 'de brinde', sem custo, em outros cômodos.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "58466",
            "horario": "14h30",
            "assunto": "Instalação de Novo Ponto",
            "endereco": "RUA DA PAZ, 681",
            "cidade": "Conselvan",
            "referencia": "Perto do campo de futebol",
            "caixa_atendimento": "AYPO 05",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Instalação de Novo Ponto\n"
                "Descrição O.S. anterior: - Solicitante: atendente Lucas\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99793-8434\n"
                "Ocorrência: Cliente contratou instalação de um ponto de internet na sala."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Instalação, manutenção ou retirada de rede Fibra Optica",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O Sr. Anacleto pede, com bastante insistência simpática, pra você aproveitar que já está ali e passar mais dois pontos de rede, 'já que não ia custar nada a mais pra você'.",
             "pergunta": "Qual é a resposta correta?",
             "opcoes": [
                {
                    "texto": "Explicar com educação que o serviço contratado é o que está na O.S., e que pontos adicionais precisam ser negociados formalmente com a central, já que envolvem material e mão de obra extra",
                    "correta": True,
                    "feedback": "Correto — mesmo parecendo um pedido pequeno, alterar o escopo do serviço sem passar pelo processo formal pode gerar problemas de cobrança, material não previsto e expectativa equivocada em atendimentos futuros.",
                },
                {
                    "texto": "Explicar que não pode fazer agora e sugerir que ele mesmo compre o material, pra que numa próxima visita você já instale sem custo de mão de obra",
                    "correta": False,
                    "feedback": "Combina um serviço por fora pra depois, o que é exatamente o que a regra evita. Além disso cria expectativa de trabalho gratuito que a empresa não autorizou.",
                },
                {
                    "texto": "Fazer apenas um dos pontos extras como cortesia, já que o material sobrou da instalação e o tempo de serviço do dia comporta esse acréscimo",
                    "correta": False,
                    "feedback": "Sobra de material é da empresa, e o tempo do dia é da agenda dela. Cortesia aqui vira precedente: o próximo cliente vai ouvir de você que da outra vez deu pra fazer.",
                },
            ]},
            {"cena": "O cliente entende e pergunta como ele poderia contratar formalmente esses pontos extras.",
             "pergunta": "Como você orienta ele?",
             "opcoes": [
                {
                    "texto": "Sugere que ele entre em contato com a central comercial pra orçar e agendar a instalação dos pontos extras corretamente",
                    "correta": True,
                    "feedback": "Orientação correta — direciona o cliente pro canal certo pra atender a necessidade dele de forma organizada e registrada.",
                },
                {
                    "texto": "Explica que ele pode solicitar pelo aplicativo, onde costuma aparecer a opção de contratar serviços adicionais com o orçamento já calculado",
                    "correta": False,
                    "feedback": "Se o aplicativo não tiver essa opção, ele volta com a sensação de ter recebido informação errada. Indicar a central comercial é o caminho que você tem certeza que funciona.",
                },
                {
                    "texto": "Anota o pedido dele e diz que a própria central vai entrar em contato, sem precisar que ele procure ninguém sobre a instalação dos pontos extras",
                    "correta": False,
                    "feedback": "Sua anotação sinaliza o interesse, mas não garante ligação nenhuma. Prometer o retorno faz ele esperar em vez de procurar — e o pedido dele pode acabar não andando.",
                },
            ]},
            {"cena": "Você conclui a instalação original (o único ponto contratado) com qualidade, testando bem o sinal.",
             "pergunta": "O que registrar na O.S. sobre a conversa dos pontos extras?",
             "opcoes": [
                {
                    "texto": "Uma observação de que o cliente demonstrou interesse em pontos adicionais, sugerindo contato do comercial — sem ter executado nada fora do escopo original",
                    "correta": True,
                    "feedback": "Bom registro — documenta o interesse do cliente de forma útil pro comercial, sem misturar isso com o serviço tecnicamente contratado e executado.",
                },
                {
                    "texto": "Uma observação de que os pontos extras foram avaliados e orçados durante a visita, junto com a estimativa de material que seria necessária pra executar o serviço",
                    "correta": False,
                    "feedback": "Você não avaliou nem orçou — e não é sua atribuição. Registrar assim faz a central herdar um orçamento que não existe e que o cliente vai cobrar depois.",
                },
                {
                    "texto": "Uma observação de que o cliente pediu pontos extras e foi orientado sobre o procedimento, sem sugerir que o comercial faça contato com ele",
                    "correta": False,
                    "feedback": "Metade do valor do registro está justamente em sinalizar o interesse. Sem essa parte, a informação fica só como relato e a oportunidade morre no relatório.",
                },
            ]},
            {"cena": "Semanas depois, você é escalado pra atender justamente a instalação dos pontos extras que o Sr. Anacleto acabou contratando formalmente pelo comercial.",
             "pergunta": "Como você encara esse retorno ao mesmo cliente?",
             "opcoes": [
                {
                    "texto": "Como uma continuidade normal e positiva — o processo correto (recusar o atalho, encaminhar pro comercial) resultou numa venda registrada corretamente e um atendimento bem documentado",
                    "correta": True,
                    "feedback": "Exatamente esse é o resultado ideal — seguir o processo correto não perdeu a venda pra empresa, só garantiu que ela fosse feita de forma organizada e registrada.",
                },
                {
                    "texto": "Como uma confirmação de que valeu a pena recusar, e como uma chance de comentar com o cliente que o caminho certo acabou saindo melhor pra ele",
                    "correta": False,
                    "feedback": "O aprendizado é seu, não dele. Voltar ao assunto soa como cobrança de reconhecimento — e ele já demonstrou aceitação ao contratar pelo canal certo.",
                },
                {
                    "texto": "Como um atendimento normal, mas com atenção extra pra compensar a recusa anterior e garantir que o cliente fique satisfeito desta vez",
                    "correta": False,
                    "feedback": "Não há o que compensar: a recusa foi correta e o cliente seguiu o processo. Atenção extra por culpa é tratamento diferenciado, e o padrão de sempre já atende bem.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56320",
        "bairro": "Bairro Redenção",
        "titulo": "Suporte — Roteador com Firmware Desatualizado",
        "cliente": "Sr. Hélio",
        "equipamento": "Roteador doméstico com anos de uso",
        "briefing": "Durante um atendimento de rotina, você percebe que o roteador do cliente nunca recebeu uma atualização de firmware, algo comum quando o cliente nunca mexeu nisso.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "52336",
            "horario": "15h00",
            "assunto": "Realizar serviços - configurações",
            "endereco": "RUA JK, 32",
            "cidade": "Aripuanã",
            "referencia": "Esquina com a rua principal",
            "caixa_atendimento": "AYP 05",
            "porta_ftth": "1",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Aline\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99212-6758\n"
                "Ocorrência: Cliente solicita atendimento técnico de rotina para verificação geral do equipamento."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você verifica no painel do roteador: a versão do firmware é de vários anos atrás, bem desatualizada.",
             "pergunta": "Por que isso é relevante, além de possíveis melhorias de desempenho?",
             "opcoes": [
                {
                    "texto": "Firmware desatualizado pode ter vulnerabilidades de segurança conhecidas já corrigidas em versões mais novas, deixando a rede do cliente mais exposta",
                    "correta": True,
                    "feedback": "Exatamente — segurança é um motivo tão importante quanto desempenho pra manter o firmware atualizado; falhas antigas conhecidas podem ser exploradas em equipamentos desatualizados.",
                },
                {
                    "texto": "Firmware antigo pode não reconhecer aparelhos lançados depois dele, o que faz celulares e TVs mais novas terem dificuldade pra se conectar naquela rede",
                    "correta": False,
                    "feedback": "Compatibilidade com aparelho novo raramente depende do firmware do roteador — o Wi-Fi é padronizado justamente pra isso. O risco real que se corrige atualizando é de segurança.",
                },
                {
                    "texto": "Firmware antigo costuma limitar a velocidade máxima que o roteador entrega, então o cliente pode estar recebendo menos do que o plano contratado",
                    "correta": False,
                    "feedback": "Se houvesse esse limite ele apareceria no teste de velocidade, e não é o padrão. Versão velha traz principalmente falhas de segurança já conhecidas e corrigidas nas versões novas.",
                },
            ]},
            {"cena": "Você pergunta ao Sr. Hélio se ele autoriza a atualização, explicando rapidamente o motivo.",
             "pergunta": "Por que pedir autorização antes de atualizar, já que parece uma melhoria óbvia?",
             "opcoes": [
                {
                    "texto": "Porque a atualização pode reiniciar o roteador e interromper a internet por alguns minutos, então é importante o cliente estar ciente antes, especialmente se ele estiver em algo importante no momento",
                    "correta": True,
                    "feedback": "Boa prática de comunicação — mesmo sendo uma melhoria técnica, avisar sobre uma interrupção temporária evita surpresa desagradável pro cliente.",
                },
                {
                    "texto": "Porque se a atualização falhar no meio o roteador pode parar de funcionar, e o cliente precisa ter concordado antes com esse risco de perda do equipamento",
                    "correta": False,
                    "feedback": "O risco de travar existe e é pequeno; falar nele como principal motivo assusta o cliente e faz ele recusar uma atualização que deveria acontecer. O ponto é a interrupção momentânea.",
                },
                {
                    "texto": "Porque a atualização pode apagar as configurações personalizadas, e o cliente precisa autorizar a perda da senha e do nome de rede que ele escolheu",
                    "correta": False,
                    "feedback": "Atualização de firmware normalmente preserva a configuração — reset é outra coisa. Anunciar perda de senha cria uma expectativa errada e ainda faz parecer que o serviço é arriscado.",
                },
            ]},
            {"cena": "Com autorização do cliente, você atualiza o firmware. O processo demora alguns minutos e o roteador reinicia sozinho ao final.",
             "pergunta": "O que fazer depois que o roteador volta a funcionar?",
             "opcoes": [
                {
                    "texto": "Confirmar que a rede Wi-Fi voltou normalmente (nome e senha preservados) e que a internet está navegando, já que atualizações às vezes podem alterar pequenas configurações",
                    "correta": True,
                    "feedback": "Correto — sempre vale confirmar que tudo voltou ao normal depois de uma atualização, garantindo que a experiência do cliente não foi afetada negativamente.",
                },
                {
                    "texto": "Rodar um teste de velocidade pra comparar com o resultado anterior e comprovar ao cliente o ganho de desempenho que foi trazido pela nova versão do firmware",
                    "correta": False,
                    "feedback": "Pode não haver ganho nenhum de velocidade, e prometer comparação transforma uma atualização de segurança em promessa de desempenho que o número não vai confirmar.",
                },
                {
                    "texto": "Conferir no painel se a versão nova foi realmente aplicada e anotar o número dela na O.S., encerrando o atendimento assim que a confirmação aparecer na tela",
                    "correta": False,
                    "feedback": "Confirmar a versão é bom registro e não basta: o painel pode mostrar a versão nova com o Wi-Fi da casa fora do ar. Quem valida é a rede funcionando e a navegação.",
                },
            ]},
            {"cena": "O Sr. Hélio pergunta se vai precisar fazer isso de novo no futuro, ou se agora está resolvido pra sempre.",
             "pergunta": "Como você responde com honestidade?",
             "opcoes": [
                {
                    "texto": "Explica que atualizações de firmware são periódicas (não um evento único), e sugere que ele mesmo pode verificar de vez em quando pelo app/painel do roteador, ou pedir suporte se tiver dúvida",
                    "correta": True,
                    "feedback": "Resposta honesta e educativa — ajuda o cliente a entender que é uma manutenção contínua, não uma solução definitiva de uma vez só.",
                },
                {
                    "texto": "Explica que o próprio roteador costuma se atualizar sozinho quando há versão nova, e que ele não precisa se preocupar mais com esse assunto",
                    "correta": False,
                    "feedback": "Muitos modelos até têm atualização automática, mas nem todos, e nem sempre ativada. Dizer que não precisa se preocupar deixa o cliente com a mesma versão velha daqui a três anos.",
                },
                {
                    "texto": "Explica que atualizações aparecem de tempos em tempos e orienta que ele ligue pro suporte a cada seis meses pra pedir uma verificação da versão do firmware do roteador",
                    "correta": False,
                    "feedback": "Criar rotina de chamado semestral gera trabalho pra todo mundo por algo que ele resolve olhando o painel. Vale ensinar a conferir, e deixar o suporte pra quando surgir dúvida.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56374",
        "bairro": "Bairro Nacional",
        "titulo": "Instalação — Trabalho em Forro Muito Quente",
        "cliente": "Sr. Isaías",
        "equipamento": "Cabo de rede, ferramentas de instalação",
        "briefing": "É preciso passar um cabo pelo forro da casa, num dia de calor intenso, num telhado de fibrocimento sem isolamento.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "52019",
            "horario": "08h00",
            "assunto": "Serviços - Cabeamento",
            "endereco": "RUA DOS IPÊS, 244",
            "cidade": "Juína",
            "referencia": "Ao lado da oficina mecânica",
            "caixa_atendimento": "JNA 05",
            "porta_ftth": "6",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Serviços - Cabeamento\n"
                "Descrição O.S. anterior: - Solicitante: atendente Juliana\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99172-4534\n"
                "Ocorrência: Cliente contratou serviço de cabeamento com passagem de cabo pelo forro do imóvel."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção de cabo drop",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Ao subir no forro pra verificar a rota do cabo, você percebe que a temperatura ali dentro está extremamente elevada, bem mais quente que o resto da casa.",
             "pergunta": "Qual é a atitude correta diante dessa condição?",
             "opcoes": [
                {
                    "texto": "Trabalhar por períodos curtos, com pausas regulares pra se hidratar e recuperar, evitando ficar tempo excessivo exposto ao calor extremo de uma vez",
                    "correta": True,
                    "feedback": "Correto — calor extremo em espaços confinados como forro pode causar mal-estar sério; trabalhar em intervalos curtos com hidratação é uma prática de segurança importante.",
                },
                {
                    "texto": "Levar uma garrafa de água pro forro e trabalhar direto até terminar, evitando as subidas e descidas, que também cansam e tomam bastante tempo do serviço",
                    "correta": False,
                    "feedback": "Água ajuda e não resolve: o corpo continua acumulando calor em ambiente fechado a essa temperatura. As pausas existem justamente pra o organismo se recuperar, não só pra beber.",
                },
                {
                    "texto": "Adiar a parte do forro pro fim da tarde, quando a temperatura baixa, e adiantar o restante do serviço enquanto o telhado ainda está quente",
                    "correta": False,
                    "feedback": "Boa ideia quando a agenda permite, e vale considerar. Mas nem sempre dá pra esticar o atendimento por horas — trabalhar em ciclos curtos resolve dentro do horário previsto.",
                },
            ]},
            {"cena": "Depois de uma pausa pra se hidratar, você volta ao forro pra continuar o trabalho.",
             "pergunta": "Qual outro cuidado é importante nesse ambiente, além da temperatura?",
             "opcoes": [
                {
                    "texto": "Cuidado ao se apoiar apenas nas vigas estruturais (não no forro/gesso em si, que pode não suportar peso), pra evitar acidente de queda",
                    "correta": True,
                    "feedback": "Isso é essencial — um erro comum e perigoso é pisar em áreas do forro que não são estruturalmente resistentes, causando quedas sérias.",
                },
                {
                    "texto": "Usar máscara contra poeira, já que forro costuma acumular bastante sujeira fina que fica suspensa no ar quando alguém se movimenta lá em cima",
                    "correta": False,
                    "feedback": "Máscara é recomendável e vale levar. Mas poeira incomoda, enquanto pisar fora da viga derruba a pessoa forro abaixo — o cuidado que evita acidente grave vem primeiro.",
                },
                {
                    "texto": "Levar uma lanterna de cabeça pra manter as duas mãos livres, já que iluminar com o celular numa das mãos aumenta o risco de desequilíbrio",
                    "correta": False,
                    "feedback": "Iluminação com as mãos livres é boa prática e ajuda muito ali. Ainda assim, o que decide se você cai ou não é onde pisa: apoio só nas vigas estruturais, nunca no gesso.",
                },
            ]},
            {"cena": "Você conclui a passagem do cabo com segurança, tendo feito pausas regulares durante o trabalho.",
             "pergunta": "O que comentar com o Sr. Isaías sobre a experiência no forro?",
             "opcoes": [
                {
                    "texto": "Comentar de forma profissional que o forro está bem quente, e que isso é algo a se considerar caso ele mesmo (ou outro prestador de serviço) precise subir lá no futuro",
                    "correta": True,
                    "feedback": "Boa orientação — compartilhar essa observação prática pode ajudar o cliente a se planejar melhor em futuras necessidades de acesso ao forro.",
                },
                {
                    "texto": "Comentar que o forro estava muito quente e sugerir que ele avalie instalar alguma ventilação ou manta térmica no telhado, pra melhorar bastante a condição térmica do imóvel",
                    "correta": False,
                    "feedback": "Vira recomendação de obra que não é da sua área e que ele não pediu. Informar a condição do local é útil; indicar reforma no telhado passa do ponto do atendimento.",
                },
                {
                    "texto": "Não comentar nada pra não parecer reclamação, já que o serviço foi concluído normalmente e a condição do forro é do imóvel dele, não da instalação feita",
                    "correta": False,
                    "feedback": "Comentar de forma profissional não é reclamar: é informação útil pra ele e pra quem for subir ali depois. Silenciar guarda um dado que não custa nada compartilhar.",
                },
            ]},
            {"cena": "Antes de ir embora, você registra o atendimento no sistema.",
             "pergunta": "Vale mencionar a condição do local (calor extremo no forro) no registro interno?",
             "opcoes": [
                {
                    "texto": "Sim — essa informação pode ser útil pra um próximo técnico que precisar acessar o mesmo local, ajudando ele a se planejar melhor (horário, hidratação, tempo estimado)",
                    "correta": True,
                    "feedback": "Boa prática — compartilhar condições especiais de um endereço ajuda toda a equipe em atendimentos futuros no mesmo local.",
                },
                {
                    "texto": "Sim, mas apenas se a condição tiver de fato atrapalhado o serviço ou causado algum atraso, já que o registro técnico documenta apenas o que afeta a execução do trabalho",
                    "correta": False,
                    "feedback": "O calor não atrasou nada justamente porque você se organizou — e é essa informação que ajuda o próximo. Condicionar o registro ao prejuízo faz perder o que serve de preparo.",
                },
                {
                    "texto": "Sim, e vale sugerir no mesmo registro que os atendimentos futuros nesse endereço sejam agendados sempre de manhã bem cedo, quando o forro ainda está fresco",
                    "correta": False,
                    "feedback": "A observação é boa; virar regra de agendamento é demais pra uma condição comum em forro. Registre o fato e deixe quem for atender decidir como se organiza.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56428",
        "bairro": "Centro (Ji-Paraná)",
        "titulo": "Instalação — Organização de Rack Comercial",
        "cliente": "Auto Peças Trevo",
        "equipamento": "Rack, switch, patch panel, velcros e abraçadeiras",
        "briefing": "Instalação de rede numa loja de autopeças, com um rack pequeno que vai abrigar switch e patch panel.",
        "instrumento": "cable",
        "os_info": {
            "id_cliente": "54091",
            "horario": "09h00",
            "assunto": "Serviços - Cabeamento",
            "endereco": "RUA RIO BRANCO, 845",
            "cidade": "Colniza",
            "referencia": "Esquina com a rua principal",
            "caixa_atendimento": "CNIZ 05",
            "porta_ftth": "3",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Serviços - Cabeamento\n"
                "Descrição O.S. anterior: - Solicitante: atendente Fernanda\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99803-1328\n"
                "Ocorrência: Cliente (loja de autopeças) contratou instalação de rede com organização de rack para switch e patch panel."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção de cabo drop",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você está organizando os cabos dentro do rack e tem à disposição tanto velcro reutilizável quanto abraçadeiras plásticas descartáveis.",
             "pergunta": "Qual é a prática mais recomendada pra organizar os cabos dentro do rack?",
             "opcoes": [
                {
                    "texto": "Usar velcro reutilizável na maior parte da organização, reservando abraçadeiras plásticas só onde for realmente necessário — velcro permite reorganizar no futuro sem cortar nada",
                    "correta": True,
                    "feedback": "Boa prática — velcro é mais flexível pra manutenções futuras (você pode abrir e reorganizar sem descartar), enquanto abraçadeira plástica precisa ser cortada e substituída toda vez.",
                },
                {
                    "texto": "Usar abraçadeira plástica em tudo, mas deixando folga proposital em cada amarração pra permitir mexer nos cabos sem precisar cortar nada depois",
                    "correta": False,
                    "feedback": "Folga ajuda no aperto e não resolve a reorganização: pra tirar ou acrescentar um cabo você corta a abraçadeira do mesmo jeito. Velcro abre e fecha quantas vezes precisar.",
                },
                {
                    "texto": "Usar velcro em tudo, sem exceção, já que abraçadeira plástica não tem vantagem nenhuma dentro de um rack organizado e etiquetado corretamente",
                    "correta": False,
                    "feedback": "Velcro é a melhor escolha na maior parte, mas há pontos em que uma fixação definitiva é justamente o que se quer — a plástica continua tendo lugar, só que não em tudo.",
                },
            ]},
            {"cena": "Ao prender os cabos com velcro, você presta atenção especial pra não apertar demais.",
             "pergunta": "Por que isso é importante, mesmo usando velcro (que é mais macio que abraçadeira plástica)?",
             "opcoes": [
                {
                    "texto": "Apertar demais qualquer tipo de amarração pode deformar os cabos internamente, afetando a qualidade do sinal, especialmente em cabos de rede com pares trançados",
                    "correta": True,
                    "feedback": "Correto — mesmo com velcro, um aperto excessivo pode comprimir os pares internos do cabo, degradando a qualidade da transmissão de dados.",
                },
                {
                    "texto": "Porque a compressão excessiva aquece os cabos no ponto amarrado, e o calor acumulado ao longo do tempo acaba ressecando a capa externa deles",
                    "correta": False,
                    "feedback": "Cabo de rede não esquenta a ponto de ressecar por amarração. O problema é mecânico e imediato: a pressão deforma os pares trançados, e é isso que degrada o sinal.",
                },
                {
                    "texto": "Porque o velcro apertado demais pode marcar a capa do cabo, deixando um vinco permanente que atrapalha identificar aquele cabo específico em manutenções futuras no rack",
                    "correta": False,
                    "feedback": "A marca até aparece, mas é o menor dos problemas. O que importa é que a deformação atinge os pares por dentro, e o efeito disso é perda de desempenho no enlace.",
                },
            ]},
            {"cena": "Rack organizado, com cabos etiquetados e presos adequadamente. O dono da loja pergunta se essa organização toda 'vale a pena' pra uma loja pequena como a dele.",
             "pergunta": "Como você responde?",
             "opcoes": [
                {
                    "texto": "Explica que a organização facilita qualquer manutenção futura e reduz o tempo (e custo) de um eventual atendimento técnico, independente do tamanho da loja",
                    "correta": True,
                    "feedback": "Boa explicação — o benefício da organização não depende do tamanho do negócio, é sobre facilitar qualquer manutenção futura, seja numa loja pequena ou grande.",
                },
                {
                    "texto": "Explica que a organização é parte do padrão de instalação da empresa, e que todo rack entregue pela Norte Tel sai assim, independente do porte do cliente",
                    "correta": False,
                    "feedback": "É verdade e responde pelo lado errado: transforma em regra da empresa algo que traz benefício direto pra ele. O ganho é dele — manutenção mais rápida e mais barata.",
                },
                {
                    "texto": "Explica que a organização evita que os cabos se soltem sozinhos com a vibração dos equipamentos, o que é a causa mais comum de queda de rede dentro de um rack",
                    "correta": False,
                    "feedback": "Cabo não se solta sozinho por vibração num rack de loja. A vantagem real é outra: quando algo dá problema, achar o cabo certo leva minutos em vez de meia hora.",
                },
            ]},
            {"cena": "Antes de encerrar, você tira uma foto do rack organizado e etiquetado.",
             "pergunta": "Qual é o propósito dessa foto?",
             "opcoes": [
                {
                    "texto": "Documentar o estado da instalação recém concluída, útil como referência pra qualquer atendimento futuro nesse mesmo rack",
                    "correta": True,
                    "feedback": "Boa prática — uma foto de referência ajuda muito um próximo técnico (ou você mesmo) a entender rapidamente a organização em uma visita futura.",
                },
                {
                    "texto": "Comprovar pro cliente que o serviço foi executado com capricho, servindo de respaldo caso ele questione depois a qualidade da instalação entregue",
                    "correta": False,
                    "feedback": "Respaldo é efeito colateral. A foto vale principalmente pra quem for mexer nesse rack no futuro: ela mostra o estado original e o que estava em cada porta.",
                },
                {
                    "texto": "Registrar o antes e o depois da organização pra usar como exemplo em treinamentos internos e mostrar a outros clientes a qualidade do serviço",
                    "correta": False,
                    "feedback": "Usar a instalação de um cliente como material de divulgação exige autorização dele. A foto tem função técnica: referência pro próximo atendimento naquele rack.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56482",
        "bairro": "Costa e Silva",
        "titulo": "Suporte — Cliente Ausente no Horário Agendado",
        "cliente": "Sr. Otacílio",
        "equipamento": "Nenhum — situação de atendimento",
        "briefing": "Você chega no horário agendado, mas ninguém atende a casa. Você liga pro cliente, que esqueceu completamente do agendamento.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "55143",
            "horario": "09h00",
            "assunto": "Instalação de Novo Ponto",
            "endereco": "RUA DAS FLORES, 377",
            "cidade": "Pimenta Bueno",
            "referencia": "Portão de madeira, casa de esquina",
            "caixa_atendimento": "PBW 05",
            "porta_ftth": "7",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Instalação de Novo Ponto\n"
                "Descrição O.S. anterior: - Solicitante: atendente Aline\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99844-3208\n"
                "Ocorrência: Cliente contratou instalação de novo ponto de internet no imóvel. Atendimento agendado previamente."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Instalação, manutenção ou retirada de rede Fibra Optica",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Depois de tocar a campainha algumas vezes sem resposta, você liga pro celular do Sr. Otacílio, que atende meio sonolento, claramente tendo esquecido do horário.",
             "pergunta": "Qual é a atitude profissional correta?",
             "opcoes": [
                {
                    "texto": "Explicar com educação que você está no local no horário combinado, e perguntar se ele consegue chegar em poucos minutos ou se prefere reagendar",
                    "correta": True,
                    "feedback": "Boa conduta — comunicação clara e sem drama, oferecendo opções práticas pro cliente resolver a situação da forma mais conveniente pra ele.",
                },
                {
                    "texto": "Aguardar cerca de quinze minutos no local antes de qualquer contato, já que atraso curto é comum e o cliente pode estar chegando na rua agora",
                    "correta": False,
                    "feedback": "Esperar sem ligar gasta o mesmo tempo e não traz informação nenhuma. Uma ligação em trinta segundos já diz se ele está a caminho ou se o melhor é reagendar.",
                },
                {
                    "texto": "Ligar pra central relatando ausência do cliente no endereço e seguir para o próximo atendimento, deixando o reagendamento por conta do setor responsável",
                    "correta": False,
                    "feedback": "Registrar a ausência faz parte, mas pular direto pra central ignora o mais simples: o cliente pode estar a cinco minutos dali. Falar com ele primeiro costuma salvar a visita.",
                },
            ]},
            {"cena": "O Sr. Otacílio pede desculpas e diz que consegue chegar em 15 minutos.",
             "pergunta": "Como você gerencia essa espera considerando o resto da sua agenda do dia?",
             "opcoes": [
                {
                    "texto": "Aceita esperar os 15 minutos (um tempo razoável), e se isso puder atrasar o próximo atendimento, avisa a central ou o próximo cliente com antecedência",
                    "correta": True,
                    "feedback": "Boa gestão — 15 minutos é um tempo razoável de espera, e comunicar proativamente um possível atraso no próximo compromisso evita um efeito cascata de insatisfação.",
                },
                {
                    "texto": "Aceita esperar e usa o tempo pra adiantar o que for possível do serviço na parte externa do imóvel, ganhando tempo enquanto o cliente não chega",
                    "correta": False,
                    "feedback": "Adiantar parece produtivo e é arriscado: sem o morador presente você estaria trabalhando no imóvel dele sem autorização de quem responde pelo local.",
                },
                {
                    "texto": "Aceita esperar os quinze minutos combinados e, se ele não chegar nesse prazo, encerra a visita como ausência e segue direto pro próximo atendimento da agenda",
                    "correta": False,
                    "feedback": "Esperar está certo e falta a parte que protege o resto do dia: se a espera comprometer o próximo horário, alguém precisa ser avisado antes, não depois do atraso acontecer.",
                },
            ]},
            {"cena": "O Sr. Otacílio chega em 12 minutos, agradecendo bastante a paciência.",
             "pergunta": "Como você conduz o restante do atendimento a partir daí?",
             "opcoes": [
                {
                    "texto": "Segue normalmente com o atendimento, sem fazer o cliente se sentir mal pelo esquecimento, mantendo o profissionalismo de sempre",
                    "correta": True,
                    "feedback": "Boa conduta — o incidente já foi resolvido com a chegada dele; não há necessidade de prolongar o desconforto, o atendimento deve seguir normalmente.",
                },
                {
                    "texto": "Segue com o atendimento e comenta de forma leve que o atraso apertou a agenda, pra que ele tenha noção do impacto e evite repetir numa próxima visita",
                    "correta": False,
                    "feedback": "Mesmo em tom leve, é cobrança — e ele já se desculpou espontaneamente. Se o atraso teve impacto real, isso vai pro registro; o cliente não precisa carregar isso na visita.",
                },
                {
                    "texto": "Segue com o atendimento de forma mais rápida que o habitual, pra recuperar o tempo perdido e conseguir chegar no horário do próximo cliente",
                    "correta": False,
                    "feedback": "Correr pra compensar transfere a conta do atraso pra qualidade do serviço dele. O ajuste é na agenda, avisando quem for afetado — não em entregar menos aqui.",
                },
            ]},
            {"cena": "Atendimento concluído normalmente, já mais tarde do que o previsto originalmente.",
             "pergunta": "O que registrar sobre esse atraso na O.S.?",
             "opcoes": [
                {
                    "texto": "Registrar objetivamente que houve atraso porque o cliente não estava no local no horário agendado, sem tom de crítica",
                    "correta": True,
                    "feedback": "Bom registro — factual e objetivo, ajuda a explicar eventuais atrasos em cascata na agenda do dia sem julgar o cliente.",
                },
                {
                    "texto": "Registrar o horário real de início e de conclusão do serviço, sem entrar no motivo, já que o importante pra O.S. é o tempo efetivo de execução",
                    "correta": False,
                    "feedback": "Os horários sozinhos sugerem que você demorou. Sem o motivo, um atraso que não foi seu aparece no relatório como se fosse — e é justamente isso que o registro deve evitar.",
                },
                {
                    "texto": "Registrar que houve atraso por ausência do cliente e sugerir que a central confirme presença por telefone antes das próximas visitas nesse endereço",
                    "correta": False,
                    "feedback": "O fato basta. Sugerir confirmação prévia cria procedimento pro endereço a partir de um esquecimento pontual, o que soa como punição a um cliente que se desculpou.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56536",
        "bairro": "Bairro Liberdade",
        "titulo": "Suporte — Verificação Pós-Tempestade",
        "cliente": "Vários clientes da rua",
        "equipamento": "Medidor óptico, kit de limpeza de fibra",
        "briefing": "Depois de uma tempestade forte na região, vários clientes da mesma rua reportaram instabilidade na internet.",
        "instrumento": "optic",
        "os_info": {
            "id_cliente": "51649",
            "horario": "13h30",
            "assunto": "Sem Internet",
            "endereco": "RUA TIRADENTES, 402",
            "cidade": "Alta Floresta",
            "referencia": "Ponto branco com azul, casa nos fundos",
            "caixa_atendimento": "AFT 05",
            "porta_ftth": "4",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Sem Internet\n"
                "Descrição O.S. anterior: - Solicitante: atendente Camila\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99399-6811\n"
                "Ocorrência: Cliente relata instabilidade na internet após tempestade forte na região. Outros clientes da mesma rua reportaram o mesmo problema."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Ampliação ou manutenção CTO",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Você chega na CTO que atende essa rua e percebe água acumulada dentro da caixa, provavelmente entrada por uma vedação danificada.",
             "pergunta": "Qual é o primeiro cuidado a tomar?",
             "opcoes": [
                {
                    "texto": "Avaliar com cuidado antes de mexer, verificando se há algum risco (ex: umidade em conectores) antes de manusear, e secar/limpar adequadamente antes de testar qualquer sinal",
                    "correta": True,
                    "feedback": "Correto — água numa CTO pode afetar conectores e causar mau contato; a prioridade é avaliar e resolver essa condição antes de qualquer outro diagnóstico.",
                },
                {
                    "texto": "Escoar a água e secar tudo rapidamente com um pano, pra poder testar o sinal e descobrir logo se a umidade chegou a afetar as conexões dentro da caixa",
                    "correta": False,
                    "feedback": "Secar é necessário mesmo, mas a pressa aqui atrapalha: manusear conector úmido espalha a umidade pra dentro do ferrolho. Avaliar antes de mexer evita transformar um problema em dois.",
                },
                {
                    "texto": "Fotografar a água acumulada e reportar à central antes de qualquer intervenção, já que uma caixa alagada indica falha de instalação que precisa ser apurada",
                    "correta": False,
                    "feedback": "Documentar é útil e vai acontecer. Mas há clientes sem internet agora, e a limpeza cuidadosa resolve hoje — o reporte da vedação segue em paralelo, não no lugar do reparo.",
                },
            ]},
            {"cena": "Depois de secar a caixa e limpar os conectores afetados pela umidade, você mede o sinal em algumas portas da CTO.",
             "pergunta": "Por que testar mais de uma porta, já que o problema parece ser geral na caixa?",
             "opcoes": [
                {
                    "texto": "Porque diferentes portas podem ter sido afetadas de forma diferente pela umidade, então testar várias ajuda a confirmar que a correção resolveu de forma abrangente, não só num ponto isolado",
                    "correta": True,
                    "feedback": "Correto — mesmo com uma causa comum (a água), o efeito pode variar entre as portas; testar várias garante uma correção mais completa antes de considerar resolvido.",
                },
                {
                    "texto": "Porque o medidor pode acusar valor bom numa porta e ruim na seguinte se o cordão estiver mal encaixado, o que é comum depois de manusear a caixa",
                    "correta": False,
                    "feedback": "Encaixe frouxo depois do manuseio é risco real e vale conferir. Mas o motivo de testar várias é anterior a isso: a umidade não atinge todos os conectores igualmente.",
                },
                {
                    "texto": "Porque cada cliente da caixa tem um plano diferente, e a faixa de sinal aceitável muda conforme a velocidade contratada por cada um deles",
                    "correta": False,
                    "feedback": "A faixa aceitável é do equipamento e não muda com o plano. Testa-se mais de uma porta porque a água pode ter afetado umas e poupado outras dentro da mesma caixa.",
                },
            ]},
            {"cena": "Sinal confirmado bom em todas as portas testadas depois da limpeza. Você identifica que a vedação da CTO estava realmente comprometida, permitindo entrada de água.",
             "pergunta": "O que fazer em relação à vedação danificada, além da limpeza já feita?",
             "opcoes": [
                {
                    "texto": "Reportar a necessidade de substituição ou reparo da vedação da CTO pra central, já que o problema provavelmente vai se repetir na próxima chuva forte se não for corrigido definitivamente",
                    "correta": True,
                    "feedback": "Correto — uma limpeza pontual resolve o sintoma imediato, mas reportar a causa raiz (vedação danificada) evita que o mesmo problema se repita na próxima tempestade.",
                },
                {
                    "texto": "Substituir a vedação você mesmo com o material de reserva da van, deixando a caixa fechada corretamente antes de sair do local nesta visita",
                    "correta": False,
                    "feedback": "Se você tem a peça certa e é procedimento seu, ótimo. O cuidado é não improvisar peça que não é da caixa: vedação errada dá sensação de resolvido e volta a entrar água.",
                },
                {
                    "texto": "Registrar a vedação danificada no relatório do atendimento, sem abrir um reporte específico, já que a central acaba lendo os relatórios das O.S. da região",
                    "correta": False,
                    "feedback": "Relatório de O.S. é lido no contexto daquele chamado e some no meio dos outros. Um problema de infraestrutura que vai atingir a rua inteira precisa de reporte próprio.",
                },
            ]},
            {"cena": "Você liga pra alguns dos clientes que reportaram problema, confirmando que já está tudo normalizado.",
             "pergunta": "Isso é um passo importante, mesmo já tendo corrigido tecnicamente o problema?",
             "opcoes": [
                {
                    "texto": "Sim — confirmar diretamente com os clientes fecha o ciclo de atendimento com transparência, e permite identificar rapidamente se algum ainda sente instabilidade por outro motivo",
                    "correta": True,
                    "feedback": "Boa prática de atendimento proativo — fechar o ciclo com os clientes afetados demonstra cuidado e permite capturar rapidamente qualquer problema remanescente.",
                },
                {
                    "texto": "Sim, mas basta ligar pro cliente que abriu o primeiro chamado, já que os demais foram afetados pelo mesmo problema e a correção foi a mesma",
                    "correta": False,
                    "feedback": "A correção foi a mesma, a experiência de cada um não. Cada porta estava num estado diferente, e é justamente ligando pros outros que você descobre se sobrou alguém instável.",
                },
                {
                    "texto": "Sim, e vale aproveitar a ligação pra explicar tecnicamente o que houve dentro da caixa e o que foi feito, pra que eles entendam bem a causa da interrupção",
                    "correta": False,
                    "feedback": "Explicar em linhas gerais é bom. Detalhar o problema de infraestrutura pode gerar preocupação e cobrança sobre a manutenção da rede — confirmar que voltou já cumpre o objetivo.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56590",
        "bairro": "Bairro Panorama",
        "titulo": "Suporte — Pedido de Bloqueio Indevido",
        "cliente": "Sr. Rogério",
        "equipamento": "Roteador doméstico",
        "briefing": "O cliente pede pra você bloquear, na rede da casa, o acesso ao Wi-Fi do vizinho — ele acha que o vizinho está 'roubando' o sinal dele, sem nenhuma evidência concreta.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "53403",
            "horario": "13h30",
            "assunto": "Realizar serviços - configurações",
            "endereco": "AVENIDA MARECHAL RONDON, 847",
            "cidade": "Cujubim",
            "referencia": "Perto do campo de futebol",
            "caixa_atendimento": "CUJU 05",
            "porta_ftth": "5",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Realizar serviços - configurações\n"
                "Descrição O.S. anterior: - Solicitante: atendente Rafael\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99929-5601\n"
                "Ocorrência: Cliente solicita bloqueio de um dispositivo não identificado que estaria utilizando sua rede Wi-Fi sem autorização."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "O Sr. Rogério pede pra você configurar algo que impeça 'o vizinho de usar o Wi-Fi dele', mas ao perguntar, você percebe que ele só está desconfiado, sem nenhuma prova real de acesso indevido.",
             "pergunta": "Qual é a primeira coisa a fazer antes de qualquer ação?",
             "opcoes": [
                {
                    "texto": "Verificar tecnicamente quantos e quais dispositivos estão realmente conectados na rede dele, pra confirmar se existe mesmo algum dispositivo desconhecido",
                    "correta": True,
                    "feedback": "Correto — antes de agir sobre uma suspeita, vale checar os fatos técnicos: ver a lista de dispositivos conectados no painel do roteador mostra rapidamente se existe algo estranho ou não.",
                },
                {
                    "texto": "Trocar a senha do Wi-Fi por uma bem mais forte imediatamente, que é o que resolve qualquer acesso indevido e já deixa o cliente tranquilo ali na hora",
                    "correta": False,
                    "feedback": "Trocar a senha é inofensivo e pode até acontecer no fim. Mas fazer isso antes de verificar significa nunca saber se havia alguém — e o cliente segue desconfiando do vizinho.",
                },
                {
                    "texto": "Ativar o filtro por endereço MAC no roteador, liberando apenas os aparelhos da casa, o que na prática impede qualquer dispositivo estranho de entrar na rede dele",
                    "correta": False,
                    "feedback": "Filtro por MAC dá trabalho de manter e é contornável. Antes de qualquer trava, vale confirmar se existe mesmo aparelho desconhecido — pode não haver nada a bloquear.",
                },
            ]},
            {"cena": "Você verifica a lista de dispositivos conectados: todos são identificáveis como aparelhos da própria família do Sr. Rogério, sem nenhum dispositivo estranho.",
             "pergunta": "Como você comunica esse resultado a ele?",
             "opcoes": [
                {
                    "texto": "Mostra a lista de dispositivos conectados, explicando que não há indício de acesso indevido no momento, e sugere que a senha atual já é segura, mas que ele pode trocá-la se quiser mais tranquilidade",
                    "correta": True,
                    "feedback": "Boa comunicação — mostra o resultado técnico real, e ainda oferece uma ação simples (trocar senha) que traz tranquilidade extra, mesmo sem evidência de problema.",
                },
                {
                    "texto": "Mostra a lista e explica que, como não há nada estranho, não é necessário mexer em nada na configuração atual da rede dele por enquanto",
                    "correta": False,
                    "feedback": "A leitura está certa, mas fechar a porta pra troca de senha ignora o que ele sente. Ele veio preocupado; oferecer a troca como opção resolve sem gerar alarme.",
                },
                {
                    "texto": "Mostra a lista e sugere trocar a senha assim mesmo, porque um vizinho que já tenha entrado antes pode estar desconectado no exato momento do teste e voltar depois que você sair",
                    "correta": False,
                    "feedback": "É possível em tese, e por isso a troca fica como opção. Mas apresentar isso como provável alimenta a suspeita que os dados não sustentam.",
                },
            ]},
            {"cena": "O Sr. Rogério fica mais tranquilo, mas ainda pede pra 'bloquear o Wi-Fi do vizinho' por precaução, mesmo sem evidência.",
             "pergunta": "Isso é algo que você pode/deve fazer?",
             "opcoes": [
                {
                    "texto": "Explicar que não é tecnicamente possível (nem apropriado) 'bloquear' a rede Wi-Fi de outra pessoa a partir do roteador dele — o que dá pra fazer é reforçar a segurança da própria rede dele",
                    "correta": True,
                    "feedback": "Correto e honesto — tecnicamente não existe essa função de 'bloquear a rede de outra pessoa' a partir do próprio roteador; o caminho real é fortalecer a segurança da rede própria.",
                },
                {
                    "texto": "Explica que dá pra reduzir a potência do Wi-Fi dele pra que o sinal não alcance a casa do vizinho, o que na prática já resolveria a preocupação que ele trouxe hoje",
                    "correta": False,
                    "feedback": "Reduzir potência deixaria a própria casa dele com pontos sem sinal, e não é isso que ele quer. Além disso, não é o Wi-Fi dele que ele pediu pra bloquear.",
                },
                {
                    "texto": "Explica que não dá pra bloquear e sugere que ele registre uma reclamação na Norte Tel sobre a rede do vizinho, que atende os dois endereços",
                    "correta": False,
                    "feedback": "A empresa não interfere na rede doméstica de um cliente a pedido de outro, e encaminhar assim gera uma expectativa que ninguém vai atender.",
                },
            ]},
            {"cena": "Você troca a senha do Wi-Fi por uma mais forte, a pedido dele, como medida de tranquilidade.",
             "pergunta": "O que mais vale orientar antes de encerrar?",
             "opcoes": [
                {
                    "texto": "Reforçar que, se ele notar de fato algo estranho no futuro (lentidão sem explicação, dispositivo desconhecido na lista), pode entrar em contato pra uma nova verificação",
                    "correta": True,
                    "feedback": "Boa orientação final — deixa uma porta aberta pra investigação real caso surja evidência concreta no futuro, sem alimentar uma suspeita sem fundamento agora.",
                },
                {
                    "texto": "Orientar que ele confira a lista de dispositivos conectados pelo aplicativo de vez em quando, pra ele mesmo ir acompanhando se aparece algum aparelho desconhecido ali",
                    "correta": False,
                    "feedback": "A dica é boa e tem um efeito colateral: ele já veio ansioso com o assunto, e conferir a lista toda semana costuma alimentar a desconfiança em vez de tranquilizar.",
                },
                {
                    "texto": "Orientar que ele troque a senha do Wi-Fi a cada dois ou três meses, como uma rotina fixa de segurança, mesmo sem nenhum indício concreto de acesso indevido na rede",
                    "correta": False,
                    "feedback": "Troca periódica sem motivo cria trabalho de reconectar a casa toda e não aumenta a segurança de uma senha que já é forte. O que vale é agir quando houver indício.",
                },
            ]},
        ],
    },
    {
        "id": "OS-56644",
        "bairro": "Setor 02 (Ariquemes)",
        "titulo": "Suporte — Diagnóstico Remoto Antes da Visita",
        "cliente": "Sra. Terezinha",
        "equipamento": "Telefone, acesso remoto ao sistema da ONT",
        "briefing": "Cliente liga reclamando de internet lenta. Antes de sair pra visita, você tenta um diagnóstico remoto pelo sistema da central.",
        "instrumento": "wifi",
        "os_info": {
            "id_cliente": "50197",
            "horario": "13h30",
            "assunto": "Internet Lenta",
            "endereco": "AVENIDA PRINCIPAL, 908",
            "cidade": "Alto Alegre",
            "referencia": "Perto da praça central",
            "caixa_atendimento": "AAPC 05",
            "porta_ftth": "7",
            "descricao": (
                "Processo: Suporte Unificado. Tarefa: Internet Lenta\n"
                "Descrição O.S. anterior: - Solicitante: atendente Lucas\n"
                "Horário do Cliente: a combinar\n"
                "Número de Contato: (69) 99901-4228\n"
                "Ocorrência: Cliente liga reclamando de internet lenta. Solicita verificação técnica no local."
            ),
        },
        "apr_gabarito": {
            "subiu_poste": False,
            "atividade_esperada": "Manutenção casa do cliente (internet lenta, sem internet, configuração)",
            "riscos_obrigatorios": [],
            "epis_obrigatorios": [],
        },
        "decisoes": [
            {"cena": "Pelo sistema remoto, você consegue ver que a ONT da Sra. Terezinha está reportando sinal óptico normal e sem erros.",
             "pergunta": "O que isso sugere sobre a necessidade de uma visita presencial?",
             "opcoes": [
                {
                    "texto": "Como o sinal óptico está normal remotamente, o problema provavelmente está em algo local da casa (Wi-Fi, dispositivo específico) — vale tentar orientar por telefone antes de agendar visita",
                    "correta": True,
                    "feedback": "Boa abordagem — usar diagnóstico remoto pra descartar causas de rede externa antes de deslocar um técnico economiza tempo tanto da empresa quanto do cliente, quando possível resolver por telefone.",
                },
                {
                    "texto": "Que a visita continua necessária, já que o sinal óptico normal não descarta problema no cabeamento interno ou no equipamento dentro da casa",
                    "correta": False,
                    "feedback": "Pode acabar sendo necessária, sim. Mas com o sinal bom no sistema, uma ligação de cinco minutos costuma resolver ou pelo menos apontar a causa — antes de gastar um deslocamento.",
                },
                {
                    "texto": "Que vale agendar a visita mesmo assim e aproveitar pra revisar toda a instalação da cliente, já que o deslocamento até o bairro já estaria previsto",
                    "correta": False,
                    "feedback": "Aproveitar o deslocamento é raciocínio de agenda, não de diagnóstico. Se o problema pode ser resolvido por telefone, a visita ocupa um horário que outro cliente precisa.",
                },
            ]},
            {"cena": "Você liga pra Sra. Terezinha e pede pra ela verificar quantos dispositivos estão conectados no Wi-Fi no momento.",
             "pergunta": "Por que essa pergunta é relevante?",
             "opcoes": [
                {
                    "texto": "Muitos dispositivos usando a internet ao mesmo tempo (streaming, downloads) podem explicar lentidão percebida, mesmo com o sinal de rede normal",
                    "correta": True,
                    "feedback": "Boa linha de investigação por telefone — descobrir o uso simultâneo é uma causa comum de lentidão percebida que não tem relação com a qualidade do sinal em si.",
                },
                {
                    "texto": "Porque o roteador entregue tem limite de aparelhos simultâneos, e passar desse número faz a conexão cair pra quem entrar depois do limite",
                    "correta": False,
                    "feedback": "Roteador doméstico aguenta bem mais aparelhos do que uma casa costuma ter. O ponto não é o número de conectados: é quantos estão consumindo banda pesada ao mesmo tempo.",
                },
                {
                    "texto": "Porque saber quantos aparelhos existem permite calcular quanto de velocidade caberia pra cada um e conferir se o plano contratado por ela está subdimensionado",
                    "correta": False,
                    "feedback": "Banda não se divide em partes iguais e fixas por aparelho. A pergunta serve pra descobrir se há download pesado rodando agora — não pra recalcular o plano dela.",
                },
            ]},
            {"cena": "A cliente confirma que há vários dispositivos conectados, incluindo dois celulares baixando atualizações grandes no momento.",
             "pergunta": "Como você orienta a Sra. Terezinha por telefone?",
             "opcoes": [
                {
                    "texto": "Explica que provavelmente é isso que está causando a lentidão percebida no momento, e sugere que ela teste de novo mais tarde, quando os downloads terminarem",
                    "correta": True,
                    "feedback": "Boa orientação — uma explicação simples e prática que resolve a dúvida da cliente sem precisar de visita técnica, já que a causa foi identificada remotamente.",
                },
                {
                    "texto": "Sugere que ela pause os downloads agora mesmo e refaça o teste em seguida, pra confirmar ali na hora se era isso mesmo que estava causando a lentidão que ela sentiu",
                    "correta": False,
                    "feedback": "Confirmar na hora é tentador, mas exige que ela mexa em dois aparelhos e interrompa o que a família está usando. Testar depois que terminarem chega à mesma conclusão sem atrito.",
                },
                {
                    "texto": "Explica a causa e sugere que ela configure limite de banda por aparelho no roteador, pra que downloads pesados não travem o restante da casa",
                    "correta": False,
                    "feedback": "É uma solução válida pra quem convive com o problema, e pode ser oferecida depois. Por telefone, com ela sem familiaridade com o painel, orientar configuração vira frustração.",
                },
            ]},
            {"cena": "Mais tarde, a Sra. Terezinha liga de volta confirmando que a internet voltou a ficar rápida depois que os downloads terminaram.",
             "pergunta": "O que essa confirmação reforça sobre a abordagem usada?",
             "opcoes": [
                {
                    "texto": "Que o diagnóstico remoto bem feito, combinado com uma boa comunicação por telefone, pode resolver certos problemas sem necessidade de deslocar um técnico até o local",
                    "correta": True,
                    "feedback": "Exatamente — esse tipo de resolução remota, quando possível, é benéfico pra todos: cliente atendido mais rápido, e recursos técnicos otimizados pra atendimentos que realmente precisam de visita presencial.",
                },
                {
                    "texto": "Que o diagnóstico remoto resolve a maior parte dos casos de lentidão, e que vale sempre tentar resolver por telefone antes de abrir qualquer visita técnica presencial",
                    "correta": False,
                    "feedback": "Aqui funcionou porque o sinal estava normal e a causa era local e simples. Generalizar pra 'sempre tentar antes' atrasa os casos em que a visita é mesmo necessária.",
                },
                {
                    "texto": "Que a cliente ficou satisfeita principalmente pela rapidez, e que conseguir resolver tudo no mesmo dia é o que mais pesa na percepção dela de um bom atendimento",
                    "correta": False,
                    "feedback": "Rapidez ajudou, mas ela ficou satisfeita porque o problema foi entendido e explicado. Rápido e errado teria virado um segundo chamado na semana seguinte.",
                },
            ]},
        ],
    },
]
